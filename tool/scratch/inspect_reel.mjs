const task = await taskSpace("Inspect FB Reel");
const page = task.page("p1");

try {
  console.log("Navigating to Facebook reel with domcontentloaded...");
  await page.goto("https://www.facebook.com/reel/1104369265315017", { waitUntil: "domcontentloaded", timeout: 20000 });
  
  await new Promise(r => setTimeout(r, 5000));
  
  const title = await page.title();
  console.log("Page title:", title);
  
  const currentUrl = page.url();
  console.log("Current URL:", currentUrl);
  
  // Try closing any login dialog or close button
  try {
    const closeBtn = await page.$('[aria-label="Close"], [aria-label="Đóng"], div[role="button"]:has-text("Đóng"), div[role="button"]:has-text("Close")');
    if (closeBtn) {
      console.log("Found close button, clicking...");
      await closeBtn.click();
      await new Promise(r => setTimeout(r, 1000));
    }
  } catch (e) {
    console.log("No close button or error clicking it:", e.message);
  }

  await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/reel_screenshot.png" });
  console.log("Screenshot saved to /Volumes/Data/gobi-social/shots/reel_screenshot.png");
  
  const data = await page.evaluate(() => {
    return {
      text: document.body.innerText.slice(0, 4000),
      allVideos: Array.from(document.querySelectorAll('video')).map(v => ({
        src: v.src,
        currentSrc: v.currentSrc,
        duration: v.duration
      }))
    };
  });
  
  console.log("Page Text:\n", data.text);
  console.log("Videos:", JSON.stringify(data.allVideos, null, 2));

} catch (err) {
  console.error("Error inspecting reel:", err);
} finally {
  await task.finish({ keep: [] });
}
