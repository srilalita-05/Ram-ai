import requests
from bs4 import BeautifulSoup

# Fetch one page
url = "https://valmikiramayan.net/utf8/baala/sarga1/bala_1_frame.htm"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

# Find all paragraphs
paragraphs = soup.find_all('p')
print(f"Total <p> tags found: {len(paragraphs)}\n")

# Print first 15 paragraphs with their classes
print("First 15 paragraphs and their classes:")
for i, p in enumerate(paragraphs[:15]):
    classes = p.get('class', [])
    text = p.get_text(strip=True)[:60]  # First 60 chars
    print(f"{i}: class={classes} | text='{text}...'")

print("\n\nAll unique classes found:")
all_classes = set()
for p in paragraphs:
    classes = p.get('class', [])
    if classes:
        all_classes.add(classes[0] if isinstance(classes, list) else classes)
print(all_classes)