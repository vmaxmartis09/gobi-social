const task = await taskSpace("Play Outfitsbyhan Video");
const page = task.page("p1");

await page.goto("https://www.tiktok.com/@outfitsbyhan.han/video/7697472862633921812");
await page.waitForLoadState();
await new Promise(r => setTimeout(r, 6000));

// Click center to play/unpause
await page.mouse.click(540, 500);

// Let's capture at 2s, 6s, 12s, 18s, 25s
const fs = await import('fs');

async function grabFrame(name) {
  const frameBase64 = await page.evaluate(() => {
    const v = document.querySelector('video');
    if (!v) return null;
    const canvas = document.createElement('canvas');
    canvas.width = v.videoWidth || 720;
    canvas.height = v.videoHeight || 1280;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(v, 0, 0, canvas.width, canvas.height);
    return { data: canvas.toDataURL('image/jpeg', 0.9), curTime: v.currentTime };
  });
  if (frameBase64) {
    const data = frameBase64.data.replace(/^data:image\/jpeg;base64,/, "");
    const file = `/Volumes/Data/gobi-social/shots/${name}.jpg`;
    fs.writeFileSync(file, data, 'base64');
    console.log(`Saved ${file} at currentTime ${frameBase64.curTime}`);
  }
}

await grabFrame("play_shot_0s");
await new Promise(r => setTimeout(r, 4000));
await grabFrame("play_shot_4s");
await new Promise(r => setTimeout(r, 6000));
await grabFrame("play_shot_10s");
await new Promise(r => setTimeout(r, 8000));
await grabFrame("play_shot_18s");
await new Promise(r => setTimeout(r, 10000));
await grabFrame("play_shot_28s");

await task.finish({ keep: [] });
