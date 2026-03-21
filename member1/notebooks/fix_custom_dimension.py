
import pandas as pd
from sqlalchemy import create_engine
import subprocess

# Database connection
db_connection_str = 'mysql+pymysql://datax:DxPwd123!@BPeril:3306/DIDatax'
engine = create_engine(db_connection_str)

# 1. Drop table
print("Dropping ga_custom_dimension...")
with engine.connect() as conn:
    conn.execute("DROP TABLE IF EXISTS ga_custom_dimension")
    print("Table dropped.")

# 2. Create table
create_sql = """
CREATE TABLE ga_custom_dimension (
    uid VARCHAR(255),
    visit_id VARCHAR(255),
    dim_index INT,
    value VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
print("Creating ga_custom_dimension...")
with engine.connect() as conn:
    conn.execute(create_sql)
    print("Table created.")

import json

# 3. Create modified DataX job (removing visit_id)
print("Creating corrected job configuration...")
full_job_path = r'e:\Grade3\2-DataIntegration\Assignments-DI\As2\datax\job\mysql2mysql_2-5_full.json'
with open(full_job_path, 'r', encoding='utf-8') as f:
    job_config = json.load(f)

# Extract content for ga_custom_dimension (index 1)
content = job_config['job']['content'][1]
setting = job_config['job']['setting']

# Modify Reader Query (Remove visit_id)
reader_conn = content['reader']['parameter']['connection'][0]
original_query = reader_conn['querySql'][0]
# Use replace to remove visit_id safely
new_query = original_query.replace("uid, visit_id, `index`, value", "uid, `index`, value")
reader_conn['querySql'] = [new_query]

# Modify Writer Columns (Remove visit_id)
writer_param = content['writer']['parameter']
if "visit_id" in writer_param['column']:
    writer_param['column'].remove("visit_id")

single_job = {
    "job": {
        "content": [content],
        "setting": setting
    }
}

job_file = r'e:\Grade3\2-DataIntegration\Assignments-DI\As2\datax\job\temp_ga_custom_dimension_fixed.json'
with open(job_file, 'w', encoding='utf-8') as f:
    json.dump(single_job, f, indent=4)

# 4. Run DataX job
datax_bin = r'D:\datax\bin\datax.py'
cmd = ['python', datax_bin, job_file]

print("Running DataX for ga_custom_dimension (FIXED)...")
try:
    # Capture output for debugging
    result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    print("DataX job completed successfully.")
    print(result.stdout[-1000:]) # Print last 1000 chars of output
except subprocess.CalledProcessError as e:
    print("DataX job failed.")
    print(f"Error output snippet:\n{e.output[-2000:] if e.output else 'No output captured'}")
except Exception as e:
    print(f"An error occurred: {e}")
