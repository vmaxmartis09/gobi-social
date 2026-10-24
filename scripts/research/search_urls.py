import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Input file path specified via sys.argv[1] or environment
import sys, os
target_path = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
if not os.path.exists(target_path):
    print(f'Input file not found: {target_path}. Provide input path as first argument.')
    sys.exit(0)
with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
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
