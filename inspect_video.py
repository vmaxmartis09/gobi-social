import json

with open('channel_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Search for elements containing videoId 'hAho-5UHA54' or any
target_id = 'hAho-5UHA54'

def find_context(obj, target):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if v == target:
                print("Found match in key:", k)
                print(json.dumps(obj, ensure_ascii=False, indent=2)[:1000])
                return True
            if find_context(v, target):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if find_context(item, target):
                return True
    return False

find_context(data, target_id)
