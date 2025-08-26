import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# --- Configuration de l'application ---
st.set_page_config(
    page_title="Financial Data Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- Connexion à la base de données ---
@st.cache_resource
def get_db_connection():
    """
    Crée une connexion à la base de données SQLite.
    @st.cache_resource met en cache la connexion pour éviter de la recréer.
    """
    db_path = '../data/financial_data.db'
    return create_engine(f'sqlite:///{db_path}')

# --- Fonctions de chargement de données ---
def get_all_stock_data(engine) -> pd.DataFrame:
    """
    Récupère toutes les données de la table 'financial_data'.
    """
    query = "SELECT * FROM financial_data ORDER BY date DESC"
    return pd.read_sql(query, engine)

# --- Mise en page de l'interface ---
engine = get_db_connection()

st.title("Financial Market Data Pipeline 📈")
st.markdown("---")

st.markdown("""
    This dashboard demonstrates a simple **Data Engineering Pipeline** that extracts, transforms, and loads (ETL) financial market data.
    The data is sourced from `yfinance`, transformed using `pandas`, and stored in a local SQLite database.
    This application, built with `Streamlit`, then visualizes the results.
""")

st.subheader("Latest Daily Market Data")

# Affichage des données brutes
df_data = get_all_stock_data(engine)
if not df_data.empty:
    st.dataframe(df_data, use_container_width=True)
else:
    st.warning("No data found in the database. Please run the ETL script first!")

st.markdown("---")

# Visualisation des tendances de prix
st.subheader("Stock Price Trends Over Time")
# Sélecteur pour l'utilisateur
symbols = df_data['symbol'].unique()
selected_symbol = st.selectbox("Select a stock ticker:", symbols)

if selected_symbol:
    df_symbol = df_data[df_data['symbol'] == selected_symbol].sort_values(by='date')
    
    st.line_chart(df_symbol, x='date', y=['open', 'close'])

st.markdown("---")

# Visualisation du gain quotidien
st.subheader("Daily Gain Distribution")
st.markdown("Distribution of daily percentage gains for all stocks in the database.")

if not df_data.empty:
    st.bar_chart(df_data, x='symbol', y='daily_gain')