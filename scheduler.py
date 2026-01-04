import json
import time
import schedule
from trigger_action import trigger_github_action

# =========================
# CONFIG
# =========================
JOBS_FILE = "jobs_data.json"

TESTING_FLAG = True   # 🔁 set False in production

# =========================
# LOAD JOBS
# =========================
def load_jobs():
    with open(JOBS_FILE, encoding="utf-8") as f:
        return json.load(f)

# =========================
# REGISTER JOBS
# =========================
def register_jobs():
    jobs = load_jobs()

    if TESTING_FLAG:
        print("🧪 TEST MODE ENABLED → triggering all jobs immediately\n")

        for job in jobs:
            job_copy = job.copy()
            job_copy.pop("time", None)

            print(f"⚡ Triggering {job_copy['repo']} → {job_copy['workflow']}")
            trigger_github_action(**job_copy)

        print("\n✅ Test run completed")
        return

    # -------------------------
    # NORMAL SCHEDULE MODE
    # -------------------------
    for job in jobs:
        run_time = job["time"]

        job_copy = job.copy()
        job_copy.pop("time")

        schedule.every().day.at(run_time).do(
            trigger_github_action, **job_copy
        )

        print(f"⏰ Scheduled {job_copy['repo']} → {job_copy['workflow']} at {run_time}")

# =========================
# MAIN LOOP
# =========================
if __name__ == "__main__":
    print("🚀 GitHub Action Scheduler Started")
    register_jobs()

    if TESTING_FLAG:
        # 🚫 do not block container in test mode
        exit(0)

    while True:
        schedule.run_pending()
        time.sleep(1)
