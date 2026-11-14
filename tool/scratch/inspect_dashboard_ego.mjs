const task = await taskSpace("Gobi Dashboard Review");
const page = task.page("p1");

console.log("[Ego] Navigating to http://localhost:3000...");
await page.goto("http://localhost:3000", { waitUntil: "domcontentloaded", timeout: 15000 });
await page.waitForTimeout(3000);

// Screenshot 1: Overview Dashboard
const shotMain = "/Volumes/Data/gobi-social/shots/dashboard_overview_kokonut_bw.png";
await page.screenshot({ path: shotMain });
console.log("[Ego] Overview screenshot saved to:", shotMain);

// Click on the first job card to open the Detail Inspector Modal
console.log("[Ego] Clicking on first job card...");
await page.evaluate(() => {
  const cards = document.querySelectorAll(".kokonut-card");
  // Find a card that contains "JOB-"
  const jobCard = Array.from(cards).find(c => c.innerText.includes("JOB-"));
  if (jobCard) jobCard.click();
});
await page.waitForTimeout(2000);

// Screenshot 2: Detail Modal Inspector
const shotModal = "/Volumes/Data/gobi-social/shots/dashboard_detail_modal_kokonut_bw.png";
await page.screenshot({ path: shotModal });
console.log("[Ego] Modal screenshot saved to:", shotModal);

// Click "Copy Prompt" button in modal
console.log("[Ego] Clicking Copy Prompt button in modal...");
await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button"));
  const copyBtn = buttons.find(b => (b.innerText || '').includes("Copy Prompt"));
  if (copyBtn) copyBtn.click();
});
await page.waitForTimeout(1000);

const shotCopied = "/Volumes/Data/gobi-social/shots/dashboard_prompt_copied_feedback.png";
await page.screenshot({ path: shotCopied });
console.log("[Ego] Prompt Copied screenshot saved to:", shotCopied);

await task.finish({ keep: ["p1"] });
