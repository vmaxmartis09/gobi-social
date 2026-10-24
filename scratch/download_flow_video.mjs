const task = await taskSpace("Google Flow Download Video");
const page = task.page("p1");

const url = "https://flow.google.com/project/97437688-2b73-4a07-9091-77969b802e73";
await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
await page.waitForTimeout(4000);

const videoSrc = await page.evaluate(() => {
  const v = document.querySelector("video");
  return v ? (v.src || v.currentSrc) : null;
});

console.log("[Ego] Video source URL:", videoSrc);

if (videoSrc) {
  const savePath = "/Volumes/Data/gobi-social/output/flow_gobi_test_8s.mp4";
  console.log("[Ego] Downloading video to:", savePath);
  await page.fetch(videoSrc, { saveAs: savePath });
  console.log("[Ego] Video saved successfully!");
}

await task.finish({ keep: ["p1"] });
