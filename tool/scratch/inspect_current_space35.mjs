import fs from "fs";
const task = await claimTaskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
if (!chatgptTab) { console.log("No tab"); process.exit(1); }
const page = chatgptTab.page;

const state = await page.evaluate(() => {
  const imgs = Array.from(document.querySelectorAll("img[alt*=\"Generated\"]"));
  const text = document.body.innerText;
  const isGenerating = !!document.querySelector("button[aria-label=\"Stop generating\"], [data-testid=\"stop-button\"]");
  const limitReached = text.includes("limit") && (text.includes("image") || text.includes("attachment") || text.includes("free") || text.includes("Upgrade"));
  return {
    url: window.location.href,
    imageCount: imgs.length,
    isGenerating,
    limitReached,
    tailText: text.slice(-400)
  };
});
console.log("Current ChatGPT State:", JSON.stringify(state, null, 2));
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/live_status_check.png" });
