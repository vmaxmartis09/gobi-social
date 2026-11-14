import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/raw/tiktok/tiktok_fashion_survey.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('data/analytics/survey_analysis.txt', 'w', encoding='utf-8') as out:
    for i, v in enumerate(data, 1):
        out.write(f"==================== VIDEO #{i} ====================\n")
        out.write(f"URL: {v.get('url')}\n")
        out.write(f"Author: {v.get('author_name')} (@{v.get('author_id')})\n")
        out.write(f"Title / Caption: {v.get('title')}\n")
        out.write(f"Duration: {v.get('duration')}s\n")
        out.write(f"Views: {v.get('play_count'):,} | Likes: {v.get('digg_count'):,} | Shares: {v.get('share_count')} | Saves: {v.get('collect_count')}\n")
        out.write(f"Music: {v.get('music_title')} (by {v.get('music_author')})\n")
        out.write(f"Anchors: {json.dumps(v.get('anchors'), ensure_ascii=False)}\n")
        out.write(f"Anchors Extras: {v.get('anchors_extras')}\n")
        out.write(f"Commerce Info: {json.dumps(v.get('commerce_info'), ensure_ascii=False)}\n")
        out.write(f"Play Address: {v.get('play')}\n")
        out.write(f"Cover: {v.get('cover')}\n\n")

print("Analysis saved to data/analytics/survey_analysis.txt")
