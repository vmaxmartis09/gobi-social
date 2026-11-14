/**
 * Claim TaskSpace and inspect Kling AI creation interface
 */
const task = await claimTaskSpace(2);
const pages = task.tabs ? await task.tabs() : [];
console.log("[Ego] Tabs count:", pages.length);

// Let's create or find the Kling page
const page = await task.newPage();
console.log("[Ego] Navigating directly to Kling Video Generation...");
await page.goto("https://kling.ai/app/creations/video", {
  waitUntil: "domcontentloaded",
  timeout: 45000
});
await page.waitForTimeout(5000);

const title = await page.title();
const url = page.url();
console.log("[Ego] Kling Page Title:", title);
console.log("[Ego] Kling URL:", url);

// Dismiss popups / cookie notices if any
await page.evaluate(() => {
  const dismissButtons = Array.from(document.querySelectorAll("button, div[role='button'], span")).filter(el => {
    const text = (el.innerText || '').toLowerCase().trim();
    return text === "got it" || text === "accept all" || text === "agree" || text === "close" || text === "ok";
  });
  dismissButtons.forEach(b => b.click());
});

await page.waitForTimeout(1500);

const screenshotPath = "/Volumes/Data/gobi-social/shots/kling_video_gen_ui.png";
await page.screenshot({ path: screenshotPath });
console.log("[Ego] Screenshot saved to:", screenshotPath);

// Extract interactive elements
const uiInfo = await page.evaluate(() => {
  // Find tabs/modes: Text to Video, Image to Video, etc.
  const tabs = Array.from(document.querySelectorAll("div, button, li, span"))
    .map(el => ({ text: (el.innerText || '').trim(), class: el.className }))
    .filter(el => ["Image to Video", "Text to Video", "Video to Video", "Elements", "Motion Brush", "Camera"].some(k => el.text.includes(k)));

  // Find file inputs
  const fileInputs = Array.from(document.querySelectorAll("input[type='file']")).map(inp => ({
    class: inp.className,
    accept: inp.getAttribute('accept'),
    id: inp.id
  }));

  // Find prompt inputs
  const promptInputs = Array.from(document.querySelectorAll("textarea, [contenteditable='true']")).map(el => ({
    placeholder: el.getAttribute('placeholder') || el.innerText,
    class: el.className
  }));

  // Find Generate button
  const generateButtons = Array.from(document.querySelectorAll("button")).map(b => (b.innerText || '').trim()).filter(t => t.toLowerCase().includes("generate"));

  return { tabs, fileInputs, promptInputs, generateButtons };
});

console.log("[Ego] Kling UI Info:", JSON.stringify(uiInfo, null, 2));

await task.finish({ keep: [page.label] });
