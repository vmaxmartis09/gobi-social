/**
 * Trigger Generate in Kling AI for Shot 1
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

await page.goto("https://kling.ai/app/creations/video", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

// Check if image and prompt are still populated, if not repopulate
const isReady = await page.evaluate(() => {
  const editor = document.querySelector(".tiptap.ProseMirror, [contenteditable='true']");
  const hasText = editor && editor.innerText.includes("Gobi");
  const hasImage = !!document.querySelector(".el-upload-list__item, [class*='preview-image'], [class*='upload-item'], img[src*='blob']");
  return { hasText, hasImage };
});

console.log("[Ego] Kling form ready status:", JSON.stringify(isReady));

if (!isReady.hasImage) {
  console.log("[Ego] Repopulating Start Frame image...");
  await page.evaluate(() => {
    const inputs = document.querySelectorAll("input[type='file']");
    if (inputs[0]) inputs[0].id = "kling_start_frame_input";
  });
  const testImage = "/Volumes/Data/gobi-social/assets/datasets/koc/campaign_neau/shot_01_hook.jpg";
  await page.setInputFiles("#kling_start_frame_input", [testImage]);
  await page.waitForTimeout(3000);
}

if (!isReady.hasText) {
  console.log("[Ego] Repopulating Prompt...");
  const promptText = "Cinematic medium close-up of Vietnamese girl Gobi wearing a tight heather grey bodyfit t-shirt. She looks directly into camera with an engaging smile, slightly tilts her head, and gently brushes a strand of hair behind her ear. Realistic breathing motion, natural cloth wrinkles shifting with movement, warm natural daylight, 4k ultra-realistic physics, 30fps.";
  await page.evaluate((text) => {
    const editor = document.querySelector(".tiptap.ProseMirror, [contenteditable='true']");
    if (editor) {
      editor.focus();
      editor.innerHTML = `<p>${text}</p>`;
      editor.dispatchEvent(new Event('input', { bubbles: true }));
      editor.dispatchEvent(new Event('change', { bubbles: true }));
    }
    const buttons = Array.from(document.querySelectorAll("button, div, span"));
    const ratio916 = buttons.find(b => (b.innerText || '').trim() === "9:16");
    if (ratio916) ratio916.click();
  }, promptText);
  await page.waitForTimeout(2000);
}

// Click Generate Button
console.log("[Ego] Clicking Generate button...");
const clickResult = await page.evaluate(() => {
  const genBtn = Array.from(document.querySelectorAll("button")).find(b => {
    const t = (b.innerText || '').trim();
    return t.startsWith("Generate") || t.includes("Generate");
  });
  if (genBtn && !genBtn.disabled && !genBtn.classList.contains("is-disabled")) {
    genBtn.click();
    return { success: true, text: genBtn.innerText };
  }
  return { success: false, text: genBtn ? genBtn.innerText : "Not found" };
});

console.log("[Ego] Click Result:", JSON.stringify(clickResult, null, 2));
await page.waitForTimeout(5000);

const shotAfterClick = "/Volumes/Data/gobi-social/shots/kling_after_generate_clicked.png";
await page.screenshot({ path: shotAfterClick });
console.log("[Ego] Post-click screenshot saved to:", shotAfterClick);

// Check if task / queue card appeared
const queueInfo = await page.evaluate(() => {
  const cards = Array.from(document.querySelectorAll("[class*='item'], [class*='card'], [class*='progress'], [class*='task']"))
    .map(el => (el.innerText || '').trim())
    .filter(t => t.includes("%") || t.toLowerCase().includes("generating") || t.toLowerCase().includes("queue") || t.toLowerCase().includes("waiting"));
  return cards.slice(0, 5);
});
console.log("[Ego] Queue info:", JSON.stringify(queueInfo));

await task.finish({ keep: [page.label] });
