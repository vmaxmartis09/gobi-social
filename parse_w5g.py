import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

# Input file path specified via sys.argv[1] or environment
import sys, os
target_path = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
if not os.path.exists(target_path):
    print(f'Input file not found: {target_path}. Provide input path as first argument.')
    sys.exit(0)
with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Title:", soup.title.string if soup.title else '')

# Extract all headings (h1, h2, h3, h4)
headings = []
for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5']):
    txt = h.get_text(strip=True)
    if txt and txt not in headings:
        headings.append(f"<{h.name}> {txt}")

print(f"Total headings: {len(headings)}")

# Extract courses or products or blog posts
items = []
for item in soup.find_all(['article', 'div'], class_=lambda c: c and any(k in str(c) for k in ['course', 'product', 'post-item', 'box-text'])):
    txt = item.get_text(separator=' | ', strip=True)
    if len(txt) > 30 and txt not in items:
        items.append(txt)

print(f"Total featured items: {len(items)}")

with open('w5g_extracted.txt', 'w', encoding='utf-8') as out:
    out.write("=== HEADINGS ===\n")
    for h in headings:
        out.write(h + "\n")
    out.write("\n=== FEATURED ITEMS & COURSES ===\n")
    for it in items[:50]:
        out.write(it + "\n---\n")

print("Saved to w5g_extracted.txt")
