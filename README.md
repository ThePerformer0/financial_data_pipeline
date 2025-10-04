# Financial Data ETL Pipeline & Streamlit Dashboard 📊

## Overview

This project implements a modular and scalable **Data Engineering pipeline** for extracting, transforming, and loading (ETL) financial market data from public APIs into a structured database. The processed data is visualized through an interactive **Streamlit** dashboard, enabling users to explore stock trends and performance metrics.

### Key Features
- **Automated Data Ingestion**: Fetches daily stock data using Python and public APIs.
- **Data Transformation**: Processes raw data to compute financial metrics like `average_price` and `daily_gain`.
- **Structured Storage**: Stores cleaned data in a **PostgreSQL** database for efficient querying.
- **Interactive Visualization**: Provides a user-friendly Streamlit dashboard for data exploration.

## Technical Stack

- **Python 3.8+**: Core programming language for the pipeline.
- **yfinance**: Library for extracting financial data from Yahoo Finance.
- **pandas**: Handles data manipulation and transformation.
- **psycopg2**: PostgreSQL connector for Python.
- **PostgreSQL**: Relational database for storing processed data.
- **Apache Airflow**: Orchestrates and schedules ETL workflows.
- **Streamlit**: Framework for building the interactive dashboard.
- **Git & GitHub**: Version control and project hosting.
- **Docker**: Optional for containerized setup and deployment.

## Project Structure

```
financial_data_pipeline/
├── etl_scripts/
│   └── extract_transform.py   # ETL script for data extraction, transformation, and loading
├── streamlit_app/
│   └── app.py                # Streamlit dashboard application
├── data/
│   └── financial_data.db     # SQLite database (auto-generated, for lightweight testing)
├── dags/
│   └── financial_etl_dag.py  # Airflow DAG for pipeline orchestration
├── docker-compose.yaml       # Docker configuration for containerized setup
├── .gitignore                # Specifies files ignored by Git
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup and Installation

Follow these steps to set up and run the project locally.

### Prerequisites
- Python 3.8+
- PostgreSQL (local or remote)
- Apache Airflow (optional for orchestration)
- Git
- Docker (optional for containerized setup)

### 1. Clone the Repository

```bash
git clone https://github.com/ThePerformer0/financial_data_pipeline.git
cd financial_data_pipeline
```

### 2. Set Up a Virtual Environment

Use a virtual environment to manage dependencies.

```bash
# Create and activate a virtual environment
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows (PowerShell)
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Set the following environment variables for PostgreSQL connectivity (replace with your values):

#### On macOS/Linux (bash)
```bash
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="your_db_name"
export DB_USER="your_db_user"
export DB_PASSWORD="your_db_password"
```

#### On Windows (PowerShell)
```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="your_db_name"
$env:DB_USER="your_db_user"
$env:DB_PASSWORD="your_db_password"
```

Alternatively, define these variables in the `docker-compose.yaml` file if using Docker.

### 4. Run the ETL Pipeline

Execute the ETL script to fetch, transform, and load data into the database.

```bash
python etl_scripts/extract_transform.py
```

### 5. Launch the Streamlit Dashboard

Run the Streamlit application to view the interactive dashboard.

```bash
cd streamlit_app
streamlit run app.py
```

The dashboard will open automatically in your default web browser (typically at `http://localhost:8501`).

### 6. Orchestrate with Apache Airflow (Optional)

Use Apache Airflow to automate and schedule the ETL pipeline.

#### Installation
```bash
pip install apache-airflow apache-airflow-providers-postgres
```

#### Quick Start
1. Initialize the Airflow database:
   ```bash
   airflow db init
   ```
2. Create an admin user:
   ```bash
   airflow users create --username admin --firstname Firstname --lastname Lastname --role Admin --email admin@example.com --password admin
   ```
3. Start the Airflow webserver and scheduler:
   ```bash
   airflow webserver -p 8080
   airflow scheduler
   ```
4. Copy `financial_etl_dag.py` to Airflow's `dags/` folder.
5. Access the Airflow UI at `http://localhost:8080`, enable the DAG, and monitor execution.

#### Notes
- The Airflow DAG orchestrates the ETL process, reusing Python functions for consistency.
- Logging is implemented to track steps and debug issues.
- Customize the schedule or add tasks in `financial_etl_dag.py` as needed.

### 7. Run with Docker (Optional)

For a containerized setup, use Docker to simplify deployment.

```bash
docker compose up
```

This starts the ETL pipeline, Streamlit dashboard, and PostgreSQL database. Check `docker-compose.yaml` for port configurations (e.g., Streamlit at `http://localhost:8501`).

## Future Enhancements

- **Advanced Orchestration**: Integrate **Prefect** or enhance Airflow for more complex workflows.
- **Cloud Deployment**: Migrate to AWS (S3, Redshift) or GCP (Cloud Storage, BigQuery) for scalability.
- **Data Warehouse**: Use **Snowflake** or **PostgreSQL** for handling larger datasets.
- **API Development**: Build a **FastAPI** REST API to serve data dynamically.
- **Analytics**: Add technical indicators (e.g., RSI, Moving Averages) or machine learning models for predictive analytics.

## Contributing

Contributions are welcome! Please:
1. Open an issue to discuss proposed changes.
2. Submit a pull request with your enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.