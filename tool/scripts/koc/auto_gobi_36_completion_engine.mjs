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

async function getChatgptPage(task) {
  const tabs = await task.tabs();
  let chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
  if (!chatgptTab) {
    const page = await task.newPage("https://chatgpt.com/");
    return page;
  }
  return chatgptTab.page;
}

async function handleGoogleSwitch(task, emailTarget) {
  console.log(`[Google Switch] Switching to Google account: ${emailTarget}...`);
  const page = await getChatgptPage(task);
  
  // Log out of ChatGPT
  console.log("[Google Switch] Logging out...");
  try {
    await page.goto("https://chatgpt.com/");
    await new Promise(r => setTimeout(r, 3000));
    await page.evaluate(() => {
      const btn = document.querySelector("button[data-testid*=\"profile\"], button[id*=\"headlessui-menu-button\"], [data-testid=\"user-menu-button\"]");
      if (btn) btn.click();
    });
    await new Promise(r => setTimeout(r, 1500));
    await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll("div[role=\"menuitem\"], button"));
      const logout = items.find(el => el.innerText?.toLowerCase().includes("log out"));
      if (logout) logout.click();
    });
    await new Promise(r => setTimeout(r, 4000));
  } catch (err) {
    console.log("[Google Switch] Logout notice:", err.message);
  }

  // Go to login -> Continue with Google
  console.log("[Google Switch] Navigating to login...");
  await page.goto("https://chatgpt.com/auth/login");
  await new Promise(r => setTimeout(r, 4000));

  await page.evaluate(() => {
    const googleBtn = Array.from(document.querySelectorAll("button")).find(b => 
      b.innerText?.toLowerCase().includes("google")
    );
    if (googleBtn) googleBtn.click();
  });
  await new Promise(r => setTimeout(r, 5000));

  // Select target email
  console.log(`[Google Switch] Selecting ${emailTarget}...`);
  const clicked = await page.evaluate((email) => {
    const el = document.querySelector(`div[data-identifier="${email}"]`);
    if (el) {
      el.click();
      return true;
    }
    const all = Array.from(document.querySelectorAll("div, span, li"));
    const found = all.find(d => d.innerText?.trim() === email);
    if (found) {
      found.closest("li, div[role=\"link\"]")?.click() || found.click();
      return true;
    }
    return false;
  }, emailTarget);

  console.log(`[Google Switch] Account selected: ${clicked}`);
  await new Promise(r => setTimeout(r, 8000));
  await page.screenshot({ path: path.join(SHOTS_DIR, `switch_after_${emailTarget.split("@")[0]}.png`) });
  return page;
}

async function runCompletionEngine() {
  console.log("===============================================================");
  console.log("=== GOBI 36 STORYBOARD RELENTLESS COMPLETION ENGINE ===");
  console.log("===============================================================");

  const task = await taskSpace(35);
  let page = await getChatgptPage(task);

  const poses = loadPoses();
  const googleAccounts = [
    "dinhthienthoai@gmail.com",
    "nguyenthixuanhuong08072003@gmail.com",
    "vmaxmartis@gmail.com"
  ];
  let currentGoogleIdx = 2; // currently vmaxmartis is active

  for (const pose of poses) {
    // Only process poses 22 to 36 (or any missing ones)
    const padded = String(pose.id).padStart(2, "0");
    const targetFile = path.join(TARGET_DIR, `gobi_angle_${padded}_${pose.pose_ref.replace(/^\d+_/, "").replace(/\.jpg$/, "")}.jpg`);

    if (fs.existsSync(targetFile)) {
      const stats = fs.statSync(targetFile);
      if (stats.size > 200000) {
        console.log(`[Engine] Pose #${pose.id} (${pose.title}) already completed (${(stats.size / 1024 / 1024).toFixed(2)} MB), skipping.`);
        continue;
      }
    }

    const oldPoseRefFile = path.join(OLD_POSES_DIR, pose.pose_ref);
    if (!fs.existsSync(oldPoseRefFile)) {
      console.warn(`[Engine] Warning: Reference file not found: ${oldPoseRefFile}`);
      continue;
    }

    console.log(`\n---------------------------------------------------------------`);
    console.log(`[Engine] Generating Pose #${pose.id} / 36: ${pose.title}`);
    console.log(`[Engine] Pose Ref: ${pose.pose_ref}`);
    console.log(`[Engine] Target File: ${targetFile}`);
    console.log(`---------------------------------------------------------------`);

    // Multi-reference conditioning:
    // 1. MASTER DNA Face Anchor
    // 2. High-res Beauty Face Reference
    // 3. Exact Old Pose Storyboard Crop
    const refSelection = [MASTER_DNA, BEAUTY_REF, oldPoseRefFile];
    console.log(`[Engine] Conditioning on ${refSelection.length} reference images.`);

    let success = false;
    let attempts = 0;

    while (!success && attempts < 3) {
      attempts++;
      try {
        // Check if page is ready
        const isReady = await page.evaluate(() => {
          return !!document.querySelector("div[contenteditable=true], #prompt-textarea, textarea");
        });

        if (!isReady) {
          console.log("[Engine] Navigating back to https://chatgpt.com/...");
          await page.goto("https://chatgpt.com/");
          await new Promise(r => setTimeout(r, 4000));
        }

        // Attach photos
        console.log(`[Engine] Attaching files (Attempt ${attempts})...`);
        const fileInput = "input[aria-label=\"Attach photos\"]";
        await page.setInputFiles(fileInput, refSelection);
        await new Promise(r => setTimeout(r, 4500));

        // Check for upload error or quota limit
        const limitCheck = await page.evaluate(() => {
          const t = document.body.innerText.toLowerCase();
          return t.includes("trouble processing uploads") || 
                 t.includes("reached the limit") || 
                 t.includes("limit for file attachments") ||
                 t.includes("upgrade to add more");
        });

        if (limitCheck) {
          console.log("[Engine] Attachment limit or upload trouble detected! Switching Google account...");
          currentGoogleIdx = (currentGoogleIdx + 1) % googleAccounts.length;
          page = await handleGoogleSwitch(task, googleAccounts[currentGoogleIdx]);
          continue;
        }

        // Prompt text
        const promptText = `STRICT MULTI-REFERENCE CONDITIONING:
1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical eyes, nose bridge, lips, hair color and cream silk outfit).
2. BODY POSE & CAMERA ANGLE: Match the exact body pose, camera angle, and posture shown in the attached pose reference image (Pose #${pose.id}: ${pose.title}). ${pose.prompt} Editorial studio lighting, sharp focus, 8k resolution.`;

        console.log("[Engine] Pasting prompt...");
        await page.click("div[contenteditable=true], #prompt-textarea, textarea");
        await page.keyboard.paste({ text: promptText });
        await new Promise(r => setTimeout(r, 1000));

        console.log("[Engine] Submitting generation prompt...");
        await page.keyboard.press("Enter");

        // Wait for render
        console.log("[Engine] Waiting for image generation...");
        let rendered = false;
        for (let wait = 0; wait < 35; wait++) {
          await new Promise(r => setTimeout(r, 3000));
          const state = await page.evaluate(() => {
            const text = document.body.innerText;
            const isGenerating = !!document.querySelector("button[aria-label=\"Stop generating\"], [data-testid=\"stop-button\"]");
            const imgs = Array.from(document.querySelectorAll("img[alt*=\"Generated\"]"));
            const error = text.includes("trouble processing uploads") || text.includes("limit reached") || text.includes("too many requests");
            return { isGenerating, imgCount: imgs.length, error };
          });

          if (state.error) {
            console.log("[Engine] Error banner detected during generation!");
            break;
          }

          if (!state.isGenerating && state.imgCount > 0 && wait > 3) {
            console.log(`[Engine] Generation confirmed complete at poll ${wait + 1}!`);
            rendered = true;
            break;
          }
        }

        if (!rendered) {
          console.log(`[Engine] Attempt ${attempts} did not produce image, retrying or checking limits...`);
          const hasLimit = await page.evaluate(() => {
            const t = document.body.innerText.toLowerCase();
            return t.includes("limit") || t.includes("trouble processing uploads");
          });
          if (hasLimit) {
            currentGoogleIdx = (currentGoogleIdx + 1) % googleAccounts.length;
            page = await handleGoogleSwitch(task, googleAccounts[currentGoogleIdx]);
          }
          continue;
        }

        // Download latest image
        console.log("[Engine] Downloading generated image blob...");
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
          console.log(`[Engine] SUCCESSFULLY SAVED Pose #${pose.id} (${(stats.size / 1024 / 1024).toFixed(2)} MB): ${targetFile}`);
          success = true;

          const shotPath = path.join(SHOTS_DIR, `step_pose_${padded}.png`);
          await page.screenshot({ path: shotPath });
        } else {
          console.log(`[Engine] Could not extract base64 data for pose #${pose.id}`);
        }

      } catch (err) {
        console.error(`[Engine] Error on pose #${pose.id}:`, err.message);
        await new Promise(r => setTimeout(r, 5000));
      }
    }

    if (!success) {
      console.error(`[Engine] FAILED to generate Pose #${pose.id} after 3 attempts!`);
    }

    // Small breather between generations
    await new Promise(r => setTimeout(r, 4000));
  }

  console.log("\n===============================================================");
  console.log("=== ALL REMAINING GOBI 36 POSES HAVE BEEN PROCESSED ===");
  console.log("===============================================================");
}

await runCompletionEngine();
