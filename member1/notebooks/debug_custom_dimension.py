
import os
import sys

# Paths
datax_bin = r'D:\datax\bin\datax.py'
job_file = r'e:\Grade3\2-DataIntegration\Assignments-DI\As2\datax\job\temp_ga_custom_dimension.json'
python_cmd = 'python'

# Check if job file exists, if not, we must create it (by parsing full json again)
# For simplicity, let's assume it exists from previous run or recreate it
import json
if not os.path.exists(job_file):
    print("Recreating job file...")
    full_job_path = r'e:\Grade3\2-DataIntegration\Assignments-DI\As2\datax\job\mysql2mysql_2-5_full.json'
    with open(full_job_path, 'r', encoding='utf-8') as f:
        job_config = json.load(f)
    
    # Find custom dimension content
    content = job_config['job']['content'][1] # 2nd element
    setting = job_config['job']['setting']
    
    single_job = {
        "job": {
            "content": [content],
            "setting": setting
        }
    }
    
    with open(job_file, 'w', encoding='utf-8') as f:
        json.dump(single_job, f, indent=4)

print(f"Running DataX for ga_custom_dimension using {job_file}")
cmd = f'{python_cmd} {datax_bin} "{job_file}"'
os.system(cmd)
