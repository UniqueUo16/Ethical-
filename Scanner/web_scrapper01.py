import requests
from bs4 import BeautifulSoup

url = 'https://Facebook.com'

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Extract and print clean text from all paragraphs
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        text = p.get_text().strip()
        if text:
            print(text)
            
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')  # Get the href attribute (the URL)
        text = link.text.strip()  # Get the visible text of the link
        if href:
            print(f'~{text}:{href}')
else:
    print(f'Failed to retrieve page: {response.status_code}')

