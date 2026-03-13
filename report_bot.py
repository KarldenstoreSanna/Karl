import requests
import time
import sys
import os

# --- CONFIGURATION ---
# Replace with your actual website API URL (e.g., https://api.yourdomain.com)
BASE_URL = "https://your-website-domain.com/api/v1" 
REPORT_ENDPOINT = f"{BASE_URL}/report/content"

def send_spam_report(auth_token, target_id, reason_code=0):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "User-Agent": "GitHub-Moderator-Bot/1.0"
    }
    
    # Payload matches TikTok-style architecture
    payload = {
        "target_id": str(target_id),
        "reason": int(reason_code),
        "type": "user" 
    }

    try:
        response = requests.post(REPORT_ENDPOINT, json=payload, headers=headers, timeout=10)
        if response.status_code in [200, 201]:
            print(f"[SUCCESS] Reported ID: {target_id}")
        else:
            print(f"[FAILED] Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")

if __name__ == "__main__":
    # Get the Moderator Token from GitHub Secrets
    token = os.getenv("MOD_TOKEN")
    
    if not token:
        print("ERROR: MOD_TOKEN secret is missing in GitHub Settings.")
        sys.exit(1)

    # Get inputs from the GitHub Action workflow
    if len(sys.argv) < 3:
        print("ERROR: Usage: python report_bot.py <target_id> <count>")
        sys.exit(1)

    target_id_input = sys.argv[1]
    report_count = int(sys.argv[2])

    print(f"--- Launching Report Task for: {target_id_input} ---")
    
    for i in range(report_count):
        print(f"Sending report {i+1} of {report_count}...")
        send_spam_report(token, target_id_input)
        # Sleep prevents your server from blocking the GitHub IP
        time.sleep(2) 

    print("--- Task Finished ---")
