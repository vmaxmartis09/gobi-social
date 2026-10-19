import requests
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "https://www.tiktok.com/@thaodoll__/video/7689849896786054407",
    "https://www.tiktok.com/@suchangvn/video/7695360394512108821",
    "https://www.tiktok.com/@anhlonglanhreview/video/7697112556078402823",
    "https://www.tiktok.com/@lizzie_phmm/video/7693557919828217108",
    "https://www.tiktok.com/@thaomy_riviuu/video/7690285691518930184",
    "https://www.tiktok.com/@bobietyeu.05/video/7693160717192629511",
    "https://www.tiktok.com/@bobanquan/video/7696971371536076048",
    "https://www.tiktok.com/@lumystore6/video/7690007359501978900"
]

results = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

for idx, u in enumerate(urls, 1):
    print(f"[{idx}/{len(urls)}] Dang cao du lieu tu: {u}...")
    try:
        api_url = f"https://www.tikwm.com/api/?url={u}"
        resp = requests.get(api_url, headers=headers, timeout=15)
        data = resp.json()
        
        if data.get("code") == 0:
            d = data.get("data", {})
            item = {
                "url": u,
                "id": d.get("id"),
                "title": d.get("title"),
                "author_id": d.get("author", {}).get("unique_id"),
                "author_name": d.get("author", {}).get("nickname"),
                "duration": d.get("duration"),
                "play_count": d.get("play_count"),
                "digg_count": d.get("digg_count"),
                "comment_count": d.get("comment_count"),
                "share_count": d.get("share_count"),
                "collect_count": d.get("collect_count"),
                "music_title": d.get("music_info", {}).get("title"),
                "music_author": d.get("music_info", {}).get("author"),
                "anchors": d.get("anchors"),
                "anchors_extras": d.get("anchors_extras"),
                "commerce_info": d.get("commerce_info"),
                "cover": d.get("cover"),
                "play": d.get("play")
            }
            results.append(item)
            print(f"   -> [OK] '{d.get('title')[:60]}...' | {d.get('play_count'):,} views | {d.get('digg_count'):,} tim")
        else:
            print(f"   -> [FAILED] TikWM msg: {data.get('msg')}")
            results.append({"url": u, "error": data.get("msg")})
    except Exception as e:
        print(f"   -> [ERROR] {e}")
        results.append({"url": u, "error": str(e)})
    time.sleep(1.5)

with open("tiktok_fashion_survey.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n[HOÀN TẤT] Đã lưu dữ liệu {len(results)} video vào tiktok_fashion_survey.json")
