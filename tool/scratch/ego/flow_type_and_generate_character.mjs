/**
 * Type character prompt via keyboard and click generate in Google Flow
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
await page.waitForTimeout(2000);

// Click "Nhân vật mới"
await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, [role='button']"));
  const btn = buttons.find(b => (b.innerText || '').includes("Nhân vật mới"));
  if (btn) btn.click();
});
await page.waitForTimeout(2000);

// Focus ProseMirror editor and type character description
console.log("[Ego] Focusing editor and typing Gobi character prompt...");
await page.click(".ProseMirror");
await page.waitForTimeout(500);

const charPrompt = "Gobi, co gai KOC thoi trang Viet Nam 22 tuoi, guong mat thanh tu xinh dep, nu cuoi rang ro, voc dang thon gon manh mai, mac ao thun bodyfit hien dai.";
await page.keyboard.type(charPrompt, { delay: 20 });
await page.waitForTimeout(1500);

// Check if arrow_forward is now enabled
const btnStatus = await page.evaluate(() => {
  const genBtn = document.querySelector(".generate-icon-button") || 
                 Array.from(document.querySelectorAll("button")).find(b => (b.innerText || b.getAttribute('aria-label') || '').includes("arrow_forward"));
  return genBtn ? {
    found: true,
    disabled: genBtn.disabled || genBtn.classList.contains("mat-mdc-button-disabled")
  } : { found: false };
});

console.log("[Ego] Generate Button Status:", JSON.stringify(btnStatus));

const shotBeforeClick = "/Volumes/Data/gobi-social/shots/google_flow_char_prompt_typed.png";
await page.screenshot({ path: shotBeforeClick });
console.log("[Ego] Typed prompt screenshot saved to:", shotBeforeClick);

if (btnStatus.found && !btnStatus.disabled) {
  console.log("[Ego] Clicking Generate Character (arrow_forward)...");
  await page.click(".generate-icon-button");
  console.log("[Ego] Clicked generate successfully!");
  await page.waitForTimeout(6000);
}

const shotGenerating = "/Volumes/Data/gobi-social/shots/google_flow_char_generation_started.png";
await page.screenshot({ path: shotGenerating });
console.log("[Ego] Generation started screenshot saved to:", shotGenerating);

await task.finish({ keep: [page.label] });
