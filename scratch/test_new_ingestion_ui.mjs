const task = await taskSpace("Gobi Dashboard Ingestion Review");
const page = task.page("p1");

console.log("[Ego] Navigating to http://localhost:3000...");
await page.goto("http://localhost:3000", { waitUntil: "domcontentloaded", timeout: 15000 });
await page.waitForTimeout(3000);

// Screenshot 1: Refined Overview with Fast Ingestion Strip in Hero
const shotRefined = "/Volumes/Data/gobi-social/shots/dashboard_refined_hero_input.png";
await page.screenshot({ path: shotRefined });
console.log("[Ego] Refined Overview screenshot saved to:", shotRefined);

// Click "+ Nạp Job Mới" button in Navbar
console.log("[Ego] Clicking '+ Nạp Job Mới' in Navbar...");
await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button"));
  const btn = buttons.find(b => (b.innerText || '').includes("Nạp Job Mới"));
  if (btn) btn.click();
});
await page.waitForTimeout(1500);

// Screenshot 2: Create Job Modal
const shotModal = "/Volumes/Data/gobi-social/shots/dashboard_create_job_modal.png";
await page.screenshot({ path: shotModal });
console.log("[Ego] Create Job Modal screenshot saved to:", shotModal);

// Type a sample link into the input
await page.evaluate(() => {
  const input = document.querySelector("input[type='url']");
  if (input) {
    input.value = "https://www.tiktok.com/@beenalth/video/7678960622423330066";
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }
});
await page.waitForTimeout(800);

const shotTyped = "/Volumes/Data/gobi-social/shots/dashboard_create_job_typed.png";
await page.screenshot({ path: shotTyped });
console.log("[Ego] Typed input screenshot saved to:", shotTyped);

await task.finish({ keep: ["p1"] });
