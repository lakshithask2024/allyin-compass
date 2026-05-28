import pandas as pd
import duckdb
import os

# Define CSV files and table names
csv_files = {
    'customers.csv': 'customers',
    'orders.csv': 'orders',
    'emissions.csv': 'emissions'
}

# Base path
base_path = 'data/structured'

# Load each CSV file into DuckDB
for file, table in csv_files.items():
    full_path = os.path.join(base_path, file)
    if os.path.exists(full_path):
        print(f"Loading {file} into DuckDB table: {table}")
        df = pd.read_csv(full_path)
        duckdb.sql(f"CREATE TABLE {table} AS SELECT * FROM df")
    else:
        print(f"❌ Missing file: {file}")

# Verify by querying the customers table
print("\n📊 Sample from customers:")
print(duckdb.sql("SELECT * FROM customers LIMIT 10").df())
