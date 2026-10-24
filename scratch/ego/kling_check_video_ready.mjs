/**
 * Check Kling AI generation status and video download URL
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

await page.goto("https://kling.ai/app/creations/video", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

const klingStatus = await page.evaluate(() => {
  const videos = Array.from(document.querySelectorAll("video")).map(v => ({
    src: v.src,
    duration: v.duration
  }));

  const queueCards = Array.from(document.querySelectorAll("[class*='item'], [class*='card'], [class*='task']")).map(el => (el.innerText || '').trim()).filter(t => t.includes("%") || t.toLowerCase().includes("generating") || t.toLowerCase().includes("queue"));

  return { videoCount: videos.length, videos, queueCards: queueCards.slice(0, 5) };
});

console.log("[Ego] Kling Status:", JSON.stringify(klingStatus, null, 2));

const shotKlingNow = "/Volumes/Data/gobi-social/shots/kling_current_status_after_flow.png";
await page.screenshot({ path: shotKlingNow });
console.log("[Ego] Kling status screenshot saved to:", shotKlingNow);

await task.finish({ keep: [page.label] });
