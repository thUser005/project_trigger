import json
import time
import schedule
from trigger_action import trigger_github_action

JOBS_FILE = "jobs_data.json"

def load_jobs():
    with open(JOBS_FILE, encoding="utf-8") as f:
        return json.load(f)

def register_jobs():
    jobs = load_jobs()

    for job in jobs:
        run_time = job.pop("time")  # remove time from payload

        schedule.every().day.at(run_time).do(
            trigger_github_action, **job
        )

        print(f"⏰ Scheduled {job['repo']} → {job['workflow']} at {run_time}")

if __name__ == "__main__":
    print("🚀 GitHub Action Scheduler Started")
    register_jobs()

    while True:
        schedule.run_pending()
        time.sleep(1)
