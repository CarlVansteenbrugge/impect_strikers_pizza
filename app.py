import streamlit as st
import pandas as pd
from strikers import load_striker_data
from pizza_utils import Pizza_plot_forwards
import matplotlib.pyplot as plt
from io import BytesIO

# --- Pagina-instellingen ---
st.set_page_config(layout="wide", page_title="Striker Pizza Dashboard")

# --- Data inladen ---
df = load_striker_data()

# --- Titel ---
st.title("⚽ Striker Performance Dashboard (Pizza Plots)")

# --- Resetknop ---
if st.sidebar.button("🔄 Reset Filters"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filters")

# Leeftijd filter
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.sidebar.slider("Age", min_value=min_age, max_value=max_age, value=(min_age, max_age), key="Age")

# Stap 1: Filter op leeftijd
df_age_filtered = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

# --- Stap 2: Competitie en Club als optionele filters ---

# Competitie filter (optioneel)
competitions = sorted(df_age_filtered['competitionName'].dropna().unique().tolist())
selected_competition = st.sidebar.selectbox("Competition (optioneel)", options=[""] + competitions, key="Competition")

if selected_competition:
    df_comp_filtered = df_age_filtered[df_age_filtered['competitionName'] == selected_competition]
else:
    df_comp_filtered = df_age_filtered

# Club filter (optioneel)
clubs = sorted(df_comp_filtered['squadName'].dropna().unique().tolist())
selected_club = st.sidebar.selectbox("Club (optioneel)", options=[""] + clubs, key="Club")

if selected_club:
    df_club_filtered = df_comp_filtered[df_comp_filtered['squadName'] == selected_club]
else:
    df_club_filtered = df_comp_filtered

# --- Stap 3: Dynamische percentile sliders ---
st.sidebar.header("📊 Advanced Percentile Filters")

percentile_columns = [
    'PERCENTILE IMPECT_SCORE_PACKING',
    'PERCENTILE PROGRESSION_SCORE_PACKING',
    'PERCENTILE OFFENSIVE_IMPECT_SCORE_PACKING',
    'PERCENTILE SCORER_SCORE',
    'PERCENTILE PXT',
    'PERCENTILE IMPECT_SCORE_PXT',
    'PERCENTILE OFFENSIVE_IMPECT_SCORE_PXT',
    'PERCENTILE HOLD_UP_PLAY_SCORE',
    'PERCENTILE RATIO_GROUND_DUELS',
    'PERCENTILE TOTAL_TOUCHES',
    'PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_AM',
    'PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_IBW',
    'PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_IB',
    'PERCENTILE AVAILABILITY_OUT_WIDE_SCORE',
    'PERCENTILE AVAILABILITY_BTL_SCORE',
    'PERCENTILE AVAILABILITY_FDR_SCORE',
    'PERCENTILE AVAILABILITY_IN_THE_BOX_SCORE',
    'PERCENTILE RATIO_MINUTES_PER_SHOT_XG',
    'PERCENTILE RATIO_POSTSHOT_XG_SHOT_XG',
    'PERCENTILE CLOSE_RANGE_SHOT_SCORE',
    'PERCENTILE ONE_VS_ONE_AGAINST_GK_SCORE',
    'PERCENTILE HEADER_SHOT_SCORE',
    'PERCENTILE OFFENSIVE_HEADER_SCORE'
]

df_percentile_filtered = df_club_filtered.copy()

# Pas de percentile filters toe
for col in percentile_columns:
    if col in df_percentile_filtered.columns:
        selected_range = st.sidebar.slider(
            label=col.replace('PERCENTILE ', ''),
            min_value=0, max_value=100,
            value=(0, 100), key=col
        )
        df_percentile_filtered = df_percentile_filtered[
            df_percentile_filtered[col].between(selected_range[0], selected_range[1])
        ]

# --- Stap 4: Player selector helemaal onderaan ---
player_names = sorted(df_percentile_filtered['playerName'].dropna().unique().tolist())
selected_player = st.sidebar.selectbox("Player", options=[""] + player_names, key="Player")

# --- Plot als speler gekozen is ---
if selected_player:
    st.subheader(f"🎯 Pizza Plot: {selected_player}")
    fig = Pizza_plot_forwards(selected_player, df_percentile_filtered)
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    st.image(buf.getvalue(), use_column_width=False, width=500)
else:
    st.info("👈 Selecteer een speler in de zijbalk om de Pizza Plot te tonen.")

