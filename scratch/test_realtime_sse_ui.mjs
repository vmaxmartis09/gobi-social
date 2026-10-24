const task = await taskSpace("Gobi Dashboard Realtime SSE Test");
const page = task.page("p1");

console.log("[Ego] Navigating to http://localhost:3000...");
await page.goto("http://localhost:3000", { waitUntil: "domcontentloaded", timeout: 15000 });
await page.waitForTimeout(3000);

// Screenshot 1: Verify REALTIME LIVE pill in Navbar
const shotLive = "/Volumes/Data/gobi-social/shots/dashboard_realtime_live_connected.png";
await page.screenshot({ path: shotLive });
console.log("[Ego] Realtime Live Connected saved to:", shotLive);

// Inspect the realtime indicator text in Navbar
const sseStatus = await page.evaluate(() => {
  const allTexts = Array.from(document.querySelectorAll("header span, header div")).map(el => (el.innerText || '').trim()).filter(Boolean);
  const liveIndicator = allTexts.find(t => t.includes("REALTIME LIVE") || t.includes("SYNCING"));
  return { liveIndicator, sampleHeaderTexts: allTexts.slice(0, 8) };
});
console.log("[Ego] SSE Status in DOM:", JSON.stringify(sseStatus, null, 2));

// Test real-time trigger: update product.json status of one product
console.log("[Ego] Testing real-time file change trigger...");
const fs = await import("node:fs");
const targetJson = "/Volumes/Data/gobi-social/data/products/7678960622423330066_ao_nay_tui_len_cho_may_ba_ao_thun_giay_tay_da/product.json";
if (fs.existsSync(targetJson)) {
  const content = JSON.parse(fs.readFileSync(targetJson, "utf-8"));
  content.status = "DANG_LAM";
  content.status_updated_at = new Date().toISOString();
  fs.writeFileSync(targetJson, JSON.stringify(content, null, 2), "utf-8");
  console.log("[Ego] Triggered file write on product.json!");
}

// Wait for SSE broadcast and React re-render
await page.waitForTimeout(2000);

// Screenshot 2: Verify that status changed in UI in real-time without page reload!
const shotUpdated = "/Volumes/Data/gobi-social/shots/dashboard_realtime_auto_updated.png";
await page.screenshot({ path: shotUpdated });
console.log("[Ego] Realtime Auto-Updated screenshot saved to:", shotUpdated);

await task.finish({ keep: ["p1"] });
