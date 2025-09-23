import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import psycopg2
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
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

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

def load_to_db(df: pd.DataFrame, db_host: str, db_port: str, db_name: str, db_user: str, db_password: str, table_name: str):
    """
    Étape de Chargement (L) avec psycopg2.
    """
    logging.info(f"Starting data loading into PostgreSQL database...")
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        cursor = conn.cursor()
        
        # Création de la table si elle n'existe pas
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            symbol VARCHAR(10),
            date DATE,
            open DECIMAL(10,2),
            high DECIMAL(10,2),
            low DECIMAL(10,2),
            close DECIMAL(10,2),
            volume BIGINT,
            average_price DECIMAL(10,2),
            daily_gain DECIMAL(10,4)
        );
        """
        cursor.execute(create_table_query)
        
        # Suppression des données existantes
        cursor.execute(f"DELETE FROM {table_name};")
        
        # Insertion des nouvelles données
        insert_query = f"""
        INSERT INTO {table_name} (symbol, date, open, high, low, close, volume, average_price, daily_gain)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # Conversion du DataFrame en liste de tuples
        data_tuples = [tuple(row) for row in df.values]
        
        # Insertion par batch
        cursor.executemany(insert_query, data_tuples)
        
        # Commit des changements
        conn.commit()
        
        # Vérification de l'insertion
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        logging.info(f"Loading completed. {count} rows successfully inserted into the table '{table_name}'.")
        
        # Fermeture des connexions
        cursor.close()
        conn.close()
        
    except Exception as e:
        logging.error(f"Error during data loading: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        sys.exit(1)

# --- Point d'entrée du pipeline ETL ---
if __name__ == "__main__":
    logging.info("### Starting the full ETL pipeline ###")
    
    raw_data_df = extract_stock_data(STOCK_TICKERS)
    if not raw_data_df.empty:
        final_data_df = transform_stock_data(raw_data_df)
        if not final_data_df.empty:
            load_to_db(final_data_df, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, TABLE_NAME)
        else:
            logging.warning("Transformed DataFrame is empty. Skipping load step.")
    else:
        logging.warning("Raw DataFrame is empty. Skipping pipeline execution.")
    
    logging.info("### ETL pipeline finished ###")