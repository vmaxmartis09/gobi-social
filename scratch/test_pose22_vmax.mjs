import fs from "fs";
import path from "path";

const TARGET_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36";
const MASTER_DNA = path.join(TARGET_DIR, "00_MASTER_DNA_ANCHOR.jpg");
const BEAUTY_REF = path.join(TARGET_DIR, "gobi_angle_01_front_beauty.jpg");
const POSE_22_REF = "/Volumes/Data/gobi-social/assets/datasets/koc/old_reference_poses/22_goc_ngang_hong.jpg";
const TARGET_FILE = path.join(TARGET_DIR, "gobi_angle_22_goc_ngang_hong.jpg");

const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

console.log("[Pose 22] Attaching 3 reference files...");
await page.setInputFiles("input[aria-label=\"Attach photos\"]", [MASTER_DNA, BEAUTY_REF, POSE_22_REF]);

console.log("[Pose 22] Waiting 6s for uploads to complete...");
await new Promise(r => setTimeout(r, 6000));
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/pose22_vmax_attached.png" });

// Check upload status
const uploadStatus = await page.evaluate(() => {
  const bodyText = document.body.innerText;
  const failed = bodyText.includes("Upload failed");
  const limit = bodyText.includes("limit for file attachments");
  return { failed, limit, bodySnippet: bodyText.slice(-300) };
});
console.log("[Pose 22] Upload status:", uploadStatus);

if (uploadStatus.failed || uploadStatus.limit) {
  console.error("[Pose 22] Upload error detected:", uploadStatus);
  process.exit(1);
}

// Paste prompt
const promptText = `STRICT MULTI-REFERENCE CONDITIONING:
1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical eyes, nose bridge, lips, hair color and cream silk outfit).
2. BODY POSE & CAMERA ANGLE: Match the exact body pose, camera angle, and posture shown in the attached pose reference image (Pose #22: Góc ngang hông). Waist/hip-level shot of this exact woman standing with one hand resting naturally on her hip, chic effortless poise, draped knit cardigan, 8k. Editorial studio lighting, sharp focus, 8k resolution.`;

console.log("[Pose 22] Pasting prompt...");
await page.click("div[contenteditable=true], #prompt-textarea, textarea");
await page.keyboard.paste({ text: promptText });
await new Promise(r => setTimeout(r, 1200));

console.log("[Pose 22] Submitting prompt...");
await page.keyboard.press("Enter");

console.log("[Pose 22] Monitoring generation...");
let done = false;
for (let poll = 0; poll < 45; poll++) {
  await new Promise(r => setTimeout(r, 3000));
  const status = await page.evaluate(() => {
    const isGenerating = !!document.querySelector("button[aria-label=\"Stop generating\"], [data-testid=\"stop-button\"]");
    const imgs = Array.from(document.querySelectorAll("img[alt*=\"Generated\"]"));
    return {
      isGenerating,
      imgCount: imgs.length
    };
  });

  console.log(`[Pose 22] Poll ${poll + 1}: generating=${status.isGenerating}, imgs=${status.imgCount}`);
  if (!status.isGenerating && status.imgCount > 0 && poll > 3) {
    console.log(`[Pose 22] Generation complete!`);
    done = true;
    break;
  }
}

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/pose22_vmax_result.png" });

if (done) {
  console.log("[Pose 22] Downloading generated image blob...");
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
    fs.writeFileSync(TARGET_FILE, Buffer.from(data, "base64"));
    const stats = fs.statSync(TARGET_FILE);
    console.log(`[Pose 22] SUCCESS! Saved ${(stats.size / 1024 / 1024).toFixed(2)} MB to ${TARGET_FILE}`);
  }
}
