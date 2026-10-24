/**
 * Click "Nhân vật quen thuộc" template in Google Flow Character Creator
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

// Click template "Nhân vật quen thuộc" (Chân thực và gần gũi)
console.log("[Ego] Clicking 'Nhân vật quen thuộc'...");
const templateClicked = await page.evaluate(() => {
  const cards = Array.from(document.querySelectorAll("button, div, [role='button']"));
  const card = cards.find(c => (c.innerText || '').includes("Nhân vật quen thuộc"));
  if (card) {
    card.click();
    return { success: true, text: card.innerText.slice(0, 50) };
  }
  return { success: false };
});

console.log("[Ego] Template clicked:", JSON.stringify(templateClicked));
await page.waitForTimeout(3000);

// Check what changed in the prompt input / buttons
const updatedState = await page.evaluate(() => {
  const editor = document.querySelector(".ProseMirror, textarea, [contenteditable='true']");
  const promptVal = editor ? (editor.value || editor.innerText) : '';
  const buttons = Array.from(document.querySelectorAll("button")).map(b => ({
    text: (b.innerText || b.getAttribute('aria-label') || '').trim(),
    disabled: b.disabled || b.classList.contains("mat-mdc-button-disabled")
  })).filter(b => b.text);

  return { promptVal, buttons: buttons.slice(0, 15) };
});

console.log("[Ego] Updated State:", JSON.stringify(updatedState, null, 2));

const shotTemplate = "/Volumes/Data/gobi-social/shots/google_flow_character_template_selected.png";
await page.screenshot({ path: shotTemplate });
console.log("[Ego] Template screenshot saved to:", shotTemplate);

// Now customize prompt with Gobi DNA
const customPrompt = "Gobi, cô gái Việt Nam 22 tuổi, gương mặt thanh tú, nụ cười rạng rỡ, vóc dáng thon gọn năng động, làn da sáng khỏe tự nhiên, phong cách thời trang trẻ trung hiện đại.";

console.log("[Ego] Updating prompt to Gobi KOC DNA...");
await page.evaluate((text) => {
  const editor = document.querySelector(".ProseMirror, [contenteditable='true']");
  if (editor) {
    editor.focus();
    editor.innerHTML = `<p>${text}</p>`;
    editor.dispatchEvent(new Event('input', { bubbles: true }));
  }
}, customPrompt);
await page.waitForTimeout(2000);

// Check submit button
const submitBtn = await page.evaluate(() => {
  const btn = Array.from(document.querySelectorAll("button")).find(b => {
    const t = (b.innerText || b.getAttribute('aria-label') || '').toLowerCase();
    return t.includes("tạo") || t.includes("arrow_forward") || t.includes("bắt đầu") || t.includes("generate");
  });
  if (btn && !btn.disabled && !btn.classList.contains("mat-mdc-button-disabled")) {
    btn.click();
    return { clicked: true, text: btn.innerText || btn.getAttribute('aria-label') };
  }
  return { clicked: false, text: btn ? (btn.innerText || btn.getAttribute('aria-label')) : 'None' };
});

console.log("[Ego] Submit Action:", JSON.stringify(submitBtn, null, 2));
await page.waitForTimeout(6000);

const shotAfterGen = "/Volumes/Data/gobi-social/shots/google_flow_character_generating.png";
await page.screenshot({ path: shotAfterGen });
console.log("[Ego] Generating screenshot saved to:", shotAfterGen);

await task.finish({ keep: [page.label] });
