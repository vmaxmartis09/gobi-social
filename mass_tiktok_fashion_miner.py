import os
import sys
import time
import json
import urllib.parse
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

collected_videos = {}

def handle_response(response):
    url = response.url
    if "api/search" in url or "api/challenge" in url:
        try:
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                data = response.json()
                data_list = data.get("data") or data.get("item_list") or []
                if isinstance(data_list, list):
                    for item in data_list:
                        # Extract video item
                        v_info = item.get("item") or item
                        vid_id = v_info.get("id") or v_info.get("video_id")
                        if vid_id and vid_id not in collected_videos:
                            stats = v_info.get("stats", {})
                            author = v_info.get("author", {})
                            music = v_info.get("music", {})
                            anchors = v_info.get("anchors", [])
                            
                            collected_videos[vid_id] = {
                                "id": vid_id,
                                "desc": v_info.get("desc", ""),
                                "author": author.get("nickname") or author.get("uniqueId"),
                                "author_id": author.get("uniqueId"),
                                "views": stats.get("playCount", 0),
                                "likes": stats.get("diggCount", 0),
                                "shares": stats.get("shareCount", 0),
                                "saves": stats.get("collectCount", 0),
                                "comments": stats.get("commentCount", 0),
                                "music": f"{music.get('title')} - {music.get('authorName')}",
                                "anchors": anchors,
                                "video_url": f"https://www.tiktok.com/@{author.get('uniqueId')}/video/{vid_id}"
                            }
                            print(f"[+] Harvested: {vid_id} | {stats.get('playCount', 0):,} views | {v_info.get('desc', '')[:40]}...")
        except Exception:
            pass

queries = [
    "set 2 dây cardigan hàn quốc",
    "quần short nắp túi cạp trễ",
    "áo thun dài tay ôm body hàn quốc",
    "áo len dệt kim form ôm hàn quốc",
    "phối đồ nữ phong cách hàn quốc nhu mì",
    "quần ống suông nữ cạp cao hack dáng",
    "chân váy chữ a xếp ly hàn quốc",
    "đầm hoa nhí tiểu thư hàn quốc"
]

print(f"[*] Starting Big Data Harvester across {len(queries)} fashion categories...")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        executable_path=CHROME_BIN,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.on("response", handle_response)
    
    for q_idx, q in enumerate(queries, 1):
        print(f"\n==================================================")
        print(f"[*] Query {q_idx}/{len(queries)}: '{q}'")
        print(f"==================================================")
        encoded_q = urllib.parse.quote(q)
        search_url = f"https://www.tiktok.com/search?q={encoded_q}"
        
        try:
            page.goto(search_url, wait_until="domcontentloaded", timeout=40000)
            time.sleep(4)
            
            # Continuous deep scrolling to load batches of 20-30 videos each
            for scroll_step in range(1, 12):
                page.evaluate("window.scrollBy(0, 2200)")
                time.sleep(2.5)
                
            # Fallback DOM extraction for any elements not captured via API
            dom_items = page.evaluate("""() => {
                const results = [];
                document.querySelectorAll('a[href*="/video/"]').forEach(a => {
                    const href = a.href;
                    const container = a.closest('div[data-e2e="search_video-item"]') || a.parentElement;
                    const text = container ? container.innerText.trim() : '';
                    results.push({ url: href, text: text });
                });
                return results;
            }""")
            
            for item in dom_items:
                m = re.search(r'/video/(\d+)', item["url"])
                if m:
                    vid_id = m.group(1)
                    if vid_id not in collected_videos:
                        collected_videos[vid_id] = {
                            "id": vid_id,
                            "desc": item["text"].split("\n")[0] if item["text"] else "",
                            "video_url": item["url"],
                            "raw_dom_text": item["text"]
                        }
            
            print(f"[*] Accumulated unique videos so far: {len(collected_videos)}")
        except Exception as e:
            print(f"[!] Error querying '{q}': {e}")
            
        time.sleep(2)
        
    context.close()

# Save entire big data set
out_path = os.path.join(r"c:\Users\HAI\OneDrive\Tài liệu\vmax\configs", "koc_fashion_bigdata_harvest.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(list(collected_videos.values()), f, ensure_ascii=False, indent=2)

print(f"\n[DONE] Successfully harvested {len(collected_videos)} unique videos into: {out_path}")
