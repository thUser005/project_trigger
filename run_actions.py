from trigger_action import trigger_github_action
import os,json
file_name = "jobs_data.json"
if os.path.exists(file_name):
    with open(file_name,encoding='utf-8')as f:
        jobs = json.load(f)

for job in jobs:
    trigger_github_action(**job)
