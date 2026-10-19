import re
import json

path = r"C:\Users\HAI\.gemini\antigravity\brain\e2ae0d54-6ee5-467b-a6bc-af20d8fb67a4\.system_generated\steps\2\content.md"
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
