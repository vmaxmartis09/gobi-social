const task = await taskSpace("Inspect Outfitsbyhan Video");
const page = task.page("p1");

console.log("Navigating directly to video...");
await page.goto("https://www.tiktok.com/@outfitsbyhan.han/video/7697472862633921812");
await page.waitForLoadState();
await new Promise(r => setTimeout(r, 4000));

const videoInfo = await page.evaluate(() => {
  const allVideos = Array.from(document.querySelectorAll('video')).map((v, i) => ({
    index: i,
    src: v.src,
    currentSrc: v.currentSrc,
    width: v.videoWidth,
    height: v.videoHeight,
    duration: v.duration,
    currentTime: v.currentTime,
    paused: v.paused,
    parentClass: v.parentElement?.className
  }));

  const desc = document.querySelector('[data-e2e="browse-video-desc"]')?.innerText || "";
  const nickname = document.querySelector('[data-e2e="browser-nickname"]')?.innerText || "";

  return { allVideos, desc, nickname, url: window.location.href };
});

console.log("Video Info:", JSON.stringify(videoInfo, null, 2));

// Let's capture the main container screenshot
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/outfitsbyhan_page.png" });

await task.finish({ keep: [] });
