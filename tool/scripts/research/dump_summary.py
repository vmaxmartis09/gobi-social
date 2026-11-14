import json
import sys

with open('data/raw/youtube/video_details.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open('data/raw/youtube/parsed_summary.txt', 'w', encoding='utf-8') as out:
    out.write(f"ID: {d.get('id')}\n")
    out.write(f"Desc: {d.get('desc')}\n")
    out.write(f"CreateTime: {d.get('createTime')}\n")
    out.write(f"SuggestedWords: {d.get('suggestedWords')}\n")
    out.write(f"DiversificationLabels: {d.get('diversificationLabels')}\n")
    out.write(f"AIGCDescription: {d.get('AIGCDescription')}\n")
    out.write(f"IsAigc: {d.get('IsAigc')}\n")
    out.write(f"Contents: {d.get('contents')}\n")
    
    video = d.get('video', {})
    for k, v in video.items():
        if isinstance(v, str) and ('http' in v or len(v) < 200):
            out.write(f"video.{k}: {v}\n")
            
    music = d.get('music', {})
    for k, v in music.items():
        if isinstance(v, str):
            out.write(f"music.{k}: {v}\n")

print("Saved to data/raw/youtube/parsed_summary.txt")
