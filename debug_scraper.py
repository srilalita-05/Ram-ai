import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Fetch the frame page
url = "https://valmikiramayan.net/utf8/baala/sarga1/bala_1_frame.htm"
print(f"Fetching: {url}\n")
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

# Find all frame references
frames = soup.find_all('frame')
print(f"Found {len(frames)} frame(s):\n")

for i, frame in enumerate(frames):
    src = frame.get('src', 'NO SRC')
    name = frame.get('name', 'NO NAME')
    print(f"Frame {i}: name='{name}' src='{src}'")
    
    # Construct full URL
    if src and src != 'NO SRC':
        full_url = urljoin(url, src)
        print(f"  Full URL: {full_url}")
        
        # Fetch the actual content frame
        print(f"\n  Fetching actual content...")
        content_response = requests.get(full_url)
        content_soup = BeautifulSoup(content_response.text, 'html.parser')
        paragraphs = content_soup.find_all('p')
        print(f"  Found {len(paragraphs)} <p> tags in this frame")
        
        # Print first 10
        print(f"\n  First 10 paragraphs:")
        for j, p in enumerate(paragraphs[:10]):
            classes = p.get('class', [])
            text = p.get_text(strip=True)[:50]
            print(f"    {j}: class={classes} | text='{text}...'")