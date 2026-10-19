import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\HAI\.gemini\antigravity\brain\a13db4d9-bb82-4f31-9f51-98a691a0994e\.system_generated\steps\24\content.md', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')
print('Title:', soup.title.string if soup.title else 'No title')

body_text = soup.get_text(separator='\n', strip=True)
lines = [l.strip() for l in body_text.split('\n') if l.strip()]
print(f'Total non-empty lines: {len(lines)}')

with open('fb_extracted_lines.txt', 'w', encoding='utf-8') as out:
    for l in lines:
        out.write(l + '\n')

print('First 30 lines written to fb_extracted_lines.txt')
