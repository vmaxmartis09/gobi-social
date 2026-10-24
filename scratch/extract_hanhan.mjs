const task = await taskSpace("Extract Outfitsbyhan Frames");
const page = task.page("p1");

console.log("Navigating to video...");
await page.goto("https://www.tiktok.com/@outfitsbyhan.han/video/7697472862633921812");

// Wait 8s for TikTok to hydrate completely
await new Promise(r => setTimeout(r, 8000));

// Unpause video
await page.evaluate(async () => {
  const v = document.querySelector('video');
  if (v) {
    v.muted = true;
    try { await v.play(); } catch(e) {}
  }
});

await new Promise(r => setTimeout(r, 2000));

// Capture frames at specific points in the 52s video
const times = [2, 10, 20, 30, 40];
const fs = await import('fs');

for (const t of times) {
  const frameBase64 = await page.evaluate(async (time) => {
    const v = document.querySelector('video');
    if (!v) return null;
    v.currentTime = time;
    await new Promise(resolve => {
      const handler = () => {
        v.removeEventListener('seeked', handler);
        resolve();
      };
      v.addEventListener('seeked', handler);
      setTimeout(resolve, 1500);
    });

    const canvas = document.createElement('canvas');
    canvas.width = v.videoWidth || 720;
    canvas.height = v.videoHeight || 1280;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(v, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg', 0.9);
  }, t);

  if (frameBase64) {
    const data = frameBase64.replace(/^data:image\/jpeg;base64,/, "");
    const file = `/Volumes/Data/gobi-social/shots/hanhan_frame_${t}s.jpg`;
    fs.writeFileSync(file, data, 'base64');
    console.log(`Saved: ${file}`);
  }
}

// Get caption and tags
const details = await page.evaluate(() => {
  const text = document.querySelector('[data-e2e="browse-video-desc"]')?.innerText 
    || document.querySelector('h1')?.innerText 
    || document.querySelector('.css-10n21e5-DivContainer')?.innerText
    || "";
  return { text };
});
console.log("Video Description:", details);

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/hanhan_full_page.png" });

await task.finish({ keep: [] });
