import json

with open('data/raw/youtube/channel_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find all text and titles across data
def find_all_text(obj, results):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ['title', 'simpleText', 'text'] and isinstance(v, str):
                results.append((k, v))
            elif k in ['title', 'text'] and isinstance(v, dict):
                find_all_text(v, results)
            elif k == 'runs' and isinstance(v, list):
                for item in v:
                    if isinstance(item, dict) and 'text' in item:
                        results.append(('runs.text', item['text']))
            else:
                find_all_text(v, results)
    elif isinstance(obj, list):
        for item in obj:
            find_all_text(item, results)

# Find videoIds or commandMetadata
def find_video_ids(obj, ids):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'videoId' and isinstance(v, str):
                ids.append(v)
            elif k == 'urlEndpoint' and isinstance(v, dict):
                url = v.get('url', '')
                if '/watch?v=' in url or '/shorts/' in url:
                    ids.append(url)
            else:
                find_video_ids(v, ids)
    elif isinstance(obj, list):
        for item in obj:
            find_video_ids(item, ids)

ids = []
find_video_ids(data, ids)
print("Video IDs / URLs found:", len(ids), set(ids))

# Also print channel header metadata
header = data.get('header', {})
print("Header keys:", list(header.keys()))
microformat = data.get('microformat', {})
print("Microformat:", json.dumps(microformat, ensure_ascii=False)[:300])
