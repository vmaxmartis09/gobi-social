/**
 * Configure Video mode, 9:16, Gobi character, and generate video on Google Flow
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const projectUrl = "https://flow.google.com/project/97437688-2b73-4a07-9091-77969b802e73";
await page.goto(projectUrl, { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);

// 1. Open settings popover
console.log("[Ego] Opening settings popover...");
await page.click(".settings-trigger-button");
await page.waitForTimeout(1000);

// 2. Select "Video" mode
console.log("[Ego] Switching to Video mode...");
await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, [role='button'], .mat-button-toggle-button"));
  const videoBtn = buttons.find(b => (b.innerText || '').includes("Video"));
  if (videoBtn) videoBtn.click();
});
await page.waitForTimeout(1000);

// 3. Select 9:16 aspect ratio
console.log("[Ego] Selecting 9:16 aspect ratio...");
await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, [role='button'], .mat-button-toggle-button"));
  const ratioBtn = buttons.find(b => (b.innerText || '').includes("9:16"));
  if (ratioBtn) ratioBtn.click();
});
await page.waitForTimeout(1000);

// Close settings popover via Escape key
console.log("[Ego] Closing settings popover via Escape key...");
await page.keyboard.press("Escape");
await page.waitForTimeout(1500);

// 4. Select Gobi Character
console.log("[Ego] Selecting Gobi character...");
await page.evaluate(() => {
  const agentChip = document.querySelector(".agent-mode-chip") || 
                    Array.from(document.querySelectorAll("button, div")).find(el => (el.innerText || '').includes("Tác nhân"));
  if (agentChip) agentChip.click();
});
await page.waitForTimeout(1500);

// Select Gobi from dropdown if present
const gobiSelected = await page.evaluate(() => {
  const items = Array.from(document.querySelectorAll("[role='menuitem'], .mat-mdc-menu-item, [class*='character'], [class*='option']"));
  const gobiItem = items.find(el => (el.innerText || '').includes("Gobi"));
  if (gobiItem) {
    gobiItem.click();
    return true;
  }
  return false;
});
console.log("[Ego] Gobi character selected from menu:", gobiSelected);
await page.waitForTimeout(1000);

// Close any open menu
await page.keyboard.press("Escape");
await page.waitForTimeout(500);

// 5. Enter prompt into ProseMirror
console.log("[Ego] Typing prompt for Gobi wearing NEAU NuNu NU221 shirt...");
await page.click(".ProseMirror");
await page.waitForTimeout(500);

const videoPrompt = "Gobi, co gai KOC thoi trang Viet Nam 22 tuoi, mac chiec ao thun om dai tay mau xam tieu NEAU NuNu NU221, mim cuoi rang ro voi camera, nhe nhang dung tay keo nhe mep co ao the hien do co gian dan hoi cuc em ai, chuyen dong tu nhien 4k.";
await page.keyboard.type(videoPrompt, { delay: 15 });
await page.waitForTimeout(1500);

// 6. Check if generate button is enabled
const canGenerate = await page.evaluate(() => {
  const btn = document.querySelector(".generate-icon-button") || 
              Array.from(document.querySelectorAll("button")).find(b => (b.innerText || b.getAttribute('aria-label') || '').includes("arrow_forward"));
  return btn ? {
    found: true,
    disabled: btn.disabled || btn.classList.contains("mat-mdc-button-disabled")
  } : { found: false };
});

console.log("[Ego] Generate Button State:", JSON.stringify(canGenerate));

const shotBeforeGen = "/Volumes/Data/gobi-social/shots/google_flow_ready_to_gen_video.png";
await page.screenshot({ path: shotBeforeGen });
console.log("[Ego] Ready screenshot saved to:", shotBeforeGen);

// 7. Click Generate
if (canGenerate.found && !canGenerate.disabled) {
  console.log("[Ego] Clicking Generate Video in Google Flow...");
  await page.click(".generate-icon-button");
  console.log("[Ego] Generation triggered successfully!");
  await page.waitForTimeout(8000);
}

const shotGenStarted = "/Volumes/Data/gobi-social/shots/google_flow_video_gen_started.png";
await page.screenshot({ path: shotGenStarted });
console.log("[Ego] Generation started screenshot saved to:", shotGenStarted);

await task.finish({ keep: [page.label] });
