
import pandas as pd
from sqlalchemy import create_engine

# Database connection string
db_connection_str = 'mysql+pymysql://datax:DxPwd123!@BPeril:3306/DIDatax'
db_connection = create_engine(db_connection_str)

tables = [
    'ga_session',
    'ga_custom_dimension',
    'ga_hit',
    'ga_total',
    'ga_geo_network',
    'ga_traffic_source',
    'ga_device'
]

print("Checking row counts for tables...")
for table in tables:
    try:
        query = f"SELECT count(*) as count FROM {table}"
        df = pd.read_sql(query, db_connection)
        print(f"{table}: {df['count'].iloc[0]}")
    except Exception as e:
        print(f"{table}: Error - {e}")
