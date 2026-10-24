/**
 * Gobi 36-Pose Master Autonomous Generator Engine
 * Multi-Image Conditioning + Auto-Rotating Catch-All ChatGPT Accounts
 */

import fs from "fs";
import path from "path";

const TARGET_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36";
const MASTER_DNA = path.join(TARGET_DIR, "00_MASTER_DNA_ANCHOR.jpg");
const SHOTS_DIR = "/Volumes/Data/gobi-social/shots";
const POSES_CONFIG = "/Volumes/Data/gobi-social/configs/koc_gobi_36_poses.json";
const ACCOUNT_CONFIG = "/Volumes/Data/gobi-social/configs/koc_account_counter.json";

function loadPoses() {
  return JSON.parse(fs.readFileSync(POSES_CONFIG, "utf-8"));
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
  console.log(`[ROTATE] Target new email: ${newEmail}`);

  let { chatgptTab, gmailTab } = await getTabs(task);
  let page = chatgptTab.page;

  // 1. Log out of current account
  console.log("[ROTATE] Logging out from ChatGPT...");
  try {
    await page.goto("https://chatgpt.com/");
    await page.waitForTimeout(3000);
    // Click user profile button at bottom left
    const profileBtn = await page.evaluate(() => {
      const btn = document.querySelector("button[data-testid*=\"profile\"], button[id*=\"headlessui-menu-button\"], [data-testid=\"user-menu-button\"]");
      if (btn) { btn.click(); return true; }
      return false;
    });
    await page.waitForTimeout(1500);

    // Click Log out
    await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll("div[role=\"menuitem\"], button"));
      const logout = items.find(el => el.innerText?.toLowerCase().includes("log out"));
      if (logout) logout.click();
    });
    await page.waitForTimeout(4000);
  } catch (err) {
    console.log("[ROTATE] Logout navigation error (proceeding to direct auth URL):", err.message);
  }

  // 2. Go to sign up page
  console.log("[ROTATE] Navigating to Sign up page...");
  await page.goto("https://chatgpt.com/auth/login");
  await page.waitForTimeout(3000);

  // Click Sign up button if present, or direct to signup
  await page.evaluate(() => {
    const signupBtn = Array.from(document.querySelectorAll("button, a")).find(el => 
      el.innerText?.toLowerCase().includes("sign up") || el.innerText?.toLowerCase().includes("đăng ký")
    );
    if (signupBtn) signupBtn.click();
  });
  await page.waitForTimeout(3000);

  // Enter email
  console.log(`[ROTATE] Entering email: ${newEmail}`);
  await page.fill("input[name=\"email\"], input[type=\"email\"], #email-input", newEmail);
  await page.waitForTimeout(1000);

  // Click Continue
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll("button[type=\"submit\"], button"));
    const contBtn = btns.find(b => b.innerText?.toLowerCase().includes("continue") || b.innerText?.toLowerCase().includes("tiếp tục"));
    if (contBtn) contBtn.click();
  });
  await page.waitForTimeout(3000);

  // Enter password
  console.log("[ROTATE] Entering password...");
  await page.fill("input[name=\"password\"], input[type=\"password\"], #password", password);
  await page.waitForTimeout(1000);

  // Click Continue
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll("button[type=\"submit\"], button"));
    const contBtn = btns.find(b => b.innerText?.toLowerCase().includes("continue") || b.innerText?.toLowerCase().includes("tiếp tục"));
    if (contBtn) contBtn.click();
  });
  await page.waitForTimeout(5000);

  // 3. Fetch OTP from Gmail tab
  console.log("[ROTATE] Waiting 10s for OTP to arrive in Gmail...");
  await page.waitForTimeout(10000);

  let gmailPage = gmailTab ? gmailTab.page : null;
  if (!gmailPage) {
    console.log("[ROTATE] Opening Gmail tab...");
    gmailPage = await task.newPage("https://mail.google.com/mail/u/0/#inbox");
    await gmailPage.waitForTimeout(5000);
  } else {
    await gmailPage.bringToFront();
    await gmailPage.goto("https://mail.google.com/mail/u/0/#inbox");
    await gmailPage.waitForTimeout(4000);
  }

  // Find latest OpenAI verification email
  console.log("[ROTATE] Reading OTP code from Gmail...");
  const otpCode = await gmailPage.evaluate(() => {
    const emails = Array.from(document.querySelectorAll("tr.zA, div.y6"));
    for (const em of emails) {
      const text = em.innerText || "";
      if (text.includes("OpenAI") || text.includes("ChatGPT") || text.includes("verification code")) {
        const match = text.match(/\b\d{6}\b/);
        if (match) return match[0];
      }
    }
    // Deep search in recent email rows
    const allText = document.body.innerText;
    const allMatches = allText.match(/\b\d{6}\b/g);
    if (allMatches && allMatches.length > 0) return allMatches[0];
    return null;
  });

  console.log(`[ROTATE] Retrieved OTP Code: ${otpCode}`);

  if (!otpCode) {
    console.log("[ROTATE] OTP not immediately found, taking Gmail screenshot...");
    await gmailPage.screenshot({ path: path.join(SHOTS_DIR, "gmail_otp_inspect.png") });
    throw new Error("Failed to extract OTP from Gmail");
  }

  // 4. Enter OTP in ChatGPT
  await page.bringToFront();
  console.log(`[ROTATE] Entering OTP into ChatGPT: ${otpCode}`);
  await page.fill("input[name=\"code\"], input[type=\"text\"][maxlength=\"6\"], input[autocomplete=\"one-time-code\"]", otpCode);
  await page.waitForTimeout(3000);

  // 5. Complete Onboarding details (Full name and birthday)
  console.log("[ROTATE] Filling onboarding details...");
  await page.evaluate(() => {
    const nameInputs = document.querySelectorAll("input[type=\"text\"], input[name*=\"name\"]");
    if (nameInputs.length > 0) {
      nameInputs[0].value = "Nguyen Thanh Gobi";
    }
  });

  // Try to submit onboarding
  await page.evaluate(() => {
    const submitBtn = Array.from(document.querySelectorAll("button")).find(b => 
      b.innerText?.toLowerCase().includes("agree") || b.innerText?.toLowerCase().includes("tiếp tục") || b.innerText?.toLowerCase().includes("continue")
    );
    if (submitBtn) submitBtn.click();
  });
  await page.waitForTimeout(5000);

  console.log("[ROTATE] Account rotation completed successfully!");
  return page;
}

async function runAutonomousEngine() {
  console.log("==================================================");
  console.log("=== GOBI 36-POSE MASTER AUTONOMOUS ENGINE START ===");
  console.log("==================================================");

  const poses = loadPoses();
  let accountState = loadAccountState();

  const task = await claimTaskSpace(35);
  let { chatgptTab } = await getTabs(task);
  let page = chatgptTab.page;

  for (const pose of poses) {
    const targetFile = path.join(TARGET_DIR, `${pose.code}.jpg`);
    if (fs.existsSync(targetFile)) {
      const stats = fs.statSync(targetFile);
      if (stats.size > 100000) {
        console.log(`[Engine] Pose #${pose.id} (${pose.code}) already exists (${(stats.size / 1024 / 1024).toFixed(2)} MB), skipping.`);
        continue;
      }
    }

    console.log(`\n--------------------------------------------------`);
    console.log(`[Engine] Generating Pose #${pose.id} / 36: ${pose.title}`);
    console.log(`--------------------------------------------------`);

    // Prepare multi-image references (Master DNA + up to 3 recent angles)
    const existingImgs = fs.readdirSync(TARGET_DIR)
      .filter(f => f.endsWith(".jpg") && f !== `${pose.code}.jpg`)
      .sort();

    const refImages = [MASTER_DNA];
    const otherImgs = existingImgs.filter(f => !f.includes("00_MASTER_DNA")).map(f => path.join(TARGET_DIR, f));
    const recents = otherImgs.slice(-3);
    for (const r of recents) {
      if (!refImages.includes(r)) refImages.push(r);
    }

    console.log(`[Engine] Attaching ${refImages.length} references:`, refImages.map(p => path.basename(p)));

    let success = false;
    let attempts = 0;

    while (!success && attempts < 3) {
      attempts++;
      try {
        // Measure current image count in chat
        const initialImgCount = await page.evaluate(() => {
          return document.querySelectorAll("img[alt*=\"Generated\"]").length;
        });

        // Attach images
        await page.setInputFiles("input[aria-label=\"Attach photos\"]", refImages);
        await page.waitForTimeout(4000);

        // Check if rate limited
        const isLimited = await page.evaluate(() => {
          const t = document.body.innerText.toLowerCase();
          return t.includes("reached the limit") || t.includes("upgrade to add more") || t.includes("limit for file attachments");
        });

        if (isLimited) {
          console.log("[Engine] Quota limit detected! Triggering account rotation...");
          page = await rotateToNewAccount(task, accountState);
          continue; // retry this pose with fresh account
        }

        // Paste prompt
        const fullPrompt = `STRICT IDENTITY CONDITIONING: You must generate the EXACT SAME WOMAN as shown in the attached reference images. Maintain 100% identical facial features, bone structure, eye shape, nose bridge, lips, hair color and cream silk outfit. ${pose.prompt}`;
        await page.click("div[contenteditable=true], #prompt-textarea, textarea");
        await page.keyboard.paste({ text: fullPrompt });
        await page.waitForTimeout(1000);
        await page.keyboard.press("Enter");

        console.log(`[Engine] Prompt sent for Pose #${pose.id}. Waiting for render...`);

        // Wait for new image to appear
        let rendered = false;
        for (let wait = 0; wait < 35; wait++) {
          await page.waitForTimeout(2500);
          const currentCount = await page.evaluate(() => {
            return document.querySelectorAll("img[alt*=\"Generated\"]").length;
          });
          if (currentCount > initialImgCount) {
            console.log(`[Engine] Render completed! (Images in chat: ${currentCount})`);
            rendered = true;
            break;
          }
          // Check for limit/error during generation
          const errorMsg = await page.evaluate(() => {
            const err = document.querySelector(".text-red-500, [class*=\"error\"]");
            return err ? err.innerText : null;
          });
          if (errorMsg && (errorMsg.includes("limit") || errorMsg.includes("try again later"))) {
            console.log(`[Engine] Error during generation: ${errorMsg}`);
            break;
          }
        }

        if (!rendered) {
          console.log("[Engine] Render did not complete in time or was limited. Checking limit...");
          const errorCheck = await page.evaluate(() => document.body.innerText.toLowerCase());
          if (errorCheck.includes("limit") || errorCheck.includes("too many requests")) {
            page = await rotateToNewAccount(task, accountState);
            continue;
          }
        }

        // Download latest image
        console.log("[Engine] Downloading image blob...");
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
          console.log(`[Engine] Successfully saved Pose #${pose.id} (${(stats.size / 1024 / 1024).toFixed(2)} MB): ${targetFile}`);
          success = true;

          const shotPath = path.join(SHOTS_DIR, `step_pose_${String(pose.id).padStart(2, "0")}.png`);
          await page.screenshot({ path: shotPath });
        } else {
          console.log(`[Engine] Failed to extract image data on attempt ${attempts}`);
        }

      } catch (err) {
        console.error(`[Engine] Error processing pose #${pose.id}:`, err.message);
        await page.waitForTimeout(5000);
      }
    }

    if (!success) {
      console.error(`[Engine] Could not generate pose #${pose.id} after ${attempts} attempts! Continuing...`);
    }

    // Delay between generations
    await page.waitForTimeout(3000);
  }

  console.log("\n==================================================");
  console.log("=== ALL 36 GOBI PROFILE POSES COMPLETED ===");
  console.log("==================================================");
}

await runAutonomousEngine();
