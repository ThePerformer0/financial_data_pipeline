import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import logging
import sys
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
STOCK_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'GS', 'META', 'NVDA']
END_DATE = datetime.now().strftime('%Y-%m-%d')
START_DATE = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')

# --- Récupération des variables d'environnement pour PostgreSQL ---
# C'est la solution professionnelle pour gérer les informations de connexion
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Chaîne de connexion construite à partir des variables d'environnement
DB_CONNECTION_STRING = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
TABLE_NAME = 'financial_data'

def extract_stock_data(tickers: list) -> pd.DataFrame:
    """
    Étape d'Extraction (E).
    """
    logging.info(f"Starting data extraction for: {tickers} from {START_DATE} to {END_DATE}")
    try:
        data = yf.download(
            tickers=tickers,
            start=START_DATE,
            end=END_DATE,
            group_by='ticker',
            progress=False
        )
        data_long = pd.DataFrame()
        for ticker in tickers:
            if len(tickers) > 1:
                df_ticker = data[ticker].copy()
            else:
                df_ticker = data.copy()
            df_ticker['symbol'] = ticker
            df_ticker['date'] = df_ticker.index.date
            data_long = pd.concat([data_long, df_ticker.dropna(how='all')], ignore_index=True)
            
        data_long = data_long.loc[:, ['symbol', 'date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        data_long.columns = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']
        
        logging.info(f"Extraction successful. {len(data_long)} raw rows retrieved.")
        return data_long
    except Exception as e:
        logging.error(f"Error during data extraction: {e}")
        return pd.DataFrame()

def transform_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Étape de Transformation (T).
    """
    logging.info("Starting data transformation...")
    try:
        df.loc[:, 'average_price'] = (df['high'] + df['low']) / 2
        df.loc[:, 'daily_gain'] = ((df['close'] - df['open']) / df['open']) * 100
        
        df_transformed = df.loc[:, ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 
                                    'average_price', 'daily_gain']]
        logging.info("Transformation completed. DataFrame is ready for loading.")
        return df_transformed
    except Exception as e:
        logging.error(f"Error during data transformation: {e}")
        return pd.DataFrame()

def load_to_db(df: pd.DataFrame, connection_string: str, table_name: str):
    """
    Étape de Chargement (L).
    """
    logging.info(f"Starting data loading into PostgreSQL database...")
    try:
        engine = create_engine(connection_string)
        
        # Le code de création de la table doit s'exécuter dans sa propre connexion
        with engine.connect() as conn:
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                symbol TEXT NOT NULL,
                date DATE NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                average_price REAL,
                daily_gain REAL,
                PRIMARY KEY (symbol, date)
            );
            """
            conn.execute(text(create_table_sql))
            logging.info(f"Table '{table_name}' checked or created successfully.")
            
        # L'insertion des données se fait directement via l'objet engine
        # to_sql est une méthode de Pandas qui se connecte et insère les données.
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        
        # Vérification de l'insertion des données
        with engine.connect() as conn:
            count_query = f"SELECT COUNT(*) FROM {table_name};"
            count = pd.read_sql(count_query, conn).iloc[0, 0]
            logging.info(f"Loading completed. {count} rows successfully inserted into the table '{table_name}'.")

    except Exception as e:
        logging.error(f"Error during data loading: {e}")
        # En cas d'échec, le programme s'arrête
        sys.exit(1)

# --- Point d'entrée du pipeline ETL ---
if __name__ == "__main__":
    logging.info("### Starting the full ETL pipeline ###")
    
    raw_data_df = extract_stock_data(STOCK_TICKERS)
    if not raw_data_df.empty:
        final_data_df = transform_stock_data(raw_data_df)
        if not final_data_df.empty:
            load_to_db(final_data_df, DB_CONNECTION_STRING, TABLE_NAME)
        else:
            logging.warning("Transformed DataFrame is empty. Skipping load step.")
    else:
        logging.warning("Raw DataFrame is empty. Skipping pipeline execution.")
    
    logging.info("### ETL pipeline finished ###")