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
    html = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"Total script tags: {len(scripts)}")

texts_found = set()

def extract_strings(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ['text', 'message', 'story', 'description', 'caption', 'title', 'subtitle'] and isinstance(v, str):
                if len(v.strip()) > 15:
                    texts_found.add(v.strip())
            elif k == 'message' and isinstance(v, dict) and 'text' in v:
                texts_found.add(v['text'].strip())
            else:
                extract_strings(v)
    elif isinstance(obj, list):
        for item in obj:
            extract_strings(item)

for i, s in enumerate(scripts):
    s = s.strip()
    if not s:
        continue
    try:
        data = json.loads(s)
        extract_strings(data)
    except:
        pass

print(f"Extracted unique text segments from SSR scripts: {len(texts_found)}")
with open('data/raw/facebook/extracted_texts.txt', 'w', encoding='utf-8') as out:
    for t in sorted(texts_found, key=lambda x: len(x), reverse=True):
        out.write(f"--- [LEN {len(t)}] ---\n{t}\n\n")

print("Saved to data/raw/facebook/extracted_texts.txt")
