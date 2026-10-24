/**
 * Upload Gobi DNA Shot and set Prompt in Kling AI via unique ID injection
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

console.log("[Ego] Connecting to Kling Video Creation...");
await page.goto("https://kling.ai/app/creations/video", {
  waitUntil: "domcontentloaded",
  timeout: 45000
});
await page.waitForTimeout(4000);

// 1. Dismiss any popups
await page.evaluate(() => {
  const gotIt = Array.from(document.querySelectorAll("button, span")).find(b => {
    const t = (b.innerText || '').toLowerCase();
    return t.includes("got it") || t.includes("accept") || t.includes("i know");
  });
  if (gotIt) gotIt.click();
});
await page.waitForTimeout(1000);

// 2. Assign unique IDs to the hidden file inputs
console.log("[Ego] Assigning unique IDs to file inputs...");
const inputCount = await page.evaluate(() => {
  const inputs = document.querySelectorAll("input[type='file']");
  if (inputs[0]) inputs[0].id = "kling_start_frame_input";
  if (inputs[1]) inputs[1].id = "kling_end_frame_input";
  return inputs.length;
});
console.log("[Ego] Total file inputs identified:", inputCount);

// 3. Upload Start Frame
const testImage = "/Volumes/Data/gobi-social/assets/datasets/koc/campaign_neau/shot_01_hook.jpg";
console.log("[Ego] Uploading Start Frame:", testImage);
await page.setInputFiles("#kling_start_frame_input", [testImage]);
console.log("[Ego] Successfully uploaded Start Frame!");

await page.waitForTimeout(4000);

// 4. Set the prompt into ProseMirror editor
console.log("[Ego] Entering interaction prompt...");
const promptText = "Cinematic medium close-up of Vietnamese girl Gobi wearing a tight heather grey bodyfit t-shirt. She looks directly into camera with an engaging smile, slightly tilts her head, and gently brushes a strand of hair behind her ear. Realistic breathing motion, natural cloth wrinkles shifting with movement, warm natural daylight, 4k ultra-realistic physics, 30fps.";

const promptSuccess = await page.evaluate((text) => {
  const editor = document.querySelector(".tiptap.ProseMirror, [contenteditable='true']");
  if (editor) {
    editor.focus();
    editor.innerHTML = `<p>${text}</p>`;
    editor.dispatchEvent(new Event('input', { bubbles: true }));
    editor.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  }
  return false;
}, promptText);

console.log("[Ego] Prompt populated:", promptSuccess);
await page.waitForTimeout(2000);

// 5. Select 9:16 Aspect Ratio if available
const aspectSet = await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, div, span"));
  const ratio916 = buttons.find(b => (b.innerText || '').trim() === "9:16");
  if (ratio916) {
    ratio916.click();
    return true;
  }
  return false;
});
console.log("[Ego] Set 9:16 ratio:", aspectSet);

await page.waitForTimeout(2000);

// 6. Screenshot to verify image and prompt are populated
const shotResult = "/Volumes/Data/gobi-social/shots/kling_prompt_and_image_populated.png";
await page.screenshot({ path: shotResult });
console.log("[Ego] Screenshot saved to:", shotResult);

// Keep the page open on user's screen
await task.finish({ keep: [page.label] });
