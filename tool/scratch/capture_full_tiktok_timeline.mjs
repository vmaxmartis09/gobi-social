const task = await taskSpace("Inspect TikTok Timeline");
const page = task.page("p1");

await page.goto("https://www.tiktok.com/@outfitsbyhan.han/video/7697472862633921812?_r=1&_t=ZS-9AgMU4r53Bt");
await page.waitForLoadState();
await new Promise(r => setTimeout(r, 4000));

const timestamps = [1, 3, 6, 9, 12];
const fs = await import('fs');

for (const ts of timestamps) {
  const frameDataUrl = await page.evaluate(async (time) => {
    const v = document.querySelector('video');
    if (!v) return null;
    v.currentTime = time;
    await new Promise(res => {
      v.onseeked = res;
      setTimeout(res, 800);
    });
    const canvas = document.createElement('canvas');
    canvas.width = v.videoWidth || 1080;
    canvas.height = v.videoHeight || 1920;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(v, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg', 0.85);
  }, ts);

  if (frameDataUrl) {
    const base64Data = frameDataUrl.replace(/^data:image\/jpeg;base64,/, "");
    const outPath = `/Volumes/Data/gobi-social/shots/tiktok_timeline_${ts}s.jpg`;
    fs.writeFileSync(outPath, base64Data, 'base64');
    console.log(`Saved frame at ${ts}s to ${outPath}`);
  }
}

// Also get audio or description
const desc = await page.evaluate(() => {
  return {
    desc: document.querySelector('[data-e2e="browse-video-desc"]')?.innerText || "",
    music: document.querySelector('[data-e2e="browse-music"]')?.innerText || ""
  };
});
console.log("Metadata:", desc);

await task.finish({ keep: [] });
