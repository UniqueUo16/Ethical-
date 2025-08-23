import requests

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

base_url = "http://0.0.0.0:8080/"

with open("wordlist.txt") as f:
    for word in f:
        word = word.strip()
        url = f"{base_url}/{word}"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print(f"{GREEN}[FOUND]{RESET} {url}")
            elif r.status_code in (301, 302):
                print(f"{YELLOW}[REDIRECT]{RESET} {url} -> {r.headers.get('Location', '')}")
            else:
                print(f"{RED}[NOT FOUND]{RESET} {url}")
        except requests.RequestException as e:
            print(f"{RED}[ERROR]{RESET} {url} ({e})")


