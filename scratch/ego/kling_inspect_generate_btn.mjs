/**
 * Inspect and trigger Generate on Kling AI
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

await page.goto("https://kling.ai/app/creations/video", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

// Assign unique ID to file input
await page.evaluate(() => {
  const inputs = document.querySelectorAll("input[type='file']");
  if (inputs[0]) inputs[0].id = "kling_start_frame_input";
});

const testImage = "/Volumes/Data/gobi-social/assets/datasets/koc/campaign_neau/shot_01_hook.jpg";
await page.setInputFiles("#kling_start_frame_input", [testImage]);
await page.waitForTimeout(3000);

// Set prompt
const promptText = "Cinematic medium close-up of Vietnamese girl Gobi wearing a tight heather grey bodyfit t-shirt. She looks directly into camera with an engaging smile, slightly tilts her head, and gently brushes a strand of hair behind her ear. Realistic breathing motion, natural cloth wrinkles shifting with movement, warm natural daylight, 4k ultra-realistic physics, 30fps.";

await page.evaluate((text) => {
  const editor = document.querySelector(".tiptap.ProseMirror, [contenteditable='true']");
  if (editor) {
    editor.focus();
    editor.innerHTML = `<p>${text}</p>`;
    editor.dispatchEvent(new Event('input', { bubbles: true }));
    editor.dispatchEvent(new Event('change', { bubbles: true }));
  }
  // Set 9:16
  const buttons = Array.from(document.querySelectorAll("button, div, span"));
  const ratio916 = buttons.find(b => (b.innerText || '').trim() === "9:16");
  if (ratio916) ratio916.click();
}, promptText);

await page.waitForTimeout(2000);

// Find Generate button and its cost / state
const genState = await page.evaluate(() => {
  const genBtn = Array.from(document.querySelectorAll("button")).find(b => {
    const t = (b.innerText || '').trim();
    return t.startsWith("Generate") || t.includes("Generate");
  });
  return genBtn ? {
    text: genBtn.innerText,
    disabled: genBtn.disabled || genBtn.classList.contains("is-disabled"),
    className: genBtn.className
  } : null;
});

console.log("[Ego] Generate Button State:", JSON.stringify(genState, null, 2));

const shotPath = "/Volumes/Data/gobi-social/shots/kling_ready_to_generate.png";
await page.screenshot({ path: shotPath });
console.log("[Ego] Screenshot saved to:", shotPath);

await task.finish({ keep: [page.label] });
