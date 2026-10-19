import sys
import json
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

path = r"C:\Users\HAI\.gemini\antigravity\brain\383fa778-c3ea-408f-bf80-315f12e6d6f3\.system_generated\steps\837\content.md"
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
