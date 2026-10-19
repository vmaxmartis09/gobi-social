import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\HAI\.gemini\antigravity\brain\a13db4d9-bb82-4f31-9f51-98a691a0994e\.system_generated\steps\24\content.md', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

urls = re.findall(r'https?://[^\s\"\'<>]+', text)
unique_urls = set()
for u in urls:
    u_clean = u.rstrip('\\').rstrip('"').rstrip("'")
    if any(k in u_clean.lower() for k in ['youtube', 'tiktok', 'w5g', 'ngc.chu', 'martech', 'tinhtruong', 'koc']):
        unique_urls.add(u_clean)

print("Special URLs found:")
for u in unique_urls:
    print(u)
