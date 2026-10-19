import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'C:\Users\HAI\.gemini\antigravity\brain\f0653b66-ea39-4969-8458-d1570b145951\.system_generated\steps\49\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

clean = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'<[^>]+>', '\n', clean)
lines = [l.strip() for l in clean.split('\n') if l.strip()]

with open('article_content_clean.txt', 'w', encoding='utf-8') as out:
    for l in lines:
        out.write(l + '\n')

print("Saved clean content to article_content_clean.txt! Total lines:", len(lines))
