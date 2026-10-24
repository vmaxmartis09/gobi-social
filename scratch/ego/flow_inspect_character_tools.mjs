/**
 * Inspect Google Flow Canvas controls for Character/Actor creation
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

console.log("[Ego] Opening active Google Flow project...");
await page.goto("https://flow.google.com/", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

// Open the first project in list
await page.evaluate(() => {
  const projectCards = Array.from(document.querySelectorAll("[class*='project-thumbnail'], [class*='project-card'], [aria-label*='dự án']"));
  if (projectCards.length > 0) projectCards[0].click();
});
await page.waitForTimeout(5000);

console.log("[Ego] Current URL:", page.url());

// Inspect all buttons, icons, menus in the Flow Studio
const studioElements = await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, div[role='button'], a, [class*='tool'], [class*='tab'], [class*='panel']")).map(b => ({
    text: (b.innerText || '').trim(),
    ariaLabel: b.getAttribute('aria-label'),
    title: b.getAttribute('title'),
    className: b.className
  })).filter(b => b.text || b.ariaLabel || b.title);

  // Search specifically for Character / Actor / Tác nhân / Nhân vật / Element / Asset
  const characterControls = buttons.filter(b => {
    const s = `${b.text} ${b.ariaLabel} ${b.title}`.toLowerCase();
    return s.includes("nhân vật") || s.includes("tác nhân") || s.includes("character") || s.includes("actor") || s.includes("người") || s.includes("đối tượng") || s.includes("tài sản") || s.includes("asset");
  });

  return { sampleButtons: buttons.slice(0, 30), characterControls };
});

console.log("[Ego] Character Controls:", JSON.stringify(studioElements.characterControls, null, 2));
console.log("[Ego] Sample Buttons:", JSON.stringify(studioElements.sampleButtons.slice(0, 15), null, 2));

const shotStudio = "/Volumes/Data/gobi-social/shots/google_flow_studio_controls.png";
await page.screenshot({ path: shotStudio });
console.log("[Ego] Screenshot saved to:", shotStudio);

await task.finish({ keep: [page.label] });
