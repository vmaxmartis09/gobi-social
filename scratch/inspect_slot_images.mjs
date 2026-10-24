const task = await taskSpace("Google Flow Check Slots");
const page = task.page("p1");

const url = "https://flow.google.com/project/97437688-2b73-4a07-9091-77969b802e73";
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

// Inspect slots and reference images
const slots = await page.evaluate(() => {
  const slotElements = Array.from(document.querySelectorAll(".character-slots-container, .character-slot, [class*='slot']")).map(s => ({
    className: s.className,
    text: (s.innerText || '').trim(),
    img: s.querySelector("img")?.src || null
  }));

  const buttons = Array.from(document.querySelectorAll("button, [role='button']")).map(b => (b.innerText || b.getAttribute('aria-label') || '').trim()).filter(Boolean);

  return { slotElements, buttons };
});

console.log("[Ego] Slots info:", JSON.stringify(slots, null, 2));

// Take a focused screenshot of the character editor modal
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/ego_gobi_char_editor_full.png" });

await task.finish({ keep: ["p1"] });
