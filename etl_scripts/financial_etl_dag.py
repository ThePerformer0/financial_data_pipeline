from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import sys
sys.path.append('../etl_scripts')
from extract_transform import extract_stock_data, transform_stock_data, load_to_db, STOCK_TICKERS, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, TABLE_NAME

# Définition du DAG

def etl_pipeline():
    logging.info('--- Airflow ETL pipeline started ---')
    raw_data_df = extract_stock_data(STOCK_TICKERS)
    if not raw_data_df.empty:
        final_data_df = transform_stock_data(raw_data_df)
        if not final_data_df.empty:
            load_to_db(final_data_df, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, TABLE_NAME)
        else:
            logging.warning('Transformed DataFrame is empty. Skipping load step.')
    else:
        logging.warning('Raw DataFrame is empty. Skipping pipeline execution.')
    logging.info('--- Airflow ETL pipeline finished ---')

with DAG(
    dag_id='financial_data_etl',
    description='ETL pipeline for financial market data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['financial', 'ETL', 'yfinance'],
) as dag:
    run_etl = PythonOperator(
        task_id='run_etl_pipeline',
        python_callable=etl_pipeline
    )

    run_etl
