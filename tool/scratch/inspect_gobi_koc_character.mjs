const task = await taskSpace("Google Flow Inspect Gobi KOC");
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

// Click "Gobi KOC" tile to open detail
console.log("[Ego] Clicking 'Gobi KOC' tile...");
const clickedTile = await page.evaluate(() => {
  const tiles = Array.from(document.querySelectorAll(".character-tile-container, [class*='character']"));
  const gobiTile = tiles.find(t => (t.innerText || '').includes("Gobi"));
  if (gobiTile) {
    gobiTile.click();
    return true;
  }
  return false;
});
console.log("[Ego] Clicked Gobi tile:", clickedTile);
await page.waitForTimeout(3000);

const detailShot = "/Volumes/Data/gobi-social/shots/ego_gobi_koc_detail.png";
await page.screenshot({ path: detailShot });
console.log("[Ego] Detail screenshot saved to:", detailShot);

// Inspect the modal / drawer / panel for Gobi KOC
const charDetails = await page.evaluate(() => {
  const images = Array.from(document.querySelectorAll("img")).map(img => ({
    src: img.src,
    alt: img.alt,
    className: img.className
  }));
  const textContent = Array.from(document.querySelectorAll("input, textarea, [class*='description'], [class*='prompt'], [class*='attribute'], [class*='detail']")).map(el => ({
    tag: el.tagName,
    value: el.value || el.innerText || '',
    className: el.className
  }));
  return { images: images.slice(0, 10), textContent: textContent.slice(0, 10) };
});

console.log("[Ego] Character Details:", JSON.stringify(charDetails, null, 2));

await task.finish({ keep: ["p1"] });
