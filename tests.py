import pandas as pd
import sqlite3
import os

def test_etl_execution():
    """Verify that the ETL script produced the required files."""
    assert os.path.exists('cleaned_data.csv'), "CSV was not created!"
    assert os.path.exists('my_data.db'), "SQLite database was not created!"

def test_data_integrity():
    """Check if the cleaning logic worked correctly."""
    df = pd.read_csv('cleaned_data.csv')
    # Check that region normalization worked
    assert 'South' in df['region'].values
    # Ensure there are no nulls in customer_name
    assert df['customer_name'].isnull().sum() == 0
    # Dynamic check: Ensure we actually have rows
    assert len(df) > 0, "The dataset should not be empty."