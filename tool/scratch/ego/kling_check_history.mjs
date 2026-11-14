/**
 * Check Kling AI creation history / timeline
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

await page.goto("https://kling.ai/app/creations/grid", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

const items = await page.evaluate(() => {
  const cards = Array.from(document.querySelectorAll("[class*='item'], [class*='card'], [class*='asset']")).map(el => ({
    text: (el.innerText || '').trim(),
    hasVideo: !!el.querySelector("video"),
    videoSrc: el.querySelector("video") ? el.querySelector("video").src : null,
    imgSrc: el.querySelector("img") ? el.querySelector("img").src : null
  })).filter(c => c.text || c.hasVideo || c.imgSrc);

  return items = cards.slice(0, 10);
});

console.log("[Ego] Grid Items:", JSON.stringify(items, null, 2));

const shotGrid = "/Volumes/Data/gobi-social/shots/kling_grid_history.png";
await page.screenshot({ path: shotGrid });
console.log("[Ego] Grid screenshot saved to:", shotGrid);

await task.finish({ keep: [page.label] });
