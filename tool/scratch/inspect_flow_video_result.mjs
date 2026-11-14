const task = await taskSpace("Google Flow Check Video");
const page = task.page("p1");

const url = "https://flow.google.com/project/97437688-2b73-4a07-9091-77969b802e73";
await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
await page.waitForTimeout(4000);

// Check videos and media in the project
const mediaGallery = await page.evaluate(() => {
  const videos = Array.from(document.querySelectorAll("video")).map(v => ({
    src: v.src || v.currentSrc,
    duration: v.duration,
    paused: v.paused
  }));

  const mediaCards = Array.from(document.querySelectorAll("[class*='media-card'], [class*='asset-card'], [class*='tile-view'], .tile-container")).map(c => ({
    text: (c.innerText || '').trim().replace(/\n+/g, ' | '),
    className: c.className,
    hasVideo: !!c.querySelector("video"),
    hasImg: !!c.querySelector("img")
  }));

  return { videos, mediaCards: mediaCards.slice(0, 10) };
});

console.log("[Ego] Media Gallery:", JSON.stringify(mediaGallery, null, 2));

const galleryShot = "/Volumes/Data/gobi-social/shots/ego_flow_media_gallery_status.png";
await page.screenshot({ path: galleryShot });
console.log("[Ego] Gallery screenshot saved to:", galleryShot);

await task.finish({ keep: ["p1"] });
