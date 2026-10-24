/**
 * Click "add\nNhân vật mới" in Google Flow
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
await page.waitForTimeout(3000);

// Click "add\nNhân vật mới"
console.log("[Ego] Clicking 'Nhân vật mới' button...");
const clickedNewChar = await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, [role='button']"));
  const btn = buttons.find(b => (b.innerText || '').includes("Nhân vật mới"));
  if (btn) {
    btn.click();
    return { success: true, text: btn.innerText.trim() };
  }
  return { success: false };
});

console.log("[Ego] Clicked 'Nhân vật mới':", JSON.stringify(clickedNewChar));
await page.waitForTimeout(4000);

// Inspect newly opened screen/dialog
const charDialogInfo = await page.evaluate(() => {
  const allText = document.body.innerText.slice(0, 800);
  const buttons = Array.from(document.querySelectorAll("button, [role='button']")).map(b => ({
    text: (b.innerText || b.getAttribute('aria-label') || '').trim(),
    className: b.className
  })).filter(b => b.text);

  const inputs = Array.from(document.querySelectorAll("input, textarea, [contenteditable='true']")).map(inp => ({
    tag: inp.tagName,
    type: inp.getAttribute('type'),
    placeholder: inp.getAttribute('placeholder'),
    className: inp.className
  }));

  return { allText, buttons: buttons.slice(0, 20), inputs };
});

console.log("[Ego] Character Dialog Info:", JSON.stringify(charDialogInfo, null, 2));

const shotDialog = "/Volumes/Data/gobi-social/shots/google_flow_new_char_dialog.png";
await page.screenshot({ path: shotDialog });
console.log("[Ego] Screenshot saved to:", shotDialog);

await task.finish({ keep: [page.label] });
