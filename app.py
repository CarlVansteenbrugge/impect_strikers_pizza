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

# Leeftijdsgrenzen bepalen
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())

# Percentile-kolommen
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

# --- Resetknop ---
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.update({
        "Age": (min_age, max_age),
        "Competition": "",
        "Club": "",
        "Player": "",
        **{col: (0, 100) for col in percentile_columns}
    })
    st.rerun()

# --- Titel ---
st.title("⚽ Striker Performance Dashboard (Pizza Plots)")

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filters")

# Leeftijd
age_range = st.sidebar.slider("Age", min_value=min_age, max_value=max_age, value=(min_age, max_age), key="Age")
df_age_filtered = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

# Competitie (optioneel)
competitions = sorted(df_age_filtered['competitionName'].dropna().unique().tolist())
selected_competition = st.sidebar.selectbox("Competition (optioneel)", options=[""] + competitions, key="Competition")

if selected_competition:
    df_comp_filtered = df_age_filtered[df_age_filtered['competitionName'] == selected_competition]
else:
    df_comp_filtered = df_age_filtered

# Club (optioneel)
clubs = sorted(df_comp_filtered['squadName'].dropna().unique().tolist())
selected_club = st.sidebar.selectbox("Club (optioneel)", options=[""] + clubs, key="Club")

if selected_club:
    df_club_filtered = df_comp_filtered[df_comp_filtered['squadName'] == selected_club]
else:
    df_club_filtered = df_comp_filtered

# --- Percentile filters ---
st.sidebar.header("📊 Advanced Percentile Filters")
df_percentile_filtered = df_club_filtered.copy()

for col in percentile_columns:
    if col in df_percentile_filtered.columns:
        selected_range = st.sidebar.slider(
            label=col.replace('PERCENTILE ', ''),
            min_value=0, max_value=100,
            value=(0, 100),
            key=col
        )
        df_percentile_filtered = df_percentile_filtered[
            df_percentile_filtered[col].between(selected_range[0], selected_range[1])
        ]

# --- Filter de spelerslijst op basis van de percentielen en andere filters ---
player_names = sorted(df_percentile_filtered['playerName'].dropna().unique().tolist())

# Als de lijst leeg is, toon een melding
if len(player_names) == 0:
    st.warning("⚠️ Geen enkele speler voldoet aan de huidige filters.")
else:
    # Spelerselectie
    selected_player = st.sidebar.selectbox("Player", options=[""] + player_names, key="Player")

    # --- Plot tonen als speler gekozen is ---
    if selected_player:
        player_df = df_percentile_filtered[df_percentile_filtered['playerName'] == selected_player]
        if not player_df.empty:
            st.subheader(f"🎯 Pizza Plot: {selected_player}")
            fig = Pizza_plot_forwards(selected_player, df_percentile_filtered)
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
            st.image(buf.getvalue(), use_column_width=False, width=500)
        else:
            st.warning("⚠️ Deze speler voldoet niet aan de huidige percentile filters.")

