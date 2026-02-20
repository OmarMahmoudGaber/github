import pandas as pd
import numpy as np
import os
import duckdb # Add this import


FILE_NAME = 'data.csv'

if not os.path.exists(FILE_NAME):
    print(f"Error: {FILE_NAME} not found in current directory.")
else:
    print(f"Loading {FILE_NAME}...")
    df = pd.read_csv(FILE_NAME)

    print("Transforming data...")

    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df[['category', 'product']] = df['product_info'].str.split('|', expand=True)
    

    if 'customer_name' in df.columns:
        df['customer_name'] = df['customer_name'].fillna('Guest Customer')
    
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    
    median_price = df['unit_price'].median()
    df['unit_price'] = df['unit_price'].fillna(median_price)

    df['region'] = df['region'].str.strip().str.capitalize()
    df['total_sales'] = df['quantity'] * df['unit_price']

    df.drop_duplicates(subset=['order_id'], keep='first', inplace=True)
    

    OUTPUT_FILE = 'cleaned_data.csv'
    df.to_csv(OUTPUT_FILE, index=False)

    print("Loading into DuckDB...")
    con = duckdb.connect('dev.duckdb')

    con.execute("CREATE OR REPLACE TABLE raw_sales_data AS SELECT * FROM df")
    con.close()
    
    print("-" * 30)
    print(f"SUCCESS: Data ready for dbt in dev.duckdb")