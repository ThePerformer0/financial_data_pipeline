# Financial Data ETL Pipeline & Streamlit Dashboard 📈

## Project Overview

This project showcases a **Data Engineering pipeline** designed to extract, transform, and load (ETL) financial market data from public APIs into a structured database. The processed data is then visualized through an interactive dashboard built with Streamlit.

The pipeline is built with modularity and scalability in mind, demonstrating core data engineering principles.

**Key Features:**

* **Automated Data Ingestion:** A Python script automates the process of fetching daily stock data.
* **Data Transformation:** Raw data is processed to calculate key financial indicators like `average_price` and `daily_gain`.
* **Structured Storage:** Cleaned data is loaded into a relational database (`PostgreSQL`) for easy querying and analysis.
* **Interactive Visualization:** A Streamlit application provides a user-friendly dashboard to explore stock trends and performance.

## Technical Stack

* **Python:** The primary programming language for the entire pipeline.
* **`yfinance`:** A powerful library used to extract financial data from Yahoo! Finance.
* **`pandas`:** Essential for data manipulation and transformation (ETL's 'T' step).
* **`psycopg2`:** PostgreSQL database connector for Python.
* **`PostgreSQL`:** Robust relational database for storing financial data.
* **`Apache Airflow`:** Workflow orchestration and scheduling.
* **`Streamlit`:** A framework for building the interactive web dashboard.
* **`Git` & `GitHub`:** Used for version control and project hosting.

## Project Structure

```

.
* **Structured Storage:** Cleaned data is loaded into a relational database (`PostgreSQL`) for easy querying and analysis.
│   └── extract_transform.py      # The main ETL script (E & T & L)
├── streamlit_app/
│   └── app.py                    # The Streamlit dashboard application
├── data/
│   └── financial_data.db         # The SQLite database (automatically generated)
├── .gitignore                    # Specifies files to be ignored by Git
├── requirements.txt              # Lists all project dependencies
└── README.md                     # This documentation file

````

## How to Run the Project

Follow these steps to set up and run the project locally.

### Prerequisites

* PostgreSQL (local ou distant)
* Apache Airflow
* Python 3.8+
* Git
* Docker (recommended for easy setup)

### 1. Clone the repository

```bash
git clone https://github.com/ThePerformer0/financial_data_pipeline.git
cd financial_data_pipeline
````

### 2\. Set up the environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create and activate a virtual environment
python -m venv venv
### 3. Configure environment variables

### Alternative: Run with Docker

You can run the ETL and dashboard using Docker for easier setup and isolation.

#### On Windows (PowerShell)
```powershell

Set the following environment variables for PostgreSQL connection (replace with your values):

```powershell

#### On Linux/macOS (bash)
```bash
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="your_db_name"

This will build and start all containers defined in `docker-compose.yaml`.
The ETL will run, the dashboard will be available (check the ports in your compose file), and the database will be started automatically.
$env:DB_USER="your_db_user"
$env:DB_PASSWORD="your_db_password"
```

Or in bash:
```bash
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="your_db_name"
export DB_USER="your_db_user"
export DB_PASSWORD="your_db_password"
```
# On macOS/Linux:
source venv/bin/activate
# On Windows (PowerShell):
.\venv\Scripts\Activate

# Install the required libraries
pip install -r requirements.txt
```


If you use Docker, these environment variables can be set in the `docker-compose.yaml` file under the relevant service.
### 3\. Run the ETL Pipeline

This script will fetch the data and populate the SQLite database.

```bash
python etl_scripts/extract_transform.py
```


Or with Docker (if not using Airflow):
```bash
### 4\. Launch the Streamlit Dashboard

Open a new terminal, activate the virtual environment, and navigate to the `streamlit_app` directory.
docker compose run etl

sudo docker compose run etl
### 6. Orchestration avec Airflow

Apache Airflow permet d'automatiser et de planifier l'exécution du pipeline ETL.

#### Installation

Installez Airflow et les providers nécessaires :

```bash

Or with Docker:
```bash
pip install apache-airflow apache-airflow-providers-postgres
docker compose up dashboard
```
sudo docker compose up dashboard

#### Quick Start

Apache Airflow automates and schedules the ETL pipeline execution.

#### Installation

Install Airflow and the required providers:

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
  airflow users create --username admin --firstname First --lastname Last --role Admin --email admin@example.com --password admin
  ```
3. Start the webserver and scheduler:
  ```bash
  airflow webserver -p 8080
  airflow scheduler
  ```
4. Place the `financial_etl_dag.py` file in Airflow's `dags/` folder.
5. Check the Airflow UI (http://localhost:8080), enable the DAG, and monitor execution.

#### Educational Notes

- The Airflow DAG orchestrates extraction, transformation, and loading of financial data.
- It reuses your existing Python functions for consistency and maintainability.
- Logging helps you track each step and debug issues.
- You can change the schedule or add steps as needed.

1. Initialize the Airflow database:
  ```bash
  airflow db init
  ```
2. Create an admin user:
  ```bash
  airflow users create --username admin --firstname Firstname --lastname Lastname --role Admin --email admin@example.com --password admin
  ```
3. Start the webserver and scheduler:
  ```bash
  airflow webserver -p 8080
  airflow scheduler
  ```
4. Place the `financial_etl_dag.py` file in Airflow's `dags/` folder.
5. Check the Airflow interface (http://localhost:8080), ensure the DAG appears, and enable it.

#### Educational Notes

- The Airflow DAG orchestrates extraction, transformation, and loading of data.
- It reuses your existing Python functions for consistency and maintainability.
- Logging helps you track each step and debug issues easily.
- You can change the execution frequency or add steps as needed.

```bash
cd streamlit_app
streamlit run app.py
```

Your web browser will automatically open the dashboard.

## Potential Future Enhancements

This project is designed to be a foundation. Here are some ideas to evolve it into a more advanced data engineering solution:

  * **Orchestration:** Use a tool like **Apache Airflow** or **Prefect** to schedule the ETL script to run automatically every day.
  * **Cloud Migration:** Migrate the pipeline to a cloud provider like AWS (S3 for data lake, Redshift for data warehouse) or GCP (Cloud Storage, BigQuery).
  * **Data Warehouse:** Use a more robust database like **PostgreSQL** or **Snowflake** to handle larger volumes and more complex queries.
  * **API & Microservices:** Develop a REST API using **FastAPI** to serve the data instead of a dashboard.
  * **Advanced Analytics:** Incorporate more complex transformations, such as calculating technical indicators (e.g., Moving Averages, RSI) or integrating with machine learning models for stock prediction.

## Contribution

Feel free to suggest improvements or enhancements by opening an issue or submitting a pull request.
