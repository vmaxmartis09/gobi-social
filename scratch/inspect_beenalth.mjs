const task = await taskSpace("Inspect TikTok Video Beenalth Full");
const page = task.page("p1");

console.log("Navigating to TikTok video...");
await page.goto("https://www.tiktok.com/@beenalth/video/7678960622423330066?_r=1&_t=ZS-9Ahu49CY6tQ");
await page.waitForLoadState();
await new Promise(r => setTimeout(r, 6000));

// Click "more" button if present
try {
  await page.evaluate(() => {
    const moreBtn = Array.from(document.querySelectorAll('button, span')).find(b => b.innerText && b.innerText.trim().toLowerCase() === 'more');
    if (moreBtn) moreBtn.click();
  });
} catch (e) {
  console.log("No more button error:", e);
}

await new Promise(r => setTimeout(r, 1000));

const data = await page.evaluate(() => {
  const descEl = document.querySelector('[data-e2e="browse-video-desc"]');
  const fullDesc = descEl ? descEl.innerText : "";
  const authorEl = document.querySelector('[data-e2e="browse-username"]') || document.querySelector('[data-e2e="browser-nickname"]');
  const author = authorEl ? authorEl.innerText : "";
  const musicEl = document.querySelector('[data-e2e="browse-music"]');
  const music = musicEl ? musicEl.innerText : "";
  const video = document.querySelector('video');
  const videoSrc = video ? (video.currentSrc || video.src) : "";
  const duration = video ? video.duration : 0;
  
  // Grab all text around the video container
  const container = document.querySelector('[data-e2e="browse-video-desc"]')?.parentElement;
  const containerText = container ? container.innerText : "";

  return { fullDesc, author, music, videoSrc, duration, containerText };
});

console.log("DETAILED_DATA:", JSON.stringify(data, null, 2));

const shot3 = "/Volumes/Data/gobi-social/shots/beenalth_full_desc.png";
await page.screenshot({ path: shot3 });

await task.finish({ keep: [] });
