const task = await taskSpace("Google Flow Review");
const page = task.page("p1");

console.log("[Ego] Navigating to https://flow.google.com...");
await page.goto("https://flow.google.com", { waitUntil: "domcontentloaded", timeout: 30000 });
await page.waitForTimeout(4000);

const currentUrl = page.url();
const title = await page.title();
console.log("[Ego] Current URL:", currentUrl);
console.log("[Ego] Page Title:", title);

// Take screenshot of home/dashboard
const homeShot = "/Volumes/Data/gobi-social/shots/ego_flow_home_review.png";
await page.screenshot({ path: homeShot });
console.log("[Ego] Home screenshot saved to:", homeShot);

// Inspect projects and UI elements
const dashboardInfo = await page.evaluate(() => {
  const projects = Array.from(document.querySelectorAll("[class*='project-card'], [class*='project-tile'], [class*='recent-item'], mat-card, a[href*='/project/']")).map(el => {
    const link = el.tagName === 'A' ? el.href : (el.querySelector("a")?.href || '');
    return {
      text: (el.innerText || '').trim().replace(/\n+/g, ' | '),
      href: link
    };
  });

  const buttons = Array.from(document.querySelectorAll("button, [role='button']")).map(b => (b.innerText || b.getAttribute('aria-label') || '').trim()).filter(Boolean);

  return { projects, buttons: buttons.slice(0, 15) };
});

console.log("[Ego] Dashboard Info:", JSON.stringify(dashboardInfo, null, 2));

await task.finish({ keep: ["p1"] });
