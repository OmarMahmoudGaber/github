import pandas as pd
import os
import sqlite3
import pytest

def test_files_created():
    """Verify ETL outputs exist."""
    assert os.path.exists('cleaned_data.csv')
    assert os.path.exists('my_data.db')

def test_sqlite_content():
    """Check if data reached the database correctly."""
    conn = sqlite3.connect('my_data.db')
    df = pd.read_sql('SELECT * FROM raw_sales_data', conn)
    conn.close()
    
    # Check that we actually have data (dynamic check)
    assert len(df) > 0, "The database table is empty!"
    
    # Check if your transformation logic worked
    assert 'Guest Customer' in df['customer_name'].values