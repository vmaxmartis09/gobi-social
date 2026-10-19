import json

with open('channel_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Keys in data:", list(data.keys()))
# Recursively find any keys that have 'video' or 'renderer'
found_keys = set()
def explore(d, depth=0):
    if depth > 5:
        return
    if isinstance(d, dict):
        for k, v in d.items():
            if 'video' in k.lower() or 'tab' in k.lower() or 'item' in k.lower() or 'content' in k.lower():
                found_keys.add(k)
            explore(v, depth+1)
    elif isinstance(d, list):
        for x in d:
            explore(x, depth+1)

explore(data)
print("Interesting keys:", found_keys)
