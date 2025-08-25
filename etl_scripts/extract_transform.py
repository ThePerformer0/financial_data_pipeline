import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# --- Configuration ---
STOCK_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# je prends 730 jours ce qui représente 2 ans,
# pour avoir un jeu de données plus conséquent et représentatif.
START_DATE = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
END_DATE = datetime.now().strftime('%Y-%m-%d')

def extract_stock_data(tickers: list) -> pd.DataFrame:
    """
    Étape d'Extraction (E).
    Récupère les données historiques des actions à l'aide de l'API yfinance.
    """
    print(f"Extraction des données pour: {tickers} du {START_DATE} au {END_DATE}")
    
    # Utilisation de la fonction download de yfinance pour plus d'efficacité
    data = yf.download(
        tickers=tickers,
        start=START_DATE,
        end=END_DATE,
        group_by='ticker',
        progress=False  # Cache les barres de progression pour un output propre
    )
    
    # yfinance retourne un DataFrame multi-indexé. On le 'dépile' pour une meilleure manipulation.
    data_long = pd.DataFrame()
    for ticker in tickers:
        # Sélectionne les colonnes pertinentes et ajoute une colonne 'symbol'
        if len(tickers) > 1:
            df_ticker = data[ticker].copy()
        else:
            df_ticker = data.copy()

        df_ticker['symbol'] = ticker
        df_ticker['date'] = df_ticker.index.date # Extrait la date seule
        data_long = pd.concat([data_long, df_ticker.dropna(how='all')], ignore_index=True)
    
    # Nettoyage et sélection des colonnes
    data_long = data_long[['symbol', 'date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    # Renommage des colonnes pour correspondre à notre modèle SQL
    data_long.columns = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']
    
    print(f"Extraction terminée. {len(data_long)} lignes brutes récupérées.")
    return data_long

def transform_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Étape de Transformation (T).
    Calcule des indicateurs clés (features) à partir des données brutes.
    """
    print("Démarrage de l'étape de Transformation...")
    
    # 1. Calcul du Prix Moyen (Average Price)
    df['average_price'] = (df['high'] + df['low']) / 2
    
    # 2. Calcul du Gain Quotidien en Pourcentage (Daily Gain)
    df['daily_gain'] = ((df['close'] - df['open']) / df['open']) * 100

    # On s'assure que le DataFrame final est propre et contient les colonnes attendues
    df_transformed = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume',
                         'average_price', 'daily_gain']]
    
    print("Transformation terminée. Le DataFrame est prêt pour le chargement (L).")
    return df_transformed

# --- Point d'entrée de l'exécution ---
if __name__ == "__main__":
    # 1. Extraction
    raw_data_df = extract_stock_data(STOCK_TICKERS)
    
    # 2. Transformation
    final_data_df = transform_stock_data(raw_data_df)
    
    # Afficher les 5 premières lignes pour validation
    print("\n--- Aperçu des Données Transformées (Prêtes pour SQL) ---")
    print(final_data_df.head())
    
    # Sauvegarde temporaire pour la validation
    # C'est une bonne pratique de sauvegarder le résultat intermédiaire
    # pour s'assurer que l'étape T a bien fonctionné avant de passer à l'étape L.
    output_path = '../data/transformed_data_preview.csv'
    final_data_df.to_csv(output_path, index=False)
    print(f"\nDonnées de validation sauvées dans : {output_path}")