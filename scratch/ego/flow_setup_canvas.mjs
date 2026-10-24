/**
 * Inspect Google Flow newly created canvas and upload reference
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

console.log("[Ego] Connecting to Google Flow newly created project...");
await page.goto("https://flow.google.com/", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

// Open the first project in the list (the newest one)
const projectOpened = await page.evaluate(() => {
  const projectCards = Array.from(document.querySelectorAll("[class*='project-thumbnail'], [class*='project-card'], [aria-label*='dự án']"));
  if (projectCards.length > 0) {
    projectCards[0].click();
    return true;
  }
  return false;
});

console.log("[Ego] Project clicked:", projectOpened);
await page.waitForTimeout(5000);

const currentUrl = page.url();
const title = await page.title();
console.log("[Ego] Project Page URL:", currentUrl);
console.log("[Ego] Project Page Title:", title);

const shotCanvas = "/Volumes/Data/gobi-social/shots/google_flow_active_project.png";
await page.screenshot({ path: shotCanvas });
console.log("[Ego] Active project screenshot saved to:", shotCanvas);

await task.finish({ keep: [page.label] });
