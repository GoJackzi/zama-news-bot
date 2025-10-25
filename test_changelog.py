"""
Quick test to see what the changelog structure looks like
"""
import requests
from bs4 import BeautifulSoup

url = "https://docs.zama.ai/change-log"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

response = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the main content area
main = soup.find('main') or soup.find('article') or soup.find('div', class_='content')

if main:
    # Look for headings
    headings = main.find_all(['h2', 'h3'], limit=3)
    
    for i, heading in enumerate(headings):
        print(f"\n{'='*60}")
        print(f"HEADING {i+1}: {heading.get_text(strip=True)}")
        print(f"Tag: {heading.name}")
        print(f"{'='*60}\n")
        
        # Get the next few siblings
        print("SIBLINGS:")
        sibling = heading.find_next_sibling()
        count = 0
        while sibling and count < 5:
            print(f"\n  Tag: {sibling.name}")
            print(f"  Classes: {sibling.get('class', [])}")
            print(f"  Text preview: {sibling.get_text(strip=True)[:100]}")
            
            # Check for lists
            if sibling.name in ['ul', 'ol']:
                items = sibling.find_all('li')
                print(f"  List items: {len(items)}")
                for li in items[:2]:
                    print(f"    - {li.get_text(strip=True)[:60]}")
            
            sibling = sibling.find_next_sibling()
            if sibling and sibling.name in ['h1', 'h2', 'h3']:
                break
            count += 1
        
        print()

else:
    print("Could not find main content area")


