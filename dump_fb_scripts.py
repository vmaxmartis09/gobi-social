import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\HAI\.gemini\antigravity\brain\a13db4d9-bb82-4f31-9f51-98a691a0994e\.system_generated\steps\24\content.md', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)

with open('script_39.txt', 'w', encoding='utf-8') as f:
    f.write(scripts[39])

with open('script_49.txt', 'w', encoding='utf-8') as f:
    f.write(scripts[49])

with open('script_61.txt', 'w', encoding='utf-8') as f:
    f.write(scripts[61])

print('Saved scripts 39, 49, 61.')
