
import pandas as pd
from sqlalchemy import create_engine

# Database connection
db_connection_str = 'mysql+pymysql://datax:DxPwd123!@BPeril:3306/DIDatax'
engine = create_engine(db_connection_str)

query = "DESCRIBE ga_custom_dimension"
try:
    df = pd.read_sql(query, engine)
    print("Schema for ga_custom_dimension:")
    print(df)
except Exception as e:
    print(e)
