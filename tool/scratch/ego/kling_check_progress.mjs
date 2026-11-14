/**
 * Check Kling AI generation progress
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

await page.goto("https://kling.ai/app/creations/video", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

const progressInfo = await page.evaluate(() => {
  const cards = Array.from(document.querySelectorAll("[class*='item'], [class*='card'], [class*='task'], [class*='creation']")).map(el => ({
    text: (el.innerText || '').trim(),
    hasVideo: !!el.querySelector("video"),
    videoSrc: el.querySelector("video") ? el.querySelector("video").src : null
  })).filter(c => c.text.includes("Gobi") || c.text.includes("Cinematic") || c.text.includes("%") || c.text.toLowerCase().includes("queue"));

  return cards;
});

console.log("[Ego] Kling Progress Info:", JSON.stringify(progressInfo, null, 2));

const shotCheck = "/Volumes/Data/gobi-social/shots/kling_progress_status.png";
await page.screenshot({ path: shotCheck });
console.log("[Ego] Progress screenshot saved to:", shotCheck);

await task.finish({ keep: [page.label] });
