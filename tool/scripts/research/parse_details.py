import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("data/raw/youtube/found_script.json", "r", encoding="utf-8") as f:
    text = f.read()

data = json.loads(text)

def search_dict(d):
    results = {}
    if isinstance(d, dict):
        if "desc" in d and "id" in d and str(d.get("id")) == "7634957602555792647":
            return d
        for k, v in d.items():
            res = search_dict(v)
            if res:
                return res
    elif isinstance(d, list):
        for item in d:
            res = search_dict(item)
            if res:
                return res
    return None

item = search_dict(data)
if item:
    print("=== VIDEO INFO ===")
    print("ID:", item.get("id"))
    print("Desc:", item.get("desc"))
    print("Author:", item.get("author", {}).get("nickname"), "(@", item.get("author", {}).get("uniqueId"), ")")
    print("Author Sig:", item.get("author", {}).get("signature"))
    print("Music:", item.get("music", {}).get("title"), "-", item.get("music", {}).get("authorName"))
    print("Stats:", item.get("stats"))
    print("Challenges / Tags:", [c.get("title") for c in item.get("challenges", [])])
    print("Video PlayAddr:", item.get("video", {}).get("playAddr"))
    print("Video Cover:", item.get("video", {}).get("cover"))
    with open("data/raw/youtube/video_details.json", "w", encoding="utf-8") as out:
        json.dump(item, out, ensure_ascii=False, indent=2)
else:
    print("Item not found directly, dumping top keys:")
    print(list(data.keys()) if isinstance(data, dict) else len(data))
    with open("raw_script.json", "w", encoding="utf-8") as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
