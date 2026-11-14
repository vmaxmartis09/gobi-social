const task = await taskSpace("Google Flow Inspect Buttons");
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

// Inspect all buttons, icons, file inputs, tooltips inside the character modal
const modalAnalysis = await page.evaluate(() => {
  const allButtons = Array.from(document.querySelectorAll("button, [role='button'], mat-icon, .clickable, input[type='file']")).map(b => ({
    tag: b.tagName,
    text: (b.innerText || '').trim().replace(/\n+/g, ' '),
    aria: b.getAttribute('aria-label') || '',
    className: b.className,
    type: b.getAttribute('type') || ''
  }));

  const textareas = Array.from(document.querySelectorAll("textarea, input[type='text'], .editable-text-input")).map(t => ({
    className: t.className,
    value: t.value || t.innerText || ''
  }));

  return { allButtons, textareas };
});

console.log("[Ego] Modal Analysis:", JSON.stringify(modalAnalysis, null, 2));

await task.finish({ keep: ["p1"] });
