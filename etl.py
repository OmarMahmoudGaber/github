import pandas as pd
import sqlite3
import os

def run_etl():
    # 1. EXTRACT
    if not os.path.exists('data.csv'):
        print("Error: data.csv not found.")
        return
    df = pd.read_csv('data.csv')

    # 2. TRANSFORM (Pandas)
    df['customer_name'] = df['customer_name'].fillna('Guest Customer')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
    df['region'] = df['region'].str.strip().str.capitalize()
    # Prepare the split for dbt SQL models
    df[['category', 'product']] = df['product_info'].str.split('|', expand=True)

    df.to_csv('cleaned_data.csv', index=False)
    

    conn = sqlite3.connect('my_data.db')
    df.to_sql('raw_sales_data', conn, if_exists='replace', index=False)
    conn.close()
    
    print("ETL SUCCESS: Data loaded into SQLite (my_data.db)")

if __name__ == "__main__":
    run_etl()