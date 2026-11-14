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

async function runFinish() {
  console.log("===============================================================");
  console.log("=== GOBI 36: ROCK-SOLID RUNNER FOR POSES 23 TO 36 ===");
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
  const remaining = poses.filter(p => p.id >= 23 && p.id <= 36);

  for (const pose of remaining) {
    const padded = String(pose.id).padStart(2, "0");
    const existing = getExistingPoseFile(padded);
    if (existing) {
      const stats = fs.statSync(path.join(TARGET_DIR, existing));
      if (stats.size > 500000) {
        console.log(`[Runner] Pose #${pose.id} (${pose.title}) already exists (${(stats.size / 1024 / 1024).toFixed(2)} MB), skipping.`);
        continue;
      }
    }

    const oldPoseFile = path.join(OLD_POSES_DIR, pose.pose_ref);
    if (!fs.existsSync(oldPoseFile)) {
      console.warn(`[Runner] Reference pose file not found: ${oldPoseFile}`);
      continue;
    }

    const slug = pose.pose_ref.replace(/^\d+_/, "").replace(/\.jpg$/, "");
    const targetFilename = `gobi_angle_${padded}_${slug}.jpg`;
    const targetPath = path.join(TARGET_DIR, targetFilename);

    console.log(`\n===============================================================`);
    console.log(`[Runner] STARTING POSE #${pose.id} / 36: ${pose.title}`);
    console.log(`[Runner] Pose Ref: ${pose.pose_ref}`);
    console.log(`[Runner] Target: ${targetFilename}`);
    console.log(`===============================================================`);

    let success = false;
    let attempts = 0;

    while (!success && attempts < 3) {
      attempts++;
      console.log(`[Runner] Attempt ${attempts} for Pose #${pose.id}...`);

      try {
        // 1. Fresh page navigation to clear attachments & input state
        console.log("[Runner] Navigating to clean https://chatgpt.com/...");
        await page.goto("https://chatgpt.com/");
        await new Promise(r => setTimeout(r, 4500));

        // 2. Attach 3 references
        const refFiles = [MASTER_DNA, BEAUTY_REF, oldPoseFile];
        console.log(`[Runner] Attaching 3 files:`, refFiles.map(f => path.basename(f)));
        await page.setInputFiles("input[aria-label=\"Attach photos\"]", refFiles);

        console.log("[Runner] Waiting 6s for uploads to complete...");
        await new Promise(r => setTimeout(r, 6000));

        // 3. Verify upload didn't fail
        const uploadState = await page.evaluate(() => {
          const bodyText = document.body.innerText;
          const failed = bodyText.includes("Upload failed");
          const limit = bodyText.includes("limit for file attachments");
          return { failed, limit };
        });

        if (uploadState.failed || uploadState.limit) {
          console.warn("[Runner] Upload failed or limit hit:", uploadState);
          await page.screenshot({ path: path.join(SHOTS_DIR, `pose_${padded}_upload_err.png`) });
          break;
        }

        // 4. Prompt text
        const promptText = `STRICT MULTI-REFERENCE CONDITIONING:
1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical eyes, nose bridge, lips, hair color and cream silk outfit).
2. BODY POSE & CAMERA ANGLE: Match the exact body pose, camera angle, and posture shown in the attached pose reference image (Pose #${pose.id}: ${pose.title}). ${pose.prompt} Editorial studio lighting, sharp focus, 8k resolution.`;

        console.log("[Runner] Entering prompt...");
        await page.click("div[contenteditable=true], #prompt-textarea, textarea");
        await page.keyboard.paste({ text: promptText });
        await new Promise(r => setTimeout(r, 1200));

        console.log("[Runner] Submitting prompt...");
        await page.keyboard.press("Enter");

        // 5. Poll for generation completion
        console.log("[Runner] Polling for generation completion...");
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

          if (poll % 5 === 0) {
            console.log(`[Runner] Poll ${poll + 1}/45: generating=${status.isGenerating}, imgs=${status.imgCount}`);
          }

          if (!status.isGenerating && status.imgCount > 0 && poll > 4) {
            console.log(`[Runner] Generation confirmed complete at poll ${poll + 1}!`);
            done = true;
            break;
          }
        }

        if (done) {
          console.log("[Runner] Downloading generated image blob...");
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
            console.log(`[Runner] SUCCESSFULLY SAVED: ${targetFilename} (${(stats.size / 1024 / 1024).toFixed(2)} MB)`);
            success = true;

            await page.screenshot({ path: path.join(SHOTS_DIR, `runner_pose_${padded}_saved.png`) });
          } else {
            console.log(`[Runner] Could not extract base64 data.`);
          }
        } else {
          console.log(`[Runner] Generation timed out.`);
          await page.screenshot({ path: path.join(SHOTS_DIR, `runner_pose_${padded}_timeout.png`) });
        }

      } catch (err) {
        console.error(`[Runner] Error on Pose #${pose.id}:`, err.message);
        await new Promise(r => setTimeout(r, 4000));
      }
    }

    if (!success) {
      console.error(`[Runner] FAILED to generate Pose #${pose.id} after attempts.`);
    }

    // Delay between poses
    console.log("[Runner] Resting 5s before next pose...");
    await new Promise(r => setTimeout(r, 5000));
  }

  console.log("\n===============================================================");
  console.log("=== ALL REMAINING POSES 23 TO 36 PROCESSED ===");
  console.log("===============================================================");
}

await runFinish();
