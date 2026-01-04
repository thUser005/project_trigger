from mongo_tokens import get_token
import requests
import os

def trigger_github_action(repo, workflow, ref):
    token = get_token("PAT_TOKEN")
    owner = os.getenv("GITHUB_OWNER")

    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "ref": ref
    }

    r = requests.post(url, headers=headers, json=payload)

    if r.status_code == 204:
        print(f"✅ Triggered {repo}/{workflow}")
    else:
        print(f"❌ Failed {repo}: {r.status_code} {r.text}")
