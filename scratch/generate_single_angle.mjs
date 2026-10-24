import fs from "fs";
import path from "path";

const TARGET_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36";
const MASTER_DNA = path.join(TARGET_DIR, "00_MASTER_DNA_ANCHOR.jpg");
const SHOTS_DIR = "/Volumes/Data/gobi-social/shots";

const ANGLE = {
  id: 4,
  code: "gobi_angle_04_half_body_waist",
  title: "Upper Body / Waist-up shot",
  prompt: "Generate Image #4: A medium waist-up portrait of this exact same woman standing naturally in studio. Showing both shoulders, delicate collarbone, cream silk camisole and light beige ribbed knit cardigan draped softly over her shoulders. Friendly direct gaze at camera, subtle natural smile, 85mm portrait, 8k."
};

const targetFile = path.join(TARGET_DIR, `${ANGLE.code}.jpg`);

console.log(`[Gobi Generator] Claiming TaskSpace 35...`);
const task = await claimTaskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
if (!chatgptTab) {
  console.error("ChatGPT tab not found!");
  process.exit(1);
}
const page = chatgptTab.page;

// Collect reference images
const existingFiles = fs.readdirSync(TARGET_DIR)
  .filter(f => f.endsWith(".jpg") && f !== `${ANGLE.code}.jpg`)
  .sort();

console.log("Existing files:", existingFiles);

// Always include Master DNA + up to 3 most recent
const refImages = [MASTER_DNA];
const otherImgs = existingFiles
  .filter(f => !f.includes("00_MASTER_DNA"))
  .map(f => path.join(TARGET_DIR, f));

// Take last 3 generated images
const recents = otherImgs.slice(-3);
for (const img of recents) {
  if (!refImages.includes(img)) refImages.push(img);
}

console.log(`[Gobi Generator] Attaching ${refImages.length} references:`, refImages.map(p => path.basename(p)));

// Count images currently in chat
const initialImgCount = await page.evaluate(() => {
  return document.querySelectorAll("img[alt*=\"Generated\"]").length;
});
console.log(`Current images in chat: ${initialImgCount}`);

// Attach reference images
console.log(`Attaching images via input[aria-label="Attach photos"]...`);
await page.setInputFiles("input[aria-label=\"Attach photos\"]", refImages);
await page.waitForTimeout(4000);

// Check if any error or quota dialog popped up
const pageCheck = await page.evaluate(() => {
  const text = document.body.innerText;
  return {
    hasLimitText: text.includes("limit") && (text.includes("attachment") || text.includes("upload") || text.includes("Upgrade")),
    thumbnailsCount: document.querySelectorAll("img[alt*=\"Uploaded\"], div[class*=\"thumbnail\"], [data-testid*=\"attachment\"]").length
  };
});
console.log("Attachment check:", pageCheck);

if (pageCheck.hasLimitText) {
  console.log("LIMIT DETECTED ON CURRENT ACCOUNT!");
  await page.screenshot({ path: path.join(SHOTS_DIR, "chatgpt_limit_hit.png") });
  process.exit(2);
}

// Prepare prompt
const fullPrompt = `STRICT IDENTITY CONDITIONING: You must generate the EXACT SAME WOMAN as shown in the attached reference images. Maintain 100% identical facial features, bone structure, eye shape, nose bridge, lips, hair color and cream silk outfit. ${ANGLE.prompt}`;

console.log("Typing prompt...");
await page.click("div[contenteditable=true], #prompt-textarea, textarea");
await page.keyboard.paste({ text: fullPrompt });
await page.waitForTimeout(1000);

// Click send or press Enter
console.log("Submitting prompt...");
await page.keyboard.press("Enter");

console.log("Waiting for image generation (monitoring image count)...");
let newImageFound = false;

for (let i = 0; i < 40; i++) { // wait up to 80 seconds
  await page.waitForTimeout(2000);
  const currentCount = await page.evaluate(() => {
    return document.querySelectorAll("img[alt*=\"Generated\"]").length;
  });
  
  if (currentCount > initialImgCount) {
    console.log(`New image detected! Count went from ${initialImgCount} to ${currentCount}`);
    newImageFound = true;
    break;
  }
  
  // Check for error messages
  const errText = await page.evaluate(() => {
    const errEl = document.querySelector(".text-red-500, [class*=\"error\"], [data-testid*=\"error\"]");
    return errEl ? errEl.innerText : null;
  });
  if (errText) {
    console.log("Error in chat:", errText);
    break;
  }
}

if (!newImageFound) {
  console.log("Waiting an extra 15 seconds to be sure...");
  await page.waitForTimeout(15000);
}

// Download latest image
console.log("Extracting latest image base64...");
const base64Data = await page.evaluate(async () => {
  const imgs = Array.from(document.querySelectorAll("img[alt*=\"Generated\"]"));
  const latestImg = imgs[imgs.length - 1];
  if (!latestImg) return null;
  const response = await fetch(latestImg.src);
  const blob = await response.blob();
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
});

if (base64Data) {
  const data = base64Data.replace(/^data:image\/\w+;base64,/, "");
  fs.writeFileSync(targetFile, Buffer.from(data, "base64"));
  const stats = fs.statSync(targetFile);
  console.log(`Successfully saved ${targetFile} (${(stats.size / 1024 / 1024).toFixed(2)} MB)`);
} else {
  console.error("Failed to extract base64 data!");
}

const shotPath = path.join(SHOTS_DIR, `chatgpt_step_${ANGLE.code}.png`);
await page.screenshot({ path: shotPath });
console.log(`Screenshot saved to ${shotPath}`);
