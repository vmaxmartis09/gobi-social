import re
import json

# Input file path specified via sys.argv[1] or environment
import sys, os
target_path = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
if not os.path.exists(target_path):
    print(f'Input file not found: {target_path}. Provide input path as first argument.')
    sys.exit(0)
with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

print("HTML length:", len(html))

metas = re.findall(r'<meta[^>]+>', html)
for m in metas:
    if any(k in m for k in ['description', 'og:title', 'og:description', 'og:video', 'twitter:']):
        print("META:", m)

matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"Total script tags: {len(matches)}")
for idx, s in enumerate(matches):
    if "7634957602555792647" in s:
        print(f"Found video ID in script {idx} (len: {len(s)})")
        with open("found_script.json", "w", encoding="utf-8") as out:
            out.write(s)
        break
