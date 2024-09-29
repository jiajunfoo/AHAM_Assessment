import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# Step 1: Read from SQLite database
sqlite_conn = sqlite3.connect('fund.db')
df = pd.read_sql_query("SELECT * FROM InvestmentFund", sqlite_conn)

# Step 2: Connect to the MySQL database
mysql_engine = create_engine('mysql+pymysql://username:password@host/dbname')

# Step 3: Write to the MySQL database
df.to_sql('InvestmentFund', mysql_engine, if_exists='replace', index=False)
