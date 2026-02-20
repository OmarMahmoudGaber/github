import pandas as pd
import numpy as np
import os

# --- 1. EXTRACT ---
FILE_NAME = 'data.csv'

if not os.path.exists(FILE_NAME):
    print(f"Error: {FILE_NAME} not found in current directory.")
else:
    print(f"Loading {FILE_NAME}...")
    df = pd.read_csv(FILE_NAME)

    # --- 2. TRANSFORM ---
    print("Transforming data...")

    # A. Standardize Dates (handles mixed formats like 2023-01-15 and 01/16/2023)
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    # B. Split 'product_info' into two columns: 'category' and 'product'
    # 'Electronics|Laptop' -> 'Electronics', 'Laptop'
    df[['category', 'product']] = df['product_info'].str.split('|', expand=True)

    # C. Handle Missing Values (Imputation)
    df['customer_name'] = df['customer_name'].fillna('Guest Customer')
    
    # D. Clean Numeric Columns
    # Convert quantity/price to numeric; 'invalid' strings become NaN
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    
    # Fill missing prices with the median price of the dataset
    median_price = df['unit_price'].median()
    df['unit_price'] = df['unit_price'].fillna(median_price)

    # E. Normalize Text (Region)
    # Changes 'SOUTH', 'south', 'South' all to 'South'
    df['region'] = df['region'].str.strip().str.capitalize()

    # F. Feature Engineering (Calculated Column)
    df['total_sales'] = df['quantity'] * df['unit_price']

    # G. Cleanup: Remove duplicates and drop the old messy column
    df.drop_duplicates(subset=['order_id'], keep='first', inplace=True)
    df.drop(columns=['product_info'], inplace=True)

    # --- 3. LOAD ---
    OUTPUT_FILE = 'cleaned_data.csv'
    df.to_csv(OUTPUT_FILE, index=False)
    
    print("-" * 30)
    print(f"SUCCESS: Cleaned data saved to {OUTPUT_FILE}")
    print(df.head())