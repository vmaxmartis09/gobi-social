/**
 * Click "Nhân vật" / "Tác nhân" in Google Flow project
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const projectUrl = "https://flow.google.com/project/b3c2d9f6-d452-40a2-96f6-c7c92fd7bf7a";
console.log("[Ego] Opening Flow Project:", projectUrl);
await page.goto(projectUrl, { waitUntil: "domcontentloaded", timeout: 35000 });
await page.waitForTimeout(4000);

// Click "Nhân vật" menu item
const charTabClicked = await page.evaluate(() => {
  const items = Array.from(document.querySelectorAll("mat-list-item, button, div, span"));
  const charItem = items.find(el => (el.innerText || '').includes("Nhân vật"));
  if (charItem) {
    charItem.click();
    return { success: true, text: charItem.innerText.trim() };
  }
  return { success: false };
});

console.log("[Ego] Clicked Character Tab:", JSON.stringify(charTabClicked));
await page.waitForTimeout(3000);

// Inspect buttons on the Character screen (e.g. "+ Tạo nhân vật" or "Thêm nhân vật")
const charScreenElements = await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, [role='button']")).map(b => ({
    text: (b.innerText || '').trim(),
    ariaLabel: b.getAttribute('aria-label'),
    className: b.className
  })).filter(b => b.text || b.ariaLabel);

  const fileInputs = Array.from(document.querySelectorAll("input[type='file']")).map(inp => ({
    className: inp.className,
    id: inp.id,
    accept: inp.getAttribute('accept')
  }));

  return { buttons: buttons.slice(0, 20), fileInputs };
});

console.log("[Ego] Character Screen Elements:", JSON.stringify(charScreenElements, null, 2));

const shotChar = "/Volumes/Data/gobi-social/shots/google_flow_character_screen.png";
await page.screenshot({ path: shotChar });
console.log("[Ego] Character screen screenshot saved to:", shotChar);

await task.finish({ keep: [page.label] });
