/**
 * Inspect Google Flow state and controls
 */
const task = await taskSpace("Gobi_Native_AI_Motion");
const page = task.page("p1");

console.log("[Ego] Opening Google Flow project...");
await page.goto("https://flow.google.com/u/1/project/905a28b7-ceb4-4cf9-b92d-443050bd2d43", {
  waitUntil: "domcontentloaded",
  timeout: 45000
});

await page.waitForTimeout(5000);

const currentUrl = page.url();
const title = await page.title();
console.log("[Ego] Current URL:", currentUrl);
console.log("[Ego] Page Title:", title);

const screenshotPath = "/Volumes/Data/gobi-social/shots/google_flow_current_state.png";
await page.screenshot({ path: screenshotPath });
console.log("[Ego] Screenshot saved to:", screenshotPath);

// Check if user is logged in or if prompt bar is visible
const uiState = await page.evaluate(() => {
  const editor = document.querySelector("[contenteditable='true'], textarea, [data-slate-editor='true']");
  const buttons = Array.from(document.querySelectorAll("button")).map(b => (b.innerText || '').trim()).filter(Boolean);
  return {
    hasEditor: !!editor,
    buttonCount: buttons.length,
    buttonsSample: buttons.slice(0, 15)
  };
});

console.log("[Ego] UI State:", JSON.stringify(uiState, null, 2));

// Keep page open so user can see or interact
await task.finish({ keep: ["p1"] });
