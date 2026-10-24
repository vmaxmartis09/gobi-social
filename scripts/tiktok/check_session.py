from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0]
    print("URL:", page.url)
    print("Title:", page.title())
    has_login = page.locator('button:has-text("Log in"), button:has-text("Đăng nhập")').first.is_visible()
    has_profile = page.locator('div[data-e2e="profile-icon"], a[href*="/@"]').first.is_visible()
    print("Has login button:", has_login)
    print("Has profile element:", has_profile)
