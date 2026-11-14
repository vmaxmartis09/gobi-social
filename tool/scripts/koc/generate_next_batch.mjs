import fs from "fs";
import path from "path";

const TARGET_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36";
const MASTER_DNA = path.join(TARGET_DIR, "00_MASTER_DNA_ANCHOR.jpg");
const BEAUTY_REF = path.join(TARGET_DIR, "gobi_angle_01_front_beauty.jpg");
const OLD_POSES_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/old_reference_poses";
const SHOTS_DIR = "/Volumes/Data/gobi-social/shots";
const CONFIG_PATH = "/Volumes/Data/gobi-social/configs/koc_gobi_36_poses.json";

function loadPoses() {
  return JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
}

function getExistingPoseFile(padded) {
  const files = fs.readdirSync(TARGET_DIR);
  return files.find(f => f.startsWith(`gobi_angle_${padded}_`) && f.endsWith(".jpg"));
}

async function runBatch() {
  console.log("===============================================================");
  console.log("=== GOBI 36: GENERATING REMAINING POSES (22 TO 36) ===");
  console.log("===============================================================");

  const task = await taskSpace(35);
  const tabs = await task.tabs();
  let chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
  if (!chatgptTab) {
    console.error("ChatGPT tab not found in space 35!");
    process.exit(1);
  }
  const page = chatgptTab.page;

  const poses = loadPoses();
  const remainingPoses = poses.filter(p => p.id >= 22 && p.id <= 36);

  for (const pose of remainingPoses) {
    const padded = String(pose.id).padStart(2, "0");
    const existing = getExistingPoseFile(padded);
    if (existing) {
      const stats = fs.statSync(path.join(TARGET_DIR, existing));
      if (stats.size > 200000) {
        console.log(`[Batch] Pose #${pose.id} (${pose.title}) already exists (${(stats.size / 1024 / 1024).toFixed(2)} MB), skipping.`);
        continue;
      }
    }

    const oldPoseFile = path.join(OLD_POSES_DIR, pose.pose_ref);
    if (!fs.existsSync(oldPoseFile)) {
      console.warn(`[Batch] Pose reference file missing: ${oldPoseFile}`);
      continue;
    }

    const targetFilename = `gobi_angle_${padded}_${pose.pose_ref.replace(/\.jpg$/, "")}.jpg`;
    const targetPath = path.join(TARGET_DIR, targetFilename);

    console.log(`\n===============================================================`);
    console.log(`[Batch] GENERATING POSE #${pose.id} / 36: ${pose.title}`);
    console.log(`[Batch] Reference: ${pose.pose_ref}`);
    console.log(`[Batch] Target: ${targetFilename}`);
    console.log(`===============================================================`);

    let success = false;
    let attempts = 0;

    while (!success && attempts < 3) {
      attempts++;
      console.log(`[Batch] Attempt ${attempts} for Pose #${pose.id}...`);

      try {
        // Start fresh prompt or navigate to chatgpt.com
        const ready = await page.evaluate(() => {
          return !!document.querySelector("div[contenteditable=true], #prompt-textarea, textarea");
        });

        if (!ready) {
          console.log("[Batch] Navigating to https://chatgpt.com/...");
          await page.goto("https://chatgpt.com/");
          await new Promise(r => setTimeout(r, 4000));
        }

        // Attach references (DNA + Beauty + Old Pose)
        const refFiles = [MASTER_DNA, BEAUTY_REF, oldPoseFile];
        console.log(`[Batch] Attaching 3 files:`, refFiles.map(f => path.basename(f)));
        await page.setInputFiles("input[aria-label=\"Attach photos\"]", refFiles);

        console.log("[Batch] Waiting 5s for attachments to upload...");
        await new Promise(r => setTimeout(r, 5000));

        // Construct strict prompt
        const promptText = `STRICT MULTI-REFERENCE CONDITIONING:
1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical eyes, nose bridge, lips, hair color and cream silk outfit).
2. BODY POSE & CAMERA ANGLE: Match the exact body pose, camera angle, and posture shown in the attached pose reference image (Pose #${pose.id}: ${pose.title}). ${pose.prompt} Editorial studio lighting, sharp focus, 8k resolution.`;

        console.log("[Batch] Entering prompt...");
        await page.click("div[contenteditable=true], #prompt-textarea, textarea");
        await page.keyboard.paste({ text: promptText });
        await new Promise(r => setTimeout(r, 1200));

        console.log("[Batch] Submitting prompt with Enter...");
        await page.keyboard.press("Enter");

        // Monitor generation
        console.log("[Batch] Monitoring image generation...");
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

          if (!status.isGenerating && status.imgCount > 0 && poll > 3) {
            console.log(`[Batch] Generation completed at poll ${poll + 1}!`);
            done = true;
            break;
          }
        }

        if (done) {
          console.log("[Batch] Downloading generated image blob...");
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
            fs.writeFileSync(targetPath, Buffer.from(data, "base64"));
            const stats = fs.statSync(targetPath);
            console.log(`[Batch] SUCCESSFULLY SAVED: ${targetFilename} (${(stats.size / 1024 / 1024).toFixed(2)} MB)`);
            success = true;

            await page.screenshot({ path: path.join(SHOTS_DIR, `batch_pose_${padded}.png`) });
          } else {
            console.log(`[Batch] Could not extract base64 data.`);
          }
        } else {
          console.log(`[Batch] Generation timed out or did not finish.`);
          await page.screenshot({ path: path.join(SHOTS_DIR, `batch_pose_${padded}_timeout.png`) });
        }

      } catch (err) {
        console.error(`[Batch] Error processing Pose #${pose.id}:`, err.message);
        await new Promise(r => setTimeout(r, 4000));
      }
    }

    if (!success) {
      console.error(`[Batch] FAILED to generate Pose #${pose.id} after 3 attempts.`);
    }

    // Delay between generations
    console.log("[Batch] Cooling down 4s before next pose...");
    await new Promise(r => setTimeout(r, 4000));
  }

  console.log("\n===============================================================");
  console.log("=== ALL REMAINING POSES 22 TO 36 PROCESSED ===");
  console.log("===============================================================");
}

await runBatch();
