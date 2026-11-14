/**
 * Click "Start Creating" or ".new-project-button" in Google Flow
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

await page.goto("https://flow.google.com/", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

// Find and click the creation button
const clicked = await page.evaluate(() => {
  const btn = document.querySelector(".new-project-button") || 
              Array.from(document.querySelectorAll("button, a")).find(b => (b.innerText || '').includes("Start Creating") || (b.innerText || '').includes("Dự án mới"));
  if (btn) {
    btn.click();
    return { success: true, text: btn.innerText };
  }
  return { success: false };
});

console.log("[Ego] Clicked Start Creating:", JSON.stringify(clicked));
await page.waitForTimeout(6000);

const currentUrl = page.url();
console.log("[Ego] New URL after click:", currentUrl);

const shotAfter = "/Volumes/Data/gobi-social/shots/google_flow_after_start_creating.png";
await page.screenshot({ path: shotAfter });
console.log("[Ego] Screenshot saved to:", shotAfter);

await task.finish({ keep: [page.label] });
