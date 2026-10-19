import sys
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('channel_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

lockups = []

def find_lockups(obj):
    if isinstance(obj, dict):
        if 'lockupViewModel' in obj:
            lockups.append(obj['lockupViewModel'])
        for v in obj.values():
            find_lockups(v)
    elif isinstance(obj, list):
        for item in obj:
            find_lockups(item)

find_lockups(data)
print(f"Total lockups found: {len(lockups)}")

parsed_videos = []
for l in lockups:
    # contentId or identifier
    content_id = l.get('contentId', '')
    # metadata
    meta = l.get('metadata', {}).get('lockupMetadataViewModel', {})
    title = meta.get('title', {}).get('content', '')
    # metadata rows
    metadata_rows = meta.get('metadata', {}).get('contentMetadataViewModel', {}).get('metadataRows', [])
    meta_texts = []
    for row in metadata_rows:
        parts = row.get('metadataParts', [])
        for p in parts:
            text = p.get('text', {}).get('content', '')
            if text:
                meta_texts.append(text)
    
    parsed_videos.append({
        'content_id': content_id,
        'title': title,
        'metadata': " | ".join(meta_texts),
        'url': f"https://www.youtube.com/watch?v={content_id}"
    })

for i, pv in enumerate(parsed_videos, 1):
    print(f"{i}. [{pv['content_id']}] {pv['title']} ({pv['metadata']})")

with open('steve_w5g_videos.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_videos, f, ensure_ascii=False, indent=2)

print("\nSaved to steve_w5g_videos.json successfully!")
