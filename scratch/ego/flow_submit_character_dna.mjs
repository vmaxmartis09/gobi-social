/**
 * Submit Gobi Master DNA and create persistent character in Google Flow
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

// Click "Tải lên" to ensure file input is mounted
await page.evaluate(() => {
  const uploadBtn = Array.from(document.querySelectorAll("button, [role='button']")).find(b => (b.innerText || '').includes("Tải lên"));
  if (uploadBtn) uploadBtn.click();
});
await page.waitForTimeout(1000);

// Assign ID to input[type='file']
const inputIdAssigned = await page.evaluate(() => {
  const fileInput = document.querySelector("input[type='file']");
  if (fileInput) {
    fileInput.id = "flow_char_file_input";
    return true;
  }
  return false;
});
console.log("[Ego] File input ID assigned:", inputIdAssigned);

const masterDna = "/Volumes/Data/gobi-social/assets/datasets/koc/MASTER_KOC_DNA.jpg";

if (inputIdAssigned) {
  console.log("[Ego] Setting input files to Gobi Master DNA...");
  await page.setInputFiles("#flow_char_file_input", [masterDna]);
  console.log("[Ego] File setInputFiles called successfully!");
}

await page.waitForTimeout(4000);

// Enter Character prompt / description
const charPrompt = "Gobi, a 22-year-old Vietnamese female fashion KOC model, delicate facial features, radiant healthy skin, slim athletic build, gentle and confident expression.";

const descEntered = await page.evaluate((text) => {
  const editor = document.querySelector(".ProseMirror, textarea, [contenteditable='true']");
  if (editor) {
    editor.focus();
    if (editor.tagName === "TEXTAREA" || editor.tagName === "INPUT") {
      editor.value = text;
      editor.dispatchEvent(new Event('input', { bubbles: true }));
      editor.dispatchEvent(new Event('change', { bubbles: true }));
    } else {
      editor.innerHTML = `<p>${text}</p>`;
      editor.dispatchEvent(new Event('input', { bubbles: true }));
    }
    return true;
  }
  return false;
}, charPrompt);

console.log("[Ego] Character prompt entered:", descEntered);
await page.waitForTimeout(2000);

// Check if submit / arrow_forward button is enabled
const submitStatus = await page.evaluate(() => {
  const submitBtn = Array.from(document.querySelectorAll("button")).find(b => {
    const t = (b.innerText || b.getAttribute('aria-label') || '').toLowerCase();
    return t.includes("arrow_forward") || t.includes("bắt đầu") || t.includes("tạo") || t.includes("generate");
  });
  return submitBtn ? {
    found: true,
    text: submitBtn.innerText || submitBtn.getAttribute('aria-label'),
    disabled: submitBtn.disabled || submitBtn.classList.contains("mat-mdc-button-disabled")
  } : { found: false };
});

console.log("[Ego] Submit Button Status:", JSON.stringify(submitStatus, null, 2));

const shotCharCreated = "/Volumes/Data/gobi-social/shots/google_flow_character_submitting.png";
await page.screenshot({ path: shotCharCreated });
console.log("[Ego] Screenshot saved to:", shotCharCreated);

// If enabled, let's click it!
if (submitStatus.found && !submitStatus.disabled) {
  console.log("[Ego] Clicking create character button...");
  await page.evaluate(() => {
    const submitBtn = Array.from(document.querySelectorAll("button")).find(b => {
      const t = (b.innerText || b.getAttribute('aria-label') || '').toLowerCase();
      return t.includes("arrow_forward") || t.includes("bắt đầu") || t.includes("tạo") || t.includes("generate");
    });
    if (submitBtn) submitBtn.click();
  });
  await page.waitForTimeout(6000);
}

const shotFinal = "/Volumes/Data/gobi-social/shots/google_flow_character_final.png";
await page.screenshot({ path: shotFinal });
console.log("[Ego] Final screenshot saved to:", shotFinal);

await task.finish({ keep: [page.label] });
