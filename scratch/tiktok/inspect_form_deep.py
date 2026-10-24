import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        os.path.join(os.path.expanduser("~"), ".agent-browser", "profiles", r"ai_profile"),
        channel='chrome',
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://www.tiktok.com/login/email/forget-password")
    page.wait_for_timeout(3000)
    
    # Check form element and submit handlers
    form_info = page.evaluate("""() => {
        const form = document.querySelector('form');
        const btn = document.querySelector('button[type="submit"]');
        return {
            hasForm: !!form,
            formAction: form ? form.action : null,
            btnOuter: btn ? btn.outerHTML : null,
            btnDisabled: btn ? btn.disabled : null,
            parentHTML: btn ? btn.parentElement.outerHTML : null
        };
    }""")
    print("Form info:", json.dumps(form_info, indent=2))
    browser.close()
