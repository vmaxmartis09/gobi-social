import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\HAI\.gemini\antigravity\brain\a13db4d9-bb82-4f31-9f51-98a691a0994e\.system_generated\steps\114\content.md', 'r', encoding='utf-8', errors='ignore') as f:
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
