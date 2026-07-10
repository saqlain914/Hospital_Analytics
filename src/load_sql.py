"""
load_sql.py
-----------
Step 3 of the ETL pipeline: LOAD

Loads the cleaned hospital dataset into Microsoft SQL Server using SQLAlchemy
+ pyodbc. Configure connection details via environment variables (see .env.example).

For local development/testing without a SQL Server instance, set
DB_ENGINE=sqlite in your .env and the script will load into a local SQLite
file at data/cleaned/hospital.db instead -- handy for verifying the pipeline
before pointing it at a real SQL Server.
"""

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

CLEANED_FILE = Path(__file__).resolve().parent.parent / "data" / "cleaned" / "hospital_cleaned.csv"
SQLITE_FALLBACK = Path(__file__).resolve().parent.parent / "data" / "cleaned" / "hospital.db"

TABLE_NAME = "Patients"


def get_engine():
    db_engine = os.getenv("DB_ENGINE", "sqlite").lower()

    if db_engine == "sqlserver":
        server = os.getenv("DB_SERVER", "localhost")
        database = os.getenv("DB_NAME", "HospitalDB")
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server").replace(" ", "+")

        if username and password:
            conn_str = (
                f"mssql+pyodbc://{username}:{password}@{server}/{database}"
                f"?driver={driver}"
            )
        else:
            # Windows auth / trusted connection
            conn_str = (
                f"mssql+pyodbc://@{server}/{database}"
                f"?driver={driver}&trusted_connection=yes"
            )
        print(f"Connecting to SQL Server: {server}/{database}")
        return create_engine(conn_str)

    print(f"Using local SQLite fallback at: {SQLITE_FALLBACK}")
    return create_engine(f"sqlite:///{SQLITE_FALLBACK}")


def create_database_if_not_exists():
    """Only relevant for SQL Server; creates the database if missing."""
    if os.getenv("DB_ENGINE", "sqlite").lower() != "sqlserver":
        return

    server = os.getenv("DB_SERVER", "localhost")
    database = os.getenv("DB_NAME", "HospitalDB")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server").replace(" ", "+")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    master_conn_str = (
        f"mssql+pyodbc://{username}:{password}@{server}/master?driver={driver}"
        if username and password
        else f"mssql+pyodbc://@{server}/master?driver={driver}&trusted_connection=yes"
    )
    master_engine = create_engine(master_conn_str, isolation_level="AUTOCOMMIT")
    with master_engine.connect() as conn:
        conn.execute(text(
            f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{database}') "
            f"CREATE DATABASE [{database}]"
        ))
    print(f"Confirmed database '{database}' exists.")


def load_to_sql(df: pd.DataFrame):
    create_database_if_not_exists()
    engine = get_engine()

    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into table '{TABLE_NAME}'.")

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}"))
        count = result.scalar()
        print(f"Verification: {TABLE_NAME} now contains {count} rows.")

    return engine


def main():
    if not CLEANED_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned file not found at {CLEANED_FILE}. Run transform.py first."
        )
    df = pd.read_csv(CLEANED_FILE)
    load_to_sql(df)


if __name__ == "__main__":
    main()
