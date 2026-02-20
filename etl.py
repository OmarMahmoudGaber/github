import pandas as pd
import duckdb
import os

def run_simple_etl():
    # 1. EXTRACT
    df = pd.read_csv('data.csv')
    print("Extracting: data.csv loaded.")

    # 2. TRANSFORM (Basic Pandas cleaning)
    # Standardize names and handle nulls
    df['customer_name'] = df['customer_name'].fillna('Guest')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
    df['region'] = df['region'].str.capitalize()
    print("Transforming: Basic cleaning complete.")

    # 3. LOAD (Into DuckDB for dbt)
    con = duckdb.connect('dev.duckdb')
    con.execute("CREATE OR REPLACE TABLE raw_sales_data AS SELECT * FROM df")
    con.close()
    print("Loading: Data pushed to dev.duckdb.")

if __name__ == "__main__":
    run_simple_etl()