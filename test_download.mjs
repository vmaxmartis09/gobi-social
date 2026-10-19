const task = await taskSpace("AI Flow Video Production");
const page = task.page("p2");

// Test downloading the video using Ego Lite's waitForEvent('download')
console.log("Preparing download...");
const downloadPromise = page.waitForEvent("download", { timeout: 15000 });

// Find the download button in the top bar
await page.evaluate(() => {
  const btn = document.querySelector('button[aria-label="Tải nội dung nghe nhìn xuống"]') || 
              document.querySelector('button[aria-label="Tải xuống"]');
  if (btn) {
    btn.click();
    console.log("Clicked download button");
  } else {
    console.log("Download button not found!");
  }
});

try {
  const download = await downloadPromise;
  console.log("Download triggered! URL:", download.url(), "Filename:", download.suggestedFilename());
  const savePath = "C:/Users/HAI/OneDrive/Tài liệu/vmax/shots/test_flow_download.mp4";
  await download.saveAs(savePath);
  console.log("Saved video to:", savePath);
} catch (e) {
  console.log("Download wait error:", e.message);
}
