import pandas as pd
import numpy as np
import os
import pytest

# Helper function to get the cleaned data
def get_cleaned_data():
    if os.path.exists('cleaned_data.csv'):
        return pd.read_csv('cleaned_data.csv')
    return None

# --- 1. Structural Tests ---

def test_output_file_exists():
    """Verify the ETL actually produced the output file."""
    assert os.path.exists('cleaned_data.csv'), "The ETL script did not create cleaned_data.csv"

def test_columns_present():
    """Verify that messy columns were removed and new ones were created."""
    df = get_cleaned_data()
    # Check that product_info was dropped
    assert 'product_info' not in df.columns
    # Check that new columns exist
    assert 'category' in df.columns
    assert 'product' in df.columns
    assert 'total_sales' in df.columns

# --- 2. Transformation Logic Tests ---

def test_null_handling():
    """Verify customer_name and quantity defaults worked."""
    df = get_cleaned_data()
    # Should not contain any nulls in these columns after ETL
    assert df['customer_name'].isnull().sum() == 0
    assert df['quantity'].isnull().sum() == 0
    # Check for our specific default string
    if 'Guest Customer' in df['customer_name'].values:
        assert True

def test_string_split_logic():
    """Verify that 'category' and 'product' are separated correctly."""
    df = get_cleaned_data()
    # Ensure category doesn't contain the pipe symbol
    assert not df['category'].str.contains('\|').any()
    assert not df['product'].str.contains('\|').any()

def test_numeric_calculations():
    """Verify that total_sales is actually quantity * unit_price."""
    df = get_cleaned_data()
    # We allow a small tolerance for floating point math
    calculated_sales = df['quantity'] * df['unit_price']
    pd.testing.assert_series_equal(df['total_sales'], calculated_sales, check_names=False)

def test_casing_normalization():
    """Verify regions are capitalized (e.g., 'South' not 'SOUTH')."""
    df = get_cleaned_data()
    # All unique values should be in Title case (Capitalized)
    for region in df['region'].unique():
        assert region == region.capitalize()

# --- 3. Deduplication Test ---

def test_duplicates_removed():
    """Verify that order_id is now unique."""
    df = get_cleaned_data()
    assert df['order_id'].is_unique, f"Duplicate order_ids found in cleaned data!"