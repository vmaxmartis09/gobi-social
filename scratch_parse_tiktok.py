import re
import json

# Input file path specified via sys.argv[1] or environment
import sys, os
target_path = sys.argv[1] if len(sys.argv) > 1 else 'sample_input.txt'
if not os.path.exists(target_path):
    print(f'Input file not found: {target_path}. Provide input path as first argument.')
    sys.exit(0)
with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:

with open(path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("File length:", len(text))

# Search for json-ld
lds = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
print(f"Found {len(lds)} ld+json blocks")
for i, ld in enumerate(lds):
    print(f"--- ld+json #{i} ---")
    try:
        data = json.loads(ld)
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
    except Exception as e:
        print("Error parsing json:", e)

# Search universal data
m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>([\s\S]*?)</script>', text)
if m:
    print("Found __UNIVERSAL_DATA_FOR_REHYDRATION__")
    try:
        data = json.loads(m.group(1))
        scope = data.get("__DEFAULT_SCOPE__", {})
        print("Scope keys:", list(scope.keys()))
        video_detail = scope.get("webapp.video-detail", {})
        item_struct = video_detail.get("itemInfo", {}).get("itemStruct", {})
        if item_struct:
            with open("tiktok_video_data.json", "w", encoding="utf-8") as out_f:
                json.dump(item_struct, out_f, indent=2, ensure_ascii=False)
            print("Successfully dumped itemStruct to tiktok_video_data.json")
    except Exception as e:
        import traceback
        traceback.print_exc()
else:
    print("No __UNIVERSAL_DATA_FOR_REHYDRATION__")

# Search SIGI
m_sigi = re.search(r'<script id="SIGI_STATE"[^>]*>([\s\S]*?)</script>', text)
if m_sigi:
    print("Found SIGI_STATE")
