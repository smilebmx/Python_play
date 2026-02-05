import sys
import logging
import os
import pyodbc
import pandas as pd
from sqlalchemy import create_engine
import urllib
# all this part till line 40 is for logging setup


# Get log file path from PowerShell argument (or fallback)
if len(sys.argv) > 1:
    log_file = sys.argv[1]
else:
    # fallback for manual run
    log_file = os.path.join(os.path.dirname(__file__), "logs", "python_fallback.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

# --- Setup logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | PYTHON | %(levelname)s | %(message)s",
    filename=log_file,
    encoding="utf-8",
    force=True
)

# --- Tee stdout and stderr to both console and log file ---
class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    def flush(self):
        for f in self.files:
            f.flush()

sys.stdout = Tee(sys.stdout, open(log_file, "a", encoding="utf-8"))
sys.stderr = Tee(sys.stderr, open(log_file, "a", encoding="utf-8"))

# --- Now everything will print and log ---
print("Python script started")
#logging.info("Logging initialized") #logging information

# Connection string
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ROSTYSLAV;"
    "DATABASE=TEST;"
    "Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
print("Connecting to database...")
# Create connection
conn = pyodbc.connect(connection_string)
print("Connection established.")
query = """
Select * from test.sales_data
"""

# Load SQL query directly into pandas
df = pd.read_sql(query, engine)
print("Data loaded into DataFrame.")
conn.close()

#print(df.head())
#print(df.tail())
#print(df.shape)
#print(df.columns)
#print(df.info()) # all columns with types
#print("Output is ready")
#print(df.columns)


sum_sales = df["SALES"].sum()

# Close connection


sum_sales_group = df.groupby("COUNTRY")["SALES"].sum().sort_values(ascending=False)
monthly_sales = (
    df.groupby(["YEAR_ID", "MONTH_ID"])["SALES"]
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)
"""
kpis = {
    "total_sales": df["SALES"].sum(),
    "avg_order_value": df["SALES"].mean(),
    "orders_count": df["ORDERNUMBER"].nunique(),
    "customers_count": df["CUSTOMERNAME"].nunique()
}

kpis
"""
path = r"C:\Users\perep\OneDrive\Desktop\Test\Output\tableau_export.csv"
tableau_df = (
    df.groupby(["YEAR_ID", "MONTH_ID", "COUNTRY"])
      .agg(total_sales=("SALES", "sum"))
      .reset_index()
)

print(f"Saving file to: {path}")

tableau_df.to_csv(path, index=False)
print(f"File saved (replaced if existed): {path}")
# transformations...
logging.info("Output file created")
print("new Branch test")
print("new Branch test")



#print(sum_sales)  
#print(sum_sales_group)  
#print(monthly_sales)

