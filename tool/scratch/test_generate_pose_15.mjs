import fs from "fs";
import path from "path";

const task = await taskSpace(35);
const p1 = task.page("p1");

const MASTER_DNA = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36/00_MASTER_DNA_ANCHOR.jpg";
const BEAUTY_REF = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36/gobi_angle_01_front_beauty.jpg";
const OLD_POSE_15 = "/Volumes/Data/gobi-social/assets/datasets/koc/old_reference_poses/15_goc_90_do_tren_xuong.jpg";

console.log("[Pose 15] Attaching 3 reference files...");
const fileInputSelector = "input[aria-label=\"Attach photos\"]";
await p1.setInputFiles(fileInputSelector, [MASTER_DNA, BEAUTY_REF, OLD_POSE_15]);

console.log("[Pose 15] Waiting 5s for attachments to upload...");
await new Promise(r => setTimeout(r, 5000));
await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/pose15_attached_preview.png" });

const promptText = `STRICT MULTI-REFERENCE CONDITIONING:
1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical eyes, nose bridge, lips, hair color and cream silk outfit).
2. BODY POSE & CAMERA ANGLE: Match the exact body pose, camera angle, and posture shown in the attached pose reference image (Pose #15: Góc 90 độ từ trên xuống). Top-down 90-degree aerial bird's eye view of this exact woman lying gracefully on a studio floor surface, hair splayed artistically, serene upward glance, 8k. Editorial studio lighting, sharp focus, 8k resolution.`;

console.log("[Pose 15] Typing prompt into textarea...");
await p1.click("div[contenteditable=true], #prompt-textarea, textarea");
await p1.keyboard.paste({ text: promptText });
await new Promise(r => setTimeout(r, 1000));

await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/pose15_ready_to_send.png" });

console.log("[Pose 15] Pressing Enter to generate...");
await p1.keyboard.press("Enter");

// Monitor generation
console.log("[Pose 15] Waiting for generation to complete...");
let done = false;
for (let i = 0; i < 40; i++) {
  await new Promise(r => setTimeout(r, 3000));
  const status = await p1.evaluate(() => {
    const text = document.body.innerText;
    const isGenerating = !!document.querySelector("button[aria-label=\"Stop generating\"], [data-testid=\"stop-button\"]");
    const imgs = Array.from(document.querySelectorAll("img[alt*=\"Generated\"]"));
    const errorBanner = text.includes("trouble processing uploads") || text.includes("limit") || text.includes("unusual activity");
    return {
      textTail: text.slice(-300),
      isGenerating,
      imgCount: imgs.length,
      errorBanner
    };
  });

  console.log(`[Pose 15] Poll ${i + 1}/40: generating=${status.isGenerating}, imgs=${status.imgCount}, error=${status.errorBanner}`);
  if (status.errorBanner) {
    console.log("[Pose 15] Error banner detected!");
    await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/pose15_error_banner.png" });
    break;
  }
  if (!status.isGenerating && status.imgCount > 0 && i > 3) {
    console.log("[Pose 15] Generation finished!");
    done = true;
    break;
  }
}

await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/pose15_final_state.png" });

if (done) {
  // Download latest image
  console.log("[Pose 15] Downloading generated image blob...");
  const base64Data = await p1.evaluate(async () => {
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
    const targetFile = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36/gobi_angle_15_goc_90_do_tren_xuong.jpg";
    const data = base64Data.replace(/^data:image\/\w+;base64,/, "");
    fs.writeFileSync(targetFile, Buffer.from(data, "base64"));
    const stats = fs.statSync(targetFile);
    console.log(`[Pose 15] Successfully saved Pose #15 (${(stats.size / 1024 / 1024).toFixed(2)} MB): ${targetFile}`);
  }
}
