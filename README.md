# Financial Data ETL Pipeline & Streamlit Dashboard 📈

## Project Overview

This project showcases a **Data Engineering pipeline** designed to extract, transform, and load (ETL) financial market data from public APIs into a structured database. The processed data is then visualized through an interactive dashboard built with Streamlit.

The pipeline is built with modularity and scalability in mind, demonstrating core data engineering principles.

**Key Features:**

* **Automated Data Ingestion:** A Python script automates the process of fetching daily stock data.
* **Data Transformation:** Raw data is processed to calculate key financial indicators like `average_price` and `daily_gain`.
* **Structured Storage:** Cleaned data is loaded into a relational database (`SQLite`) for easy querying and analysis.
* **Interactive Visualization:** A Streamlit application provides a user-friendly dashboard to explore stock trends and performance.

## Technical Stack

* **Python:** The primary programming language for the entire pipeline.
* **`yfinance`:** A powerful library used to extract financial data from Yahoo! Finance.
* **`pandas`:** Essential for data manipulation and transformation (ETL's 'T' step).
* **`SQLAlchemy`:** A robust SQL toolkit for interacting with the database.
* **`SQLite`:** A lightweight, file-based database used for data storage.
* **`Streamlit`:** A framework for building the interactive web dashboard.
* **`Git` & `GitHub`:** Used for version control and project hosting.

## Project Structure

```

.
├── etl\_scripts/
│   └── extract\_transform.py      \# The main ETL script (E & T & L)
├── streamlit\_app/
│   └── app.py                    \# The Streamlit dashboard application
├── data/
│   └── financial\_data.db         \# The SQLite database (automatically generated)
├── .gitignore                    \# Specifies files to be ignored by Git
├── requirements.txt              \# Lists all project dependencies
└── README.md                     \# This documentation file

````

## How to Run the Project

Follow these steps to set up and run the project locally.

### Prerequisites

* Python 3.8+
* Git

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
# On macOS/Linux:
source venv/bin/activate
# On Windows (PowerShell):
.\venv\Scripts\Activate

# Install the required libraries
pip install -r requirements.txt
```

### 3\. Run the ETL Pipeline

This script will fetch the data and populate the SQLite database.

```bash
python etl_scripts/extract_transform.py
```

### 4\. Launch the Streamlit Dashboard

Open a new terminal, activate the virtual environment, and navigate to the `streamlit_app` directory.

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
