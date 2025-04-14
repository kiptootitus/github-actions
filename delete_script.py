import os
import requests

# === CONFIGURATION ===
OWNER = "kiptootitus"
REPO = "github-actions"
WORKFLOW_FILENAME = "schedule.yml"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # <-- Fixed by adding quotes

# === HEADERS ===
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# === STEP 1: Get Workflow ID ===
workflow_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILENAME}"
resp = requests.get(workflow_url, headers=headers)
workflow_id = resp.json().get("id")

if not workflow_id:
    print("❌ Could not retrieve workflow ID. Check filename and permissions.")
    exit()

# === STEP 2: Get Workflow Runs ===
runs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{workflow_id}/runs?per_page=100"
runs_resp = requests.get(runs_url, headers=headers)
runs = runs_resp.json().get("workflow_runs", [])

print(f"Found {len(runs)} runs to delete.")

# === STEP 3: Delete Each Run ===
for run in runs:
    run_id = run["id"]
    del_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}"
    del_resp = requests.delete(del_url, headers=headers)
    
    if del_resp.status_code == 204:
        print(f"✅ Deleted run ID: {run_id}")
    else:
        print(f"❌ Failed to delete run ID: {run_id} | Status: {del_resp.status_code}")
