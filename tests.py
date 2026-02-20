import pandas as pd
import duckdb
import os
import pytest

# --- Test 1: Validate the CSV exists and has data ---
def test_csv_existence():
    """Check if the source data file is present."""
    assert os.path.exists('data.csv'), "data.csv is missing from the directory"

def test_csv_content():
    """Verify the CSV has the expected columns and isn't empty."""
    df = pd.read_csv('data.csv')
    expected_columns = ['order_id', 'order_date', 'product_info', 'quantity', 'unit_price']
    for col in expected_columns:
        assert col in df.columns, f"Column {col} missing from data.csv"
    assert len(df) > 0, "data.csv is empty"

# --- Test 2: Validate the ETL/DuckDB Load ---
def test_duckdb_load():
    """Check if the ETL script actually created the DuckDB table."""
    # Ensure the DB file exists (created by etl.py)
    assert os.path.exists('dev.duckdb'), "dev.duckdb was not created by etl.py"
    
    # Connect and check for the raw table
    con = duckdb.connect('dev.duckdb')
    tables = con.execute("SHOW TABLES").fetchall()
    table_names = [t[0] for t in tables]
    
    assert 'raw_sales_data' in table_names, "Table 'raw_sales_data' not found in DuckDB"
    
    # Verify row count matches (Sanity check)
    df_csv = pd.read_csv('data.csv')
    db_count = con.execute("SELECT COUNT(*) FROM raw_sales_data").fetchone()[0]
    assert db_count == len(df_csv), "Row count mismatch between CSV and DuckDB"
    
    con.close()

# --- Test 3: Data Quality (Pre-dbt) ---
def test_data_logic():
    """Ensure no negative quantities before dbt starts processing."""
    con = duckdb.connect('dev.duckdb')
    negatives = con.execute("SELECT COUNT(*) FROM raw_sales_data WHERE quantity < 0").fetchone()[0]
    assert negatives == 0, "Found negative quantities in raw data!"
    con.close()