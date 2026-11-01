# Automated API-to-PostgreSQL ETL Pipeline

## Project Overview

This project implements an automated Extract, Transform, and Load (ETL) pipeline using Python and PostgreSQL. It retrieves product information from a REST API, cleans and validates the extracted data, and loads the processed records into a PostgreSQL database.

The pipeline supports API pagination, automatic retry configuration, duplicate handling through UPSERT operations, execution logging, and automated testing.

## Architecture

```text
DummyJSON REST API
        |
        v
   Data Extraction
   Python Requests
        |
        v
 Data Transformation
      Pandas
        |
        v
   Data Validation
        |
        v
     Data Loading
 SQLAlchemy + PostgreSQL
        |
        v
  Products Database
```

## Technologies Used

- Python 3.11
- PostgreSQL
- SQLAlchemy
- Pandas
- Requests
- REST API
- python-dotenv
- Pytest
- Git and GitHub

## Key Features

- REST API data extraction
- Paginated API data retrieval
- Automatic HTTP retry configuration
- Data cleaning and transformation
- Duplicate record handling
- PostgreSQL database integration
- UPSERT operations
- Execution logging
- Automated transformation tests

## Project Structure

```text
api-to-postgresql-etl-pipeline/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── pipeline.py
│   └── test_connection.py
├── tests/
│   └── test_transform.py
├── sql/
├── logs/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd api-to-postgresql-etl-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named:

```text
etl_portfolio
```

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=etl_portfolio
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
```

Keep your `.env` file private.

### 5. Run the ETL pipeline

```bash
python -m src.pipeline
```

## Run Automated Tests

```bash
python -m pytest tests/ -v
```

## Current Implementation Results

In the development run, the pipeline successfully:

- Extracted 194 product records from the API.
- Processed 194 records through the transformation stage.
- Loaded 194 records into PostgreSQL.
- Passed all 7 transformation tests.

These are observed development results, not a guarantee of future API response sizes.

## Data Source

DummyJSON Products API:

https://dummyjson.com/docs/products

## Future Enhancements

- Expand automated test coverage.
- Add integration tests for PostgreSQL.
- Implement scheduled pipeline execution.
- Add data quality monitoring.
- Introduce Apache Airflow orchestration.
- Add cloud database integration.

## Author

Data Engineering Portfolio Project