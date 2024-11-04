import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('yokatlas.db')

# Get the list of all tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Loop through each table and export to CSV
for table_name in tables:
    table_name = table_name[0]  # Extract table name from tuple
    data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    data.to_csv(f"{table_name}.csv", index=False)  # Export each table to CSV

# Close the connection
conn.close()