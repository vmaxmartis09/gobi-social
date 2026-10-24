/**
 * Rename the character to "Gobi" in Google Flow using evaluate click
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const projectUrl = "https://flow.google.com/project/b3c2d9f6-d452-40a2-96f6-c7c92fd7bf7a";
await page.goto(projectUrl, { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);

// Navigate to "Nhân vật"
await page.evaluate(() => {
  const listItems = Array.from(document.querySelectorAll("mat-list-item, .mat-mdc-list-item"));
  const charItem = listItems.find(el => el.innerText.includes("Nhân vật"));
  if (charItem) charItem.click();
});
await page.waitForTimeout(2500);

// Click first character tile
console.log("[Ego] Opening first character tile...");
await page.evaluate(() => {
  const tiles = document.querySelectorAll(".character-tile-container");
  if (tiles[0]) tiles[0].click();
});
await page.waitForTimeout(3000);

// Check if a rename input or detail panel opened
const renameState = await page.evaluate(() => {
  const inputs = Array.from(document.querySelectorAll("input, textarea")).map(inp => ({
    value: inp.value,
    className: inp.className,
    placeholder: inp.getAttribute('placeholder')
  }));
  const buttons = Array.from(document.querySelectorAll("button")).map(b => (b.innerText || b.getAttribute('aria-label') || '').trim()).filter(Boolean);

  return { inputs, buttons: buttons.slice(0, 15) };
});

console.log("[Ego] Rename State:", JSON.stringify(renameState, null, 2));

// Rename to "Gobi"
const renamed = await page.evaluate(() => {
  const nameInput = document.querySelector(".editable-text-input, input[value*='Nhân vật chưa có tên'], input[placeholder*='Tên']");
  if (nameInput) {
    nameInput.focus();
    nameInput.value = "Gobi";
    nameInput.dispatchEvent(new Event('input', { bubbles: true }));
    nameInput.dispatchEvent(new Event('change', { bubbles: true }));
    nameInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true }));
    return { success: true };
  }
  return { success: false };
});

console.log("[Ego] Rename Action:", JSON.stringify(renamed));
await page.waitForTimeout(2000);

const shotRenamed = "/Volumes/Data/gobi-social/shots/google_flow_character_renamed_gobi.png";
await page.screenshot({ path: shotRenamed });
console.log("[Ego] Renamed screenshot saved to:", shotRenamed);

await task.finish({ keep: [page.label] });
