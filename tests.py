import pandas as pd

# Load the cleaned data
df = pd.read_csv('cleaned_sales_data.csv')

def run_quality_checks(df):
    print("=== ETL DATA QUALITY REPORT ===")
    
    # 1. NULL CHECK: Ensure critical columns are populated
    nulls = df[['order_id', 'total_sales', 'category']].isnull().sum()
    print(f"\n[1] Null Value Check:\n{nulls}")
    
    # 2. SCHEMA CHECK: Ensure data types are correct
    print(f"\n[2] Data Type Check:\n{df.dtypes[['order_date', 'total_sales']]}")
    
    # 3. LOGIC CHECK: Are there any negative sales or quantities?
    outliers = df[(df['total_sales'] < 0) | (df['quantity'] < 0)]
    print(f"\n[3] Logical Error Check (Negative Values): {len(outliers)} rows found.")
    
    # 4. DUPLICATE CHECK: Ensure order_ids are unique
    duplicates = df['order_id'].duplicated().sum()
    print(f"\n[4] Duplicate Order IDs: {duplicates}")
    
    # 5. BUSINESS SUMMARY: Quick sanity check on the numbers
    print("\n[5] Financial Summary:")
    print(f"Total Revenue: ${df['total_sales'].sum():,.2f}")
    print(f"Avg Order Value: ${df['total_sales'].mean():,.2f}")
    print(f"Top Category: {df['category'].value_counts().idxmax()}")

run_quality_checks(df)