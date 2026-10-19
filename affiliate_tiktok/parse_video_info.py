import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

content_file = r"C:\Users\HAI\.gemini\antigravity\brain\383fa778-c3ea-408f-bf80-315f12e6d6f3\.system_generated\steps\837\content.md"

with open(content_file, "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', text, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    scope = data.get("__DEFAULT_SCOPE__", {})
    print("Scope keys:", list(scope.keys()))
    for k, v in scope.items():
        if isinstance(v, dict):
            print(f"  {k} keys:", list(v.keys()))
            if "shareMeta" in v:
                print(f"    shareMeta:", v["shareMeta"])
            if "itemInfo" in v:
                print(f"    itemInfo:", v["itemInfo"])
