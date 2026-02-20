import pandas as pd
import duckdb
import os
import pytest

def test_csv_cleaning():
    """Verify Pandas transformations worked correctly."""
    df = pd.read_csv('cleaned_data.csv')
    # Ensure regions are capitalized correctly
    assert df['region'].iloc[0] in ['North', 'South', 'East', 'West']
    # Ensure no pipes remain in category
    assert not df['category'].str.contains('\|').any()

def test_duckdb_table_exists():
    """Verify DuckDB has the table dbt needs."""
    assert os.path.exists('dev.duckdb'), "dev.duckdb file was not created!"
    con = duckdb.connect('dev.duckdb')
    tables = con.execute("SHOW TABLES").fetchall()
    table_names = [t[0] for t in tables]
    con.close()
    assert 'raw_sales_data' in table_names, "Table 'raw_sales_data' is missing from DuckDB!"