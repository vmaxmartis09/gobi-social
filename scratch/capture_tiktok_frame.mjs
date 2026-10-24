const task = await taskSpace("Inspect TikTok Video Detail");
const page = task.page("p1");

await page.goto("https://www.tiktok.com/@outfitsbyhan.han/video/7697472862633921812?_r=1&_t=ZS-9AgMU4r53Bt");
await page.waitForLoadState();
await new Promise(r => setTimeout(r, 5000));

// Click play button if video is paused, or focus video
const videoDetails = await page.evaluate(async () => {
  const v = document.querySelector('video');
  if (!v) return { error: "No video found" };

  try {
    v.muted = true;
    await v.play();
  } catch (e) {}

  return {
    src: v.src,
    currentSrc: v.currentSrc,
    duration: v.duration,
    currentTime: v.currentTime,
    videoWidth: v.videoWidth,
    videoHeight: v.videoHeight,
    poster: v.poster,
    paused: v.paused
  };
});

console.log("Video Details:", videoDetails);

// Wait 2s for playback
await new Promise(r => setTimeout(r, 2000));

// Capture screenshot of video specifically or full screen
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/tiktok_video_frame.png" });

// Also let's capture the canvas frame from the video element directly!
const frameDataUrl = await page.evaluate(() => {
  const v = document.querySelector('video');
  if (!v || v.videoWidth === 0) return null;
  const canvas = document.createElement('canvas');
  canvas.width = v.videoWidth;
  canvas.height = v.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(v, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/jpeg', 0.9);
});

if (frameDataUrl) {
  const fs = await import('fs');
  const base64Data = frameDataUrl.replace(/^data:image\/jpeg;base64,/, "");
  fs.writeFileSync("/Volumes/Data/gobi-social/shots/tiktok_direct_frame.jpg", base64Data, 'base64');
  console.log("Saved direct video frame to shots/tiktok_direct_frame.jpg");
}

await task.finish({ keep: [] });
