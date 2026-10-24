import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('data/raw/youtube/video_details.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for vid, item in data.items():
    print("=" * 60)
    print(f"VIDEO: {item['title']} ({vid})")
    print(f"URL: {item['url']}")
    print("DESCRIPTION:")
    print(item['description'])
    print()
