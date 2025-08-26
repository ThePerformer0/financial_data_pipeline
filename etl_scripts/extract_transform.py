import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# --- Configuration ---
STOCK_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'GS', 'META', 'NVDA']
END_DATE = datetime.now().strftime('%Y-%m-%d')
START_DATE = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
DB_PATH = '../data/financial_data.db'

def extract_stock_data(tickers: list) -> pd.DataFrame:
    """
    Extraction (E).
    """
    print(f"Extraction des données pour: {tickers} du {START_DATE} au {END_DATE}")
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
    data_long = data_long[['symbol', 'date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    data_long.columns = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']
    print(f"Extraction terminée. {len(data_long)} lignes brutes récupérées.")
    return data_long

def transform_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformation (T).
    """
    print("Démarrage de l'étape de Transformation...")
    df['average_price'] = (df['high'] + df['low']) / 2
    df['daily_gain'] = ((df['close'] - df['open']) / df['open']) * 100
    df_transformed = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 
                         'average_price', 'daily_gain']]
    print("Transformation terminée. Le DataFrame est prêt pour le chargement (L).")
    return df_transformed

def load_to_db(df: pd.DataFrame, db_path: str):
    """
    Chargement (L).
    Connecte à la base de données, crée la table si elle n'existe pas,
    puis charge les données du DataFrame.
    """
    print(f"Démarrage du chargement vers la base de données : {db_path}")
    # Crée un moteur de base de données SQLite.
    engine = create_engine(f'sqlite:///{db_path}')

    # Définition de la table SQL avec SQLAlchemy.
    table_name = 'financial_data'
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
    with engine.connect() as connection:
        connection.execute(text(create_table_sql))
        print(f"Table '{table_name}' vérifiée ou créée avec succès.")

    # Chargement du DataFrame Pandas dans la table SQL
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Chargement terminé. {len(df)} lignes insérées dans la table '{table_name}'.")

# --- Point d'entrée de l'exécution ---
if __name__ == "__main__":
    # Pipeline ETL complet
    try:
        raw_data_df = extract_stock_data(STOCK_TICKERS)
        if not raw_data_df.empty:
            final_data_df = transform_stock_data(raw_data_df)
            load_to_db(final_data_df, DB_PATH)
        else:
            print("Aucune donnée à traiter. Fin du script.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'exécution du pipeline : {e}")