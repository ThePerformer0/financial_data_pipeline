import streamlit as st
import pandas as pd
import psycopg2
import os

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
    Crée une connexion à la base de données PostgreSQL avec psycopg2.
    """
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )

# --- Fonctions de chargement de données ---
def get_all_stock_data(conn) -> pd.DataFrame:
    """
    Récupère toutes les données de la table 'financial_data'.
    """
    query = "SELECT * FROM financial_data ORDER BY date DESC"
    try:
        return pd.read_sql_query(query, conn, index_col=None)
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return pd.DataFrame()

# --- Mise en page de l'interface ---
conn = get_db_connection()

st.title("Financial Market Data Pipeline 📈")
st.markdown("---")

st.markdown("""
    This dashboard demonstrates a simple **Data Engineering Pipeline** that extracts, transforms, and loads (ETL) financial market data.
    The data is sourced from `yfinance`, transformed using `pandas`, and stored in a local PostgreSQL database.
    This application, built with `Streamlit`, then visualizes the results.
""")

st.subheader("Latest Daily Market Data")

# Affichage des données brutes
df_data = get_all_stock_data(conn)
if not df_data.empty:
    st.dataframe(df_data, use_container_width=True)
else:
    st.warning("No data found in the database. Please run the ETL script first!")

st.markdown("---")

# Visualisation des tendances de prix
st.subheader("Stock Price Trends Over Time")
# Sélecteur pour l'utilisateur
if not df_data.empty:
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