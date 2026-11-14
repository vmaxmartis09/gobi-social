import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Input file path specified via sys.argv[1] or environment
import sys, os
target_path = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
if not os.path.exists(target_path):
    print(f'Input file not found: {target_path}. Provide input path as first argument.')
    sys.exit(0)
with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

clean = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
clean = re.sub(r'<[^>]+>', '\n', clean)
lines = [l.strip() for l in clean.split('\n') if l.strip()]

with open('data/raw/web/article_content_clean.txt', 'w', encoding='utf-8') as out:
    for l in lines:
        out.write(l + '\n')

print("Saved clean content to data/raw/web/article_content_clean.txt! Total lines:", len(lines))
