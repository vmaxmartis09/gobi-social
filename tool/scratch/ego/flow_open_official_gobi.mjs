/**
 * Open the user's official Gobi project in Google Flow
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const officialProjectUrl = "https://flow.google.com/project/97437688-2b73-4a07-9091-77969b802e73";
console.log("[Ego] Opening Official Gobi Project:", officialProjectUrl);

await page.goto(officialProjectUrl, {
  waitUntil: "domcontentloaded",
  timeout: 35000
});
await page.waitForTimeout(4000);

const currentUrl = page.url();
const pageTitle = await page.title();
console.log("[Ego] Current URL:", currentUrl);
console.log("[Ego] Page Title:", pageTitle);

const shotProject = "/Volumes/Data/gobi-social/shots/google_flow_official_gobi_project.png";
await page.screenshot({ path: shotProject });
console.log("[Ego] Screenshot saved to:", shotProject);

// Inspect the project canvas: how many characters, assets, and the prompt input at the bottom
const canvasInfo = await page.evaluate(() => {
  const characters = Array.from(document.querySelectorAll("[class*='character'], [class*='avatar'], [class*='tile']")).map(el => (el.innerText || '').trim()).filter(Boolean);
  const bottomBar = document.querySelector(".bottom-bar, [class*='prompt-box'], [class*='controls']");
  const buttons = Array.from(document.querySelectorAll("button")).map(b => (b.innerText || b.getAttribute('aria-label') || '').trim()).filter(Boolean);

  return { characters: characters.slice(0, 10), buttons: buttons.slice(0, 20) };
});

console.log("[Ego] Canvas Info:", JSON.stringify(canvasInfo, null, 2));

await task.finish({ keep: [page.label] });
