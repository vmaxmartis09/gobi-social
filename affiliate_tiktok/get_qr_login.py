from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        r'C:\Users\HAI\.agent-browser\profiles\ai_profile',
        channel='chrome',
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto('https://www.tiktok.com/login')
    page.wait_for_timeout(3000)
    
    qr_btn = page.locator('div:has-text("Use QR code"), a:has-text("Use QR code")').last
    if qr_btn.is_visible(timeout=3000):
        qr_btn.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=r'c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\tiktok_qr_login.png')
        page.screenshot(path=r'c:\Users\HAI\OneDrive\Tài liệu\vmax\shots\live.png')
        print("[+] QR Code da duoc chup va cap nhat len live_viewer.html!")
    browser.close()
