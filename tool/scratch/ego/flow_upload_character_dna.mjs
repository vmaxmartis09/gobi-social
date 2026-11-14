/**
 * Upload Gobi Master DNA to Google Flow Character Creator
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

// Inspect file inputs and upload buttons
const uploadInfo = await page.evaluate(() => {
  const fileInputs = Array.from(document.querySelectorAll("input[type='file']")).map(inp => ({
    id: inp.id,
    className: inp.className,
    accept: inp.getAttribute('accept')
  }));

  const uploadBtn = Array.from(document.querySelectorAll("button, [role='button']")).find(b => (b.innerText || '').includes("Tải lên"));

  return { fileInputs, uploadBtnFound: !!uploadBtn };
});

console.log("[Ego] Upload Info:", JSON.stringify(uploadInfo, null, 2));

const masterDna = "/Volumes/Data/gobi-social/assets/datasets/koc/MASTER_KOC_DNA.jpg";

// If file input exists, use setInputFiles directly; if not, use waitForFileChooser
let fileUploaded = false;
if (uploadInfo.fileInputs.length > 0) {
  console.log("[Ego] Setting input files directly...");
  await page.evaluate(() => {
    const inputs = document.querySelectorAll("input[type='file']");
    if (inputs[0]) inputs[0].id = "flow_character_upload_input";
  });
  await page.setInputFiles("#flow_character_upload_input", [masterDna]);
  fileUploaded = true;
} else {
  console.log("[Ego] Triggering file chooser via button click...");
  const chooserPromise = page.waitForFileChooser({ timeout: 10000 });
  await page.evaluate(() => {
    const uploadBtn = Array.from(document.querySelectorAll("button, [role='button']")).find(b => (b.innerText || '').includes("Tải lên"));
    if (uploadBtn) uploadBtn.click();
  });
  try {
    const chooser = await chooserPromise;
    await chooser.setFiles(masterDna);
    fileUploaded = true;
    console.log("[Ego] File chooser set files successfully!");
  } catch (err) {
    console.log("[!] File chooser error:", err.message);
  }
}

await page.waitForTimeout(5000);

// Screenshot after upload
const shotAfterUpload = "/Volumes/Data/gobi-social/shots/google_flow_character_uploaded.png";
await page.screenshot({ path: shotAfterUpload });
console.log("[Ego] Character uploaded screenshot saved to:", shotAfterUpload);

// Inspect name input or prompt input
const charState = await page.evaluate(() => {
  const inputs = Array.from(document.querySelectorAll("input, textarea, [contenteditable='true']")).map(el => ({
    tag: el.tagName,
    type: el.getAttribute('type'),
    placeholder: el.getAttribute('placeholder') || el.innerText,
    value: el.value || ''
  }));
  const buttons = Array.from(document.querySelectorAll("button, [role='button']")).map(b => (b.innerText || '').trim()).filter(Boolean);
  return { inputs, buttons: buttons.slice(0, 15) };
});

console.log("[Ego] State After Character Upload:", JSON.stringify(charState, null, 2));

await task.finish({ keep: [page.label] });
