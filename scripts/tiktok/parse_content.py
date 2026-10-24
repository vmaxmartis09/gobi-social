import sys
import json
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Input file path specified via sys.argv[1] or environment
import sys, os
target_path = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
if not os.path.exists(target_path):
    print(f'Input file not found: {target_path}. Provide input path as first argument.')
    sys.exit(0)
with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', text)
if m:
    data = json.loads(m.group(1))
    vd = data.get('__DEFAULT_SCOPE__', {}).get('webapp.video-detail', {})
    print("STATUS:", vd.get("statusCode"))
    print("SHARE_META:", json.dumps(vd.get("shareMeta"), ensure_ascii=False, indent=2))
    item = vd.get("itemInfo", {}).get("itemStruct", {})
    print("DESC:", item.get("desc"))
    print("AUTHOR:", item.get("author"))
    print("MUSIC:", item.get("music"))
    print("VIDEO_DUR:", item.get("video", {}).get("duration"))
    print("RATIO:", item.get("video", {}).get("ratio"))
    print("PLAY_ADDR:", item.get("video", {}).get("playAddr"))
    print("DOWNLOAD_ADDR:", item.get("video", {}).get("downloadAddr"))
    print("COVER:", item.get("video", {}).get("cover"))
    print("STATS:", item.get("stats"))
    print("CONTENTS:", item.get("contents"))
    print("CHALLENGES:", [c.get("title") for c in item.get("challenges", [])])
    
    # Save the video URL or download it to examine
    download_url = item.get("video", {}).get("playAddr") or item.get("video", {}).get("downloadAddr")
    with open("shots/ber_video_meta.json", "w", encoding="utf-8") as out:
        json.dump(item, out, ensure_ascii=False, indent=2)
    print("Saved metadata to shots/ber_video_meta.json")
