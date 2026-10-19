import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

# Input file path specified via sys.argv[1] or environment
import sys, os
target_path = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
if not os.path.exists(target_path):
    print(f'Input file not found: {target_path}. Provide input path as first argument.')
    sys.exit(0)
with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)

with open('script_39.txt', 'w', encoding='utf-8') as f:
    f.write(scripts[39])

with open('script_49.txt', 'w', encoding='utf-8') as f:
    f.write(scripts[49])

with open('script_61.txt', 'w', encoding='utf-8') as f:
    f.write(scripts[61])

print('Saved scripts 39, 49, 61.')
