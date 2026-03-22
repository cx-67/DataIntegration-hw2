
import json
import os
import subprocess
import time

# Configuration
old_job_file = r'e:\Grade3\2-DataIntegration\Assignments-DI\As2\datax\job\mysql2mysql_7-10_full.json'

# Use correct path to datax.py - based on your environment this might need adjustment
# Assuming default installation under specific path or try to locate it
datax_bin = r'D:\datax\bin\datax.py' # Adjust if necessary
python_cmd = 'python'

# Step 1: Skip automatic table clearing via Python to avoid connection issues.
# DataX jobs now include "preSql": ["DELETE FROM table"] to handle cleanup themselves.

# Step 2: Run DataX Jobs
print("Step 2: Starting DataX jobs (7 tables) with built-in cleanup...")

# Check if datax file exists
if not os.path.exists(datax_bin):
    print(f"Error: DataX binary not found at {datax_bin}")
    exit(1)

# Read the full JSON
print(f"Reading job config from: {old_job_file}")
try:
    with open(old_job_file, 'r', encoding='utf-8') as f:
        job_config = json.load(f)
except FileNotFoundError:
    print(f"Error: Job file not found: {old_job_file}")
    exit(1)

content_list = job_config['job']['content']
setting = job_config['job']['setting']

# Iterate and run each job
for i, content in enumerate(content_list):
    # Extract table name for filename
    try:
        table_name = content['writer']['parameter']['connection'][0]['table'][0]
    except:
        table_name = f'job_{i}'
    
    print(f"\n[JOB {i+1}/{len(content_list)}] Preparing job for table: {table_name}")
    
    # Force TRUNCATE instead of DELETE for performance
    try:
        if 'preSql' in content['writer']['parameter']:
            content['writer']['parameter']['preSql'] = [
                sql.replace('DELETE FROM', 'TRUNCATE TABLE') 
                for sql in content['writer']['parameter']['preSql']
            ]
            print(f" Modified preSql to TRUNCATE for {table_name}")
    except Exception as e:
        print(f" Warning: Could not modify preSql: {e}")

    # Create single job config
    single_job = {
        "job": {
            "content": [content],
            "setting": setting
        }
    }
    
    # Save to temp file
    temp_job_file = f'e:\\Grade3\\2-DataIntegration\\Assignments-DI\\As2\\datax\\job\\temp_{table_name}_7_10.json'
    with open(temp_job_file, 'w', encoding='utf-8') as f:
        json.dump(single_job, f, indent=4)
        
    print(f" Running DataX for {table_name}...")
    start_time = time.time()
    
    # Run DataX
    cmd = [python_cmd, datax_bin, temp_job_file]
    
    try:
        # Run and capture output
        # Use errors='replace' to prevent encoding crashes
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(f" Job for {table_name} COMPLETED successfully.")
            # Print last few lines of output
            print(" Output snippet:")
            print('\n'.join(stdout.splitlines()[-5:]))
        else:
            print(f" Job for {table_name} FAILED with return code {process.returncode}.")
            print(" Error output:")
            print(stderr)
            print(" Stdout snippet:")
            print('\n'.join(stdout.splitlines()[-10:]))
            print(" FAILED DETAILED LOG START:")
            print(stdout[:2000])
            print(" FAILED DETAILED LOG END:")
            break
            
    except Exception as e:
        print(f" An error occurred executing DataX: {e}")
    
    end_time = time.time()
    print(f" Duration: {end_time - start_time:.2f} seconds")
    
    # Clean up temp file
    if os.path.exists(temp_job_file):
        try:
            os.remove(temp_job_file)
        except:
            pass

print("\nAll jobs execution attempted.")
