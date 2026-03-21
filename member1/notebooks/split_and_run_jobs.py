
import json
import os
import subprocess
import time

# Path to the full JSON file
full_job_path = r'e:\Grade3\2-DataIntegration\Assignments-DI\As2\datax\job\mysql2mysql_2-5_full.json'
datax_bin = r'D:\datax\bin\datax.py'
python_cmd = 'python'

# Read the full JSON
with open(full_job_path, 'r', encoding='utf-8') as f:
    job_config = json.load(f)

content_list = job_config['job']['content']
setting = job_config['job']['setting']

# Iterate and run each job
for i, content in enumerate(content_list):
    # Extract table name for filename
    # Usually in writer -> connection -> table[0]
    try:
        table_name = content['writer']['parameter']['connection'][0]['table'][0]
    except:
        table_name = f'job_{i}'
    
    print(f"Preparing job for table: {table_name}")
    
    if table_name == 'ga_session':
        print(f"Skipping {table_name} as it is already synchronized.")
        continue

    # Create single job config
    single_job = {
        "job": {
            "content": [content],
            "setting": setting
        }
    }
    
    # Save to temp file
    temp_job_file = f'e:\\Grade3\\2-DataIntegration\\Assignments-DI\\As2\\datax\\job\\temp_{table_name}.json'
    with open(temp_job_file, 'w', encoding='utf-8') as f:
        json.dump(single_job, f, indent=4)
        
    print(f"Running DataX for {table_name}...")
    start_time = time.time()
    
    # Run DataX
    # Using python to invoke datax.py
    cmd = [python_cmd, datax_bin, temp_job_file]
    
    try:
        # Run and capture output to verify success
        # Use errors='replace' to avoid encoding issues
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        print(f"Job for {table_name} completed successfully.")
        # print(result.stdout) # Uncomment for debugging
    except subprocess.CalledProcessError as e:
        print(f"Job for {table_name} FAILED.")
        # print(e.output) # Uncomment if detailed error needed
    except Exception as e:
        print(f"An error occurred: {e}")
    
    end_time = time.time()
    print(f"Duration: {end_time - start_time:.2f} seconds\n")
    
    # Clean up temp file (optional, keeping for inspection implies reliability)
    # os.remove(temp_job_file)

print("All jobs execution attempted.")
