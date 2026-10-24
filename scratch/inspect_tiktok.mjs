import path from "path";

const task = await taskSpace("Inspect TikTok Video");
const page = task.page("p1");

console.log("Navigating to TikTok video...");
await page.goto("https://www.tiktok.com/@outfitsbyhan.han/video/7697472862633921812?_r=1&_t=ZS-9AgMU4r53Bt");
await page.waitForLoadState();

// Wait 4 seconds for video and captions to load
await new Promise(r => setTimeout(r, 4000));

const shot1 = "/Volumes/Data/gobi-social/shots/tiktok_video_shot1.png";
const shot2 = "/Volumes/Data/gobi-social/shots/tiktok_video_shot2.png";
const shot3 = "/Volumes/Data/gobi-social/shots/tiktok_video_shot3.png";

await page.screenshot({ path: shot1 });
console.log("Saved screenshot:", shot1);

const data = await page.evaluate(() => {
  const title = document.title;
  const description = document.querySelector('meta[name="description"]')?.content || "";
  const videoText = document.querySelector('[data-e2e="browse-video-desc"]')?.innerText || "";
  const music = document.querySelector('[data-e2e="browse-music"]')?.innerText || "";
  const author = document.querySelector('[data-e2e="browser-nickname"]')?.innerText || "";
  const video = document.querySelector('video');
  const videoSrc = video ? video.src : "";
  const currentTime = video ? video.currentTime : 0;
  const duration = video ? video.duration : 0;
  return { title, description, videoText, music, author, videoSrc, currentTime, duration };
});

console.log("TikTok Video Data:", JSON.stringify(data, null, 2));

// Wait 3 seconds and take another shot
await new Promise(r => setTimeout(r, 3000));
await page.screenshot({ path: shot2 });
console.log("Saved screenshot:", shot2);

// Wait another 3 seconds
await new Promise(r => setTimeout(r, 3000));
await page.screenshot({ path: shot3 });
console.log("Saved screenshot:", shot3);

await task.finish({ keep: [] });
