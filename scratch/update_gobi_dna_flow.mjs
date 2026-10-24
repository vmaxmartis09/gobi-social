const task = await taskSpace("Google Flow Update Gobi DNA");
const page = task.page("p1");

const url = "https://flow.google.com/project/97437688-2b73-4a07-9091-77969b802e73";
console.log("[Ego] Opening project:", url);
await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
await page.waitForTimeout(3000);

// Navigate to "Nhân vật"
await page.evaluate(() => {
  const all = Array.from(document.querySelectorAll("mat-list-item, .mat-mdc-list-item, button, div"));
  const target = all.find(el => (el.innerText || '').trim().includes("Nhân vật"));
  if (target) target.click();
});
await page.waitForTimeout(2000);

// Click "Gobi KOC"
await page.evaluate(() => {
  const tiles = Array.from(document.querySelectorAll(".character-tile-container, [class*='character']"));
  const gobiTile = tiles.find(t => (t.innerText || '').includes("Gobi"));
  if (gobiTile) gobiTile.click();
});
await page.waitForTimeout(2500);

// New Invariant DNA descriptor (Universal across all videos, no specific clothing/action)
const masterDnaPrompt = "Gobi, nữ KOC thời trang Việt Nam 22 tuổi. Gương mặt trái xoan thanh tú, mắt hạnh nhân hai mí tự nhiên sáng ngời, sống mũi cao thẳng thon gọn, môi cánh cung mềm mại rạng rỡ. Chiều cao 1m62, nặng 49kg, vóc dáng thon thả chuẩn người mẫu thời trang lookbook. Làn da trắng sứ mịn màng bắt sáng studio tự nhiên, mái tóc đen tuyền suôn mượt buông xõa vai. Thần thái thanh lịch, hiện đại phong cách Quiet Luxury, chi tiết chân thực chuẩn 8K điện ảnh.";

console.log("[Ego] Updating personality-textarea with Master Invariant DNA...");
const updated = await page.evaluate((newBio) => {
  const textarea = document.querySelector(".personality-textarea, textarea");
  if (textarea) {
    textarea.focus();
    textarea.value = newBio;
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    textarea.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  }
  return false;
}, masterDnaPrompt);

console.log("[Ego] Personality textarea updated:", updated);
await page.waitForTimeout(1000);

// Click "Xong" button to save changes
console.log("[Ego] Clicking 'Xong' to save character profile...");
const clickedSave = await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, [role='button']"));
  const doneBtn = buttons.find(b => (b.innerText || '').trim() === "Xong");
  if (doneBtn) {
    doneBtn.click();
    return true;
  }
  return false;
});
console.log("[Ego] Clicked 'Xong' button:", clickedSave);
await page.waitForTimeout(3000);

// Verify screenshot
const verifyShot = "/Volumes/Data/gobi-social/shots/ego_gobi_dna_updated_verified.png";
await page.screenshot({ path: verifyShot });
console.log("[Ego] Verified screenshot saved to:", verifyShot);

await task.finish({ keep: ["p1"] });
