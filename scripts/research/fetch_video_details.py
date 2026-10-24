import urllib.request
import json
import re
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

video_ids = [
    'MFNJns-r840', # Bulk Video Creation Tool
    'SsMLBpDCing', # Create AI Videos Automatically
    'AsF7vXwArqo', # Create AI Videos Automatically in Any Language
    '5sqJlQBTBf4', # Video KOC AI - Thể loại Cập nhật thông tin
    'mC0j2tQ2RHU', # Câu lệnh Video KOC AI - Chill Beatbox Music
    'hAho-5UHA54', # KOC AI - Bộ giải pháp tạo ra video chân thật, nhanh chóng, dành cho affiliate
    'nEtDRyjyVbE', # KOC AI - Tạo ra những video nhanh chóng từ workflow.
    'YklvukrODd8', # KOC AI - Update lại bộ giải pháp, ưu tiên hiệu quả và tiết kiệm chi phí nhất
    'TMbKZ4j2LE8', # KOC AI - review sản phẩm - mỹ phẩm
    'w4xmKsXuMEg', # Tạo video KOC AI với model Veo3
    'KJGpujaLNMc', # KOC AI - Workflow review sản phẩm căn hộ dùng model Veo3.1
    'BxTe0O-p28A', # Quy trình KOC AI đánh giá giày thể thao từ Walmart
    'D0pNOwHKqws', # Quy trình KOC AI Workflow review sản phẩm bằng mô hình Veo 3
    'R2tnz2_bdho', # KOC AI Storyboard Tập thể dục buổi sáng
    'ORvrhQUYzMA', # AI Automation Workflow
    'Zt5lYIxD4C8'  # AI Workflow Automation
]

details = {}

for vid in video_ids:
    url = f"https://www.youtube.com/watch?v={vid}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        # find title and description
        title_m = re.search(r'<title>(.*?)</title>', html)
        title = title_m.group(1) if title_m else ""
        
        # find description
        desc_m = re.search(r'"shortDescription":"(.*?)"', html)
        desc = ""
        if desc_m:
            desc = desc_m.group(1).encode('utf-8').decode('unicode_escape', errors='ignore')
            
        details[vid] = {
            'id': vid,
            'title': title,
            'description': desc,
            'url': url
        }
        print(f"Fetched {vid}: {title}")
        if desc:
            print(f"   Desc: {desc[:150]}...")
    except Exception as e:
        print(f"Error {vid}: {e}")

with open('data/raw/youtube/video_details.json', 'w', encoding='utf-8') as f:
    json.dump(details, f, ensure_ascii=False, indent=2)

print("\nDone! Saved to data/raw/youtube/video_details.json")
