const task = await taskSpace("Find Main TikTok Video");
const page = task.page("p1");

await page.goto("https://www.tiktok.com/@outfitsbyhan.han/video/7697472862633921812");
await page.waitForLoadState();
await new Promise(r => setTimeout(r, 6000));

const videoElements = await page.evaluate(() => {
  const videos = Array.from(document.querySelectorAll('video'));
  return videos.map((v, i) => {
    const rect = v.getBoundingClientRect();
    return {
      index: i,
      x: rect.x,
      y: rect.y,
      width: rect.width,
      height: rect.height,
      src: v.src,
      currentSrc: v.currentSrc,
      duration: v.duration,
      paused: v.paused,
      muted: v.muted,
      readyState: v.readyState
    };
  });
});

console.log("Found Videos:", JSON.stringify(videoElements, null, 2));

// If there is a video in the middle (e.g. rect.x between 200 and 800)
// Let's capture from that specific video!
if (videoElements.length > 0) {
  // Find the largest video or the one in the center
  const mainIdx = videoElements.reduce((bestIdx, cur, i) => {
    const area = cur.width * cur.height;
    const bestArea = videoElements[bestIdx].width * videoElements[bestIdx].height;
    return area > bestArea ? i : bestIdx;
  }, 0);

  console.log(`Main video is index ${mainIdx}`);

  const fs = await import('fs');
  const frame = await page.evaluate(async (idx) => {
    const v = document.querySelectorAll('video')[idx];
    if (!v) return null;
    v.muted = true;
    try { await v.play(); } catch(e) {}
    
    // Draw current frame
    const canvas = document.createElement('canvas');
    canvas.width = v.videoWidth || 720;
    canvas.height = v.videoHeight || 1280;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(v, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg', 0.9);
  }, mainIdx);

  if (frame) {
    const base64Data = frame.replace(/^data:image\/jpeg;base64,/, "");
    fs.writeFileSync("/Volumes/Data/gobi-social/shots/main_hanhan_center.jpg", base64Data, 'base64');
    console.log("Saved main video to shots/main_hanhan_center.jpg");
  }
}

await task.finish({ keep: [] });
