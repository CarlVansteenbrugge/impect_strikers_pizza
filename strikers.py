import os
import time
from datetime import date
import pandas as pd
from scipy.stats import zscore, norm
import impectPy as ip
import streamlit as st

# Decorator om caching van de data mogelijk te maken
@st.cache_data(show_spinner="Data wordt geladen...")


def load_striker_data():
    username = "carl.vansteenbrugge@essevee.be"
    password = "8P5BG@iuD2r6Ter"

    # 🔑 Token ophalen via impectPy
    token = ip.getAccessToken(username=username, password=password)

    # 📦 Iteraties ophalen en filteren
    df_iterations = ip.getIterations(token=token)
    df_iterations = df_iterations[
        (df_iterations['season'] == '24/25') &
        (df_iterations['competitionType'] == 'League') &
        (df_iterations['competitionGender'] == 'MALE') &
        (~df_iterations['competitionId'].isin([2, 3, 8, 9, 10, 19, 34, 166, 241, 354, 355, 379, 380])) &
        (~df_iterations['id'].isin([1137, 1149]))
    ].copy()

    iteration_ids = df_iterations['id'].unique().tolist()

    # 🎯 Alleen center forwards
    positions = ['CENTER_FORWARD']
    
    
    all_dfs = []

    # ⏳ Iteraties ophalen met retry op rate limit
    for iteration_id in iteration_ids:
        for attempt in range(5):
            try:
                df_strikers = ip.getPlayerIterationScores(iteration=iteration_id, positions=positions, token=token)
                df_strikers = df_strikers[df_strikers['playDuration'] >= 30000]
                all_dfs.append(df_strikers)
                print(f"✅ Iteration {iteration_id} done")
                break
            except Exception as e:
                if "429" in str(e):
                    print(f"⏳ Rate limited, retrying (attempt {attempt + 1})...")
                    time.sleep(10 * (attempt + 1))
                else:
                    print(f"❌ Skipping iteration {iteration_id} due to error: {e}")
                    break

    # 📊 Gegevens combineren en voorbereiden
    df = pd.concat(all_dfs, ignore_index=True)

    # Bereken aantal 90's obv playDuration
    df["90's"] = df['playDuration']/5400
    

    # Bereken de 'Age' kolom vanuit de 'birthdate' kolom
    df['birthdate'] = pd.to_datetime(df['birthdate'], errors='coerce').dt.date
    today = date.today()
    df['Age'] = df['birthdate'].apply(lambda d: round((today - d).days / 365.25, 1) if pd.notnull(d) else None)
    
    # Deze kolommen willen we behouden
    cols = [
    'competitionName', 'squadName', 'playerId', 'playerName', 'birthdate', 'leg', 'Age',
    "90's", 'IMPECT_SCORE_PACKING', 'IMPECT_SCORE_PXT', 'OFFENSIVE_IMPECT_SCORE_PXT', 'PXT', 'SCORER_SCORE', 'PROGRESSION_SCORE_PACKING',
    'OFFENSIVE_IMPECT_SCORE_PACKING', 'TOTAL_TOUCHES_IN_PACKING_ZONE_AM',
    'TOTAL_TOUCHES_IN_PACKING_ZONE_IBWR', 'TOTAL_TOUCHES_IN_PACKING_ZONE_IBWL',
    'TOTAL_TOUCHES_IN_PACKING_ZONE_IB', 'AVAILABILITY_OUT_WIDE_SCORE',
    'AVAILABILITY_BTL_SCORE', 'AVAILABILITY_FDR_SCORE',
    'AVAILABILITY_IN_THE_BOX_SCORE', 'HOLD_UP_PLAY_SCORE', 'OFFENSIVE_HEADER_SCORE',
    'CLOSE_RANGE_SHOT_SCORE', 'ONE_VS_ONE_AGAINST_GK_SCORE', 'HEADER_SHOT_SCORE',
    'RATIO_GROUND_DUELS', 'RATIO_MINUTES_PER_SHOT_XG', 'TOTAL_TOUCHES',
    'RATIO_POSTSHOT_XG_SHOT_XG']

    # Filter de DataFrame om alleen de gewenste kolommen te behouden
    df = df[cols]



    # Van volgende kolommen willen we nu een percentielscore
    percentile_cols = ['IMPECT_SCORE_PACKING', 'IMPECT_SCORE_PXT', 'OFFENSIVE_IMPECT_SCORE_PXT', 'PXT', 'SCORER_SCORE', 'PROGRESSION_SCORE_PACKING',
    'OFFENSIVE_IMPECT_SCORE_PACKING', 'TOTAL_TOUCHES_IN_PACKING_ZONE_AM',
    'TOTAL_TOUCHES_IN_PACKING_ZONE_IBWR', 'TOTAL_TOUCHES_IN_PACKING_ZONE_IBWL',
    'TOTAL_TOUCHES_IN_PACKING_ZONE_IB', 'AVAILABILITY_OUT_WIDE_SCORE',
    'AVAILABILITY_BTL_SCORE', 'AVAILABILITY_FDR_SCORE',
    'AVAILABILITY_IN_THE_BOX_SCORE', 'HOLD_UP_PLAY_SCORE', 'OFFENSIVE_HEADER_SCORE',
    'CLOSE_RANGE_SHOT_SCORE', 'ONE_VS_ONE_AGAINST_GK_SCORE', 'HEADER_SHOT_SCORE',
    'RATIO_GROUND_DUELS', 'RATIO_MINUTES_PER_SHOT_XG', 'TOTAL_TOUCHES',
    'RATIO_POSTSHOT_XG_SHOT_XG'
    ]

    for col in percentile_cols:
    # Forceer de kolom om numerieke waarden te hebben
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Bereken de z-score
        z = zscore(df[col], nan_policy='omit')
    # Bereken de percentielen en converteer naar pandas Series om fillna toe te passen
        percentile = norm.cdf(z) * 100
        percentile = pd.Series(percentile)  # Converteer naar pandas Series om fillna te gebruiken
        df[f'PERCENTILE {col}'] = percentile.round(0).fillna(0).astype(int)

    # Omgekeerde schaal voor 'minuten per shot XG'
    df['PERCENTILE RATIO_MINUTES_PER_SHOT_XG'] = (
    100 - df['PERCENTILE RATIO_MINUTES_PER_SHOT_XG'])

    # Gemiddelde percentiel voor IBWR en IBWL
    df['PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_IBW'] = (
    (df['PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_IBWR'] + df['PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_IBWL']) / 2
).astype(int)

    return df
