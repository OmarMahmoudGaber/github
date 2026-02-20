import pandas as pd
import sqlite3
import os

def run_etl():
    # --- 1. EXTRACT ---
    if not os.path.exists('data.csv'):
        print("Error: data.csv not found.")
        return
    df = pd.read_csv('data.csv')

    # --- 2. TRANSFORM ---
    # Standardize names and handle nulls
    df['customer_name'] = df['customer_name'].fillna('Guest Customer')
    # Clean numeric columns to avoid dbt math errors
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce').fillna(0)
    # Normalize region casing (e.g., SOUTH -> South)
    df['region'] = df['region'].str.strip().str.capitalize()

    # --- 3. LOAD ---
    # Save a cleaned CSV for your pytest validation
    df.to_csv('cleaned_data.csv', index=False)
    
    # Load into SQLite (creates my_data.db)
    # This provides the source for dbt
    conn = sqlite3.connect('my_data.db')
    df.to_sql('raw_sales_data', conn, if_exists='replace', index=False)
    conn.close()
    
    print("ETL SUCCESS: my_data.db is ready for dbt.")

if __name__ == "__main__":
    run_etl()