import time
import sys
import json
import re
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = r"C:\Users\HAI\.agent-browser\profiles\ai_profile"
CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

queries = [
    "set 2 dây cardigan hàn quốc",
    "quần short nắp túi cạp trễ",
    "áo thun dài tay ôm body hàn quốc"
]

all_found_videos = []

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        executable_path=CHROME_BIN,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    
    for q in queries:
        search_url = f"https://www.tiktok.com/search?q={requests.utils.quote(q) if 'requests' in globals() else q.replace(' ', '%20')}"
        print(f"\n[*] Tim kiem tren TikTok: '{q}' -> {search_url}")
        try:
            page.goto(search_url, wait_until='domcontentloaded', timeout=30000)
            time.sleep(5)
            
            # Scroll down to load videos
            for _ in range(3):
                page.evaluate("window.scrollBy(0, 1500)")
                time.sleep(2)
                
            # Extract video links
            links = page.evaluate("""() => {
                const results = [];
                const anchors = document.querySelectorAll('a[href*="/video/"]');
                anchors.forEach(a => {
                    const href = a.href;
                    // Find title/caption and stats nearby
                    const container = a.closest('div[data-e2e="search_video-item"]') || a.parentElement;
                    const text = container ? container.innerText.trim() : '';
                    if (!results.some(r => r.url === href)) {
                        results.push({ url: href, raw_text: text });
                    }
                });
                return results;
            }""")
            
            print(f"[+] Tim thay {len(links)} video cho tu khoa '{q}'")
            for item in links[:6]:
                all_found_videos.append({"query": q, "url": item["url"], "raw_text": item["raw_text"]})
                print(f"   + {item['url']}")
        except Exception as e:
            print(f"[!] Loi khi tim '{q}': {e}")
            
    context.close()

with open("tiktok_expanded_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_found_videos, f, ensure_ascii=False, indent=2)

print(f"\n[OK] Da thu thap tong cong {len(all_found_videos)} video lien quan!")
