import streamlit as st
import pandas as pd
from strikers import load_striker_data
from pizza_utils import Pizza_plot_forwards  # Zorg dat deze functie correct werkt
import matplotlib.pyplot as plt
from io import BytesIO



# --- Pagina-instellingen ---
st.set_page_config(layout="wide", page_title="Striker Pizza Dashboard")

# --- Data inladen ---
df = load_striker_data()

# --- Titel ---
st.title("⚽ Striker Performance Dashboard (Pizza Plots)")

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filters")

# Leeftijd filter
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.sidebar.slider("Age", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Stap 1: Filter op leeftijd
df_age_filtered = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

# Stap 2: Competitie filter gebaseerd op leeftijdsfilter
competitions = sorted(df_age_filtered['competitionName'].dropna().unique().tolist())
selected_competition = st.sidebar.selectbox("Competition", options=competitions)

df_comp_filtered = df_age_filtered[df_age_filtered['competitionName'] == selected_competition]

# Stap 3: Club filter gebaseerd op competitie
clubs = sorted(df_comp_filtered['squadName'].dropna().unique().tolist())
selected_club = st.sidebar.selectbox("Club", options=clubs)

df_club_filtered = df_comp_filtered[df_comp_filtered['squadName'] == selected_club]

# Stap 4: Speler filter gebaseerd op club
player_names = sorted(df_club_filtered['playerName'].dropna().unique().tolist())
selected_player = st.sidebar.selectbox("Player", options=player_names)




if selected_player:
    st.subheader(f"🎯 Pizza Plot: {selected_player}")
    fig = Pizza_plot_forwards(selected_player, df_club_filtered)

    # Compacte weergave zonder vervorming
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    st.image(buf.getvalue(), use_column_width=False, width=500)