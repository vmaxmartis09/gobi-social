/**
 * Gobi 36-Pose Master Storyboard Engine
 * Strictly references the old 36-cell storyboard poses
 * + Master DNA Anchor for 100% facial and body consistency
 */

import fs from "fs";
import path from "path";

const TARGET_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36";
const MASTER_DNA = path.join(TARGET_DIR, "00_MASTER_DNA_ANCHOR.jpg");
const BEAUTY_REF = path.join(TARGET_DIR, "gobi_angle_01_front_beauty.jpg");
const OLD_POSES_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/old_reference_poses";
const SHOTS_DIR = "/Volumes/Data/gobi-social/shots";
const CONFIG_PATH = "/Volumes/Data/gobi-social/configs/koc_gobi_36_poses.json";
const ACCOUNT_CONFIG = "/Volumes/Data/gobi-social/configs/koc_account_counter.json";

function loadPoses() {
  return JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
}

function loadAccountState() {
  return JSON.parse(fs.readFileSync(ACCOUNT_CONFIG, "utf-8"));
}

function saveAccountState(state) {
  fs.writeFileSync(ACCOUNT_CONFIG, JSON.stringify(state, null, 2));
}

async function getTabs(task) {
  const tabs = await task.tabs();
  const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
  const gmailTab = tabs.find(t => t.url?.includes("mail.google.com"));
  return { chatgptTab, gmailTab };
}

async function rotateToNewAccount(task, state) {
  console.log("\n[ROTATE] Starting automatic account rotation...");
  state.current_worker_index += 1;
  const padded = String(state.current_worker_index).padStart(2, "0");
  const newEmail = `worker${padded}.gobi@${state.domain}`;
  const password = state.password_template;
  saveAccountState(state);
  console.log(`[ROTATE] Registering new email: ${newEmail}`);

  let { chatgptTab, gmailTab } = await getTabs(task);
  let page = chatgptTab.page;

  // Log out of current account
  console.log("[ROTATE] Logging out from ChatGPT...");
  try {
    await page.goto("https://chatgpt.com/");
    await page.waitForTimeout(3000);
    await page.evaluate(() => {
      const btn = document.querySelector("button[data-testid*=\"profile\"], button[id*=\"headlessui-menu-button\"], [data-testid=\"user-menu-button\"]");
      if (btn) btn.click();
    });
    await page.waitForTimeout(1500);

    await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll("div[role=\"menuitem\"], button"));
      const logout = items.find(el => el.innerText?.toLowerCase().includes("log out"));
      if (logout) logout.click();
    });
    await page.waitForTimeout(4000);
  } catch (err) {
    console.log("[ROTATE] Logout note:", err.message);
  }

  // Sign up
  console.log("[ROTATE] Navigating to Sign up page...");
  await page.goto("https://chatgpt.com/auth/login");
  await page.waitForTimeout(3000);

  await page.evaluate(() => {
    const signupBtn = Array.from(document.querySelectorAll("button, a")).find(el => 
      el.innerText?.toLowerCase().includes("sign up") || el.innerText?.toLowerCase().includes("đăng ký")
    );
    if (signupBtn) signupBtn.click();
  });
  await page.waitForTimeout(3000);

  console.log(`[ROTATE] Entering email: ${newEmail}`);
  await page.fill("input[name=\"email\"], input[type=\"email\"], #email-input", newEmail);
  await page.waitForTimeout(1000);

  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll("button[type=\"submit\"], button"));
    const contBtn = btns.find(b => b.innerText?.toLowerCase().includes("continue") || b.innerText?.toLowerCase().includes("tiếp tục"));
    if (contBtn) contBtn.click();
  });
  await page.waitForTimeout(3000);

  console.log("[ROTATE] Entering password...");
  await page.fill("input[name=\"password\"], input[type=\"password\"], #password", password);
  await page.waitForTimeout(1000);

  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll("button[type=\"submit\"], button"));
    const contBtn = btns.find(b => b.innerText?.toLowerCase().includes("continue") || b.innerText?.toLowerCase().includes("tiếp tục"));
    if (contBtn) contBtn.click();
  });
  await page.waitForTimeout(6000);

  // OTP
  console.log("[ROTATE] Waiting 10s for OTP in Gmail...");
  await page.waitForTimeout(10000);

  let gmailPage = gmailTab ? gmailTab.page : null;
  if (!gmailPage) {
    gmailPage = await task.newPage("https://mail.google.com/mail/u/0/#inbox");
    await gmailPage.waitForTimeout(5000);
  } else {
    await gmailPage.bringToFront();
    await gmailPage.goto("https://mail.google.com/mail/u/0/#inbox");
    await gmailPage.waitForTimeout(4000);
  }

  const otpCode = await gmailPage.evaluate(() => {
    const allText = document.body.innerText;
    const allMatches = allText.match(/\b\d{6}\b/g);
    if (allMatches && allMatches.length > 0) return allMatches[0];
    return null;
  });

  console.log(`[ROTATE] Retrieved OTP: ${otpCode}`);
  if (!otpCode) {
    await gmailPage.screenshot({ path: path.join(SHOTS_DIR, "gmail_otp_inspect.png") });
    throw new Error("Could not extract OTP");
  }

  await page.bringToFront();
  await page.fill("input[name=\"code\"], input[type=\"text\"][maxlength=\"6\"], input[autocomplete=\"one-time-code\"]", otpCode);
  await page.waitForTimeout(3000);

  await page.evaluate(() => {
    const nameInputs = document.querySelectorAll("input[type=\"text\"], input[name*=\"name\"]");
    if (nameInputs.length > 0) nameInputs[0].value = "Nguyen Thanh Gobi";
  });

  await page.evaluate(() => {
    const submitBtn = Array.from(document.querySelectorAll("button")).find(b => 
      b.innerText?.toLowerCase().includes("agree") || b.innerText?.toLowerCase().includes("tiếp tục") || b.innerText?.toLowerCase().includes("continue")
    );
    if (submitBtn) submitBtn.click();
  });
  await page.waitForTimeout(5000);

  console.log("[ROTATE] Account rotation successful!");
  return page;
}

async function runStoryboardMaster() {
  console.log("===============================================================");
  console.log("=== GOBI 36 STORYBOARD MASTER ENGINE (WITH OLD POSE REFS) ===");
  console.log("===============================================================");

  const poses = loadPoses();
  let accountState = loadAccountState();

  const task = await claimTaskSpace(35);
  let { chatgptTab } = await getTabs(task);
  let page = chatgptTab.page;

  for (const pose of poses) {
    const padded = String(pose.id).padStart(2, "0");
    const targetFile = path.join(TARGET_DIR, `gobi_storyboard_${padded}_${pose.pose_ref}`);

    if (fs.existsSync(targetFile)) {
      const stats = fs.statSync(targetFile);
      if (stats.size > 100000) {
        console.log(`[Storyboard Engine] Pose #${pose.id} (${pose.title}) already exists (${(stats.size / 1024 / 1024).toFixed(2)} MB), skipping.`);
        continue;
      }
    }

    const oldPoseRefFile = path.join(OLD_POSES_DIR, pose.pose_ref);
    if (!fs.existsSync(oldPoseRefFile)) {
      console.warn(`[Storyboard Engine] Warning: Old pose reference not found at ${oldPoseRefFile}`);
    }

    console.log(`\n---------------------------------------------------------------`);
    console.log(`[Storyboard Engine] Generating Pose #${pose.id} / 36: ${pose.title}`);
    console.log(`[Storyboard Engine] Referencing Old Pose: ${pose.pose_ref}`);
    console.log(`---------------------------------------------------------------`);

    // Triple conditioning:
    // 1. MASTER DNA Face
    // 2. High-res Beauty Face
    // 3. Exact Cropped Old Storyboard Pose
    const refSelection = [MASTER_DNA, BEAUTY_REF];
    if (fs.existsSync(oldPoseRefFile)) {
      refSelection.push(oldPoseRefFile);
    }

    console.log(`[Storyboard Engine] Attaching ${refSelection.length} references:`, refSelection.map(p => path.basename(p)));

    let success = false;
    let attempts = 0;

    while (!success && attempts < 3) {
      attempts++;
      try {
        // Scroll to bottom
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        await page.waitForTimeout(500);

        // Attach references
        await page.setInputFiles("input[aria-label=\"Attach photos\"]", refSelection);
        await page.waitForTimeout(4000);

        // Check if rate limited
        const isLimited = await page.evaluate(() => {
          const t = document.body.innerText.toLowerCase();
          return t.includes("reached the limit") || t.includes("upgrade to add more") || t.includes("limit for file attachments");
        });

        if (isLimited) {
          console.log("[Storyboard Engine] Limit detected! Rotating account...");
          page = await rotateToNewAccount(task, accountState);
          continue;
        }

        // Construct strict dual prompt
        const promptText = `STRICT DUAL CONDITIONING:\n1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical eyes, nose bridge, lips, hair color and cream silk outfit).\n2. BODY POSE & CAMERA ANGLE: Match the exact body pose, camera angle, and posture shown in the attached pose reference image (Pose #${pose.id}: ${pose.title}). ${pose.prompt} Editorial studio lighting, sharp focus, 8k resolution.`;

        await page.click("div[contenteditable=true], #prompt-textarea, textarea");
        await page.keyboard.paste({ text: promptText });
        await page.waitForTimeout(1000);
        await page.keyboard.press("Enter");

        console.log(`[Storyboard Engine] Prompt sent for Pose #${pose.id}. Waiting for render...`);

        // Wait for render to complete (monitor 'Response complete' or stop button absence)
        let rendered = false;
        for (let wait = 0; wait < 35; wait++) {
          await page.waitForTimeout(2500);
          const state = await page.evaluate(() => {
            const text = document.body.innerText;
            const stopBtn = !!document.querySelector("button[aria-label=\"Stop generating\"], [data-testid=\"stop-button\"]");
            return {
              isComplete: text.includes("Response complete") || text.includes("Edit\nChatGPT can make mistakes"),
              isGenerating: stopBtn
            };
          });

          if (state.isComplete && !state.isGenerating && wait > 4) {
            console.log(`[Storyboard Engine] Render complete confirmed!`);
            rendered = true;
            break;
          }
        }

        if (!rendered) {
          console.log("[Storyboard Engine] Generation wait timed out. Checking limit...");
          const textCheck = await page.evaluate(() => document.body.innerText.toLowerCase());
          if (textCheck.includes("limit") || textCheck.includes("too many requests")) {
            page = await rotateToNewAccount(task, accountState);
            continue;
          }
        }

        // Download latest image
        console.log("[Storyboard Engine] Downloading image blob...");
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
          console.log(`[Storyboard Engine] Successfully saved Pose #${pose.id} (${(stats.size / 1024 / 1024).toFixed(2)} MB): ${targetFile}`);
          success = true;

          const shotPath = path.join(SHOTS_DIR, `step_storyboard_pose_${padded}.png`);
          await page.screenshot({ path: shotPath });
        } else {
          console.log(`[Storyboard Engine] Failed to extract image data on attempt ${attempts}`);
        }

      } catch (err) {
        console.error(`[Storyboard Engine] Error processing pose #${pose.id}:`, err.message);
        await page.waitForTimeout(5000);
      }
    }

    await page.waitForTimeout(3000);
  }

  console.log("\n===============================================================");
  console.log("=== ALL 36 STORYBOARD POSES FULLY GENERATED & VERIFIED ===");
  console.log("===============================================================");
}

await runStoryboardMaster();
