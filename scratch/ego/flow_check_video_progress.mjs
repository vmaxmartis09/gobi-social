/**
 * Check Google Flow Video Generation Progress
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const projectUrl = "https://flow.google.com/project/97437688-2b73-4a07-9091-77969b802e73";
await page.goto(projectUrl, { waitUntil: "domcontentloaded" });
await page.waitForTimeout(4000);

const flowVideoStatus = await page.evaluate(() => {
  const mediaItems = Array.from(document.querySelectorAll("video, [class*='media-card'], [class*='asset-card'], [class*='tile']")).map(el => ({
    tagName: el.tagName,
    text: (el.innerText || '').trim(),
    src: el.src || (el.querySelector("video") ? el.querySelector("video").src : null) || (el.querySelector("img") ? el.querySelector("img").src : null)
  }));

  const progressBars = Array.from(document.querySelectorAll("[role='progressbar'], mat-progress-bar, [class*='progress']")).map(p => ({
    ariaValuenow: p.getAttribute('aria-valuenow'),
    className: p.className
  }));

  return { mediaItems: mediaItems.slice(0, 10), progressBars };
});

console.log("[Ego] Flow Video Status:", JSON.stringify(flowVideoStatus, null, 2));

const shotFlowNow = "/Volumes/Data/gobi-social/shots/google_flow_current_video_progress.png";
await page.screenshot({ path: shotFlowNow });
console.log("[Ego] Flow current video screenshot saved to:", shotFlowNow);

await task.finish({ keep: [page.label] });
