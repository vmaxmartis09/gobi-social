import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

# Input file path specified via sys.argv[1] or environment
import sys, os
target_path = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
if not os.path.exists(target_path):
    print(f'Input file not found: {target_path}. Provide input path as first argument.')
    sys.exit(0)
with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
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
