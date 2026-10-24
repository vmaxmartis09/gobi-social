import json

with open('data/raw/youtube/channel_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

videos = []

def find_video_renderers(obj):
    if isinstance(obj, dict):
        if 'videoRenderer' in obj:
            vr = obj['videoRenderer']
            vid = vr.get('videoId')
            title = ""
            if 'title' in vr:
                runs = vr['title'].get('runs', [])
                if runs:
                    title = "".join(r.get('text', '') for r in runs)
                else:
                    title = vr['title'].get('simpleText', '')
            view_count = vr.get('viewCountText', {}).get('simpleText', '')
            published = vr.get('publishedTimeText', {}).get('simpleText', '')
            length = vr.get('lengthText', {}).get('simpleText', '')
            videos.append({'id': vid, 'title': title, 'views': view_count, 'published': published, 'length': length})
        elif 'richItemRenderer' in obj:
            find_video_renderers(obj['richItemRenderer'])
        else:
            for k, v in obj.items():
                find_video_renderers(v)
    elif isinstance(obj, list):
        for item in obj:
            find_video_renderers(item)

find_video_renderers(data)
print(f"Total videos found: {len(videos)}")
seen = set()
unique_videos = []
for v in videos:
    if v['id'] and v['id'] not in seen:
        seen.add(v['id'])
        unique_videos.append(v)

print(f"Unique videos: {len(unique_videos)}")
for i, v in enumerate(unique_videos, 1):
    print(f"{i}. [{v['id']}] {v['title']} ({v['length']}, {v['published']})")

with open('data/raw/youtube/unique_videos.json', 'w', encoding='utf-8') as f:
    json.dump(unique_videos, f, ensure_ascii=False, indent=2)
