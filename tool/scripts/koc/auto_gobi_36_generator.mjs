/**
 * Gobi 36 Multi-Angle Dataset Autonomous Generator
 * Continuous Multi-Image Conditioning Loop via Ego Lite
 */

import fs from "fs";
import path from "path";

const TARGET_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36";
const MASTER_DNA = path.join(TARGET_DIR, "00_MASTER_DNA_ANCHOR.jpg");
const SHOTS_DIR = "/Volumes/Data/gobi-social/shots";

const ANGLES_PLAN = [
  {
    id: 3,
    code: "gobi_angle_03_profile_side",
    title: "Side Profile (90-degree lateral view)",
    prompt: "Generate Image #3: A side profile view (90-degree lateral shot) of this exact same woman. Showcase her delicate straight nasal bridge, natural jawline, earlobe, and smooth neck. Keep identical skin micro-pores, natural lips, dark hair, cream silk camisole. Editorial studio lighting, crisp focus, 8k resolution."
  },
  {
    id: 4,
    code: "gobi_angle_04_half_body_waist",
    title: "Upper Body / Waist-up shot",
    prompt: "Generate Image #4: A medium waist-up portrait of this exact same woman standing naturally in studio. Showing both shoulders, delicate collarbone, cream silk camisole and light beige ribbed knit cardigan draped softly over her shoulders. Friendly direct gaze at camera, subtle natural smile, 85mm portrait, 8k."
  },
  {
    id: 5,
    code: "gobi_angle_05_holding_product",
    title: "Product Review / Holding Pose",
    prompt: "Generate Image #5: Medium shot of this exact same woman holding a sleek minimalist cosmetic bottle near her chest, introducing it to the camera. Warm engaging creator smile, natural hand gesture, manicured clean nails, crisp focus on face and product, soft bokeh studio background, 8k."
  },
  {
    id: 6,
    code: "gobi_angle_06_three_quarter_left",
    title: "3/4 Angle Left with expressive glance",
    prompt: "Generate Image #6: 3/4 angle portrait turned 30 degrees to the left, head slightly tilted, thoughtful gentle expression, direct eye contact with camera. Identical facial symmetry, eye shape, nose bridge, delicate lips, cream silk camisole, 8k studio photography."
  },
  {
    id: 7,
    code: "gobi_angle_07_full_body_standing",
    title: "Full Body Standing Lookbook",
    prompt: "Generate Image #7: A full-length vertical lookbook shot of this exact same woman (1m62 slender proportional build). Wearing the cream silk camisole, beige fine-knit cardigan, and high-waisted tailored beige wide-leg trousers. Standing gracefully against a clean warm studio cyclorama, full body in sharp focus, 8k."
  },
  {
    id: 8,
    code: "gobi_angle_08_close_macro_eyes_lips",
    title: "Macro Extreme Close-Up Beauty",
    prompt: "Generate Image #8: An extreme macro beauty close-up focusing on her eyes, nose bridge, and lips. Showing authentic human skin texture, fine pores, natural double eyelids, amber-brown irises with catchlights, satin nude-pink lip sheen. 100mm macro lens, flawless realism, 8k."
  },
  {
    id: 9,
    code: "gobi_angle_09_seated_table",
    title: "Seated at Creator Desk / Review Table",
    prompt: "Generate Image #9: Medium shot of this exact same woman seated comfortably at a modern wooden studio desk, hands resting naturally on table, smiling warmly at camera as if recording a TikTok review video. Warm natural light, shallow depth of field, 8k."
  },
  {
    id: 10,
    code: "gobi_angle_10_low_angle_editorial",
    title: "Low Angle Confident Editorial",
    prompt: "Generate Image #10: A slightly low camera angle shot looking up at this exact same woman. Confident elegant poise, sharp clean jawline, long hair softly flowing, identical facial identity, cream silk outfit, high-fashion editorial lighting, 8k."
  },
  {
    id: 11,
    code: "gobi_angle_11_high_angle_soft",
    title: "High Angle Soft Casual Glance",
    prompt: "Generate Image #11: A gentle high camera angle looking slightly down at this exact same woman. Sweet expressive upward glance, natural soft eyelashes, radiant natural skin, relaxed shoulders, cream camisole, warm aesthetic, 8k."
  },
  {
    id: 12,
    code: "gobi_angle_12_talking_gesture",
    title: "Dynamic Speaking & Explaining Pose",
    prompt: "Generate Image #12: Authentic creator snapshot of this exact same woman in the middle of talking and explaining a concept, expressive open hand gesture, enthusiastic friendly smile, lively sparkling eyes, sharp focus, 8k."
  }
];

async function runBatch() {
  console.log("[Gobi Runner] Connecting to Ego Lite space 35...");
  const task = await claimTaskSpace(35);
  const tabs = await task.tabs();
  const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
  const page = chatgptTab.page;

  for (const item of ANGLES_PLAN) {
    const targetFile = path.join(TARGET_DIR, `${item.code}.jpg`);
    if (fs.existsSync(targetFile)) {
      console.log(`[Gobi Runner] Angle #${item.id} already exists, skipping.`);
      continue;
    }

    console.log(`\n==================================================`);
    console.log(`[Gobi Runner] Processing #${item.id}: ${item.title}`);
    console.log(`==================================================`);

    // Prepare multi-image references (2 to 4 recent existing images)
    const existingImgs = fs.readdirSync(TARGET_DIR)
      .filter(f => f.endsWith(".jpg"))
      .map(f => path.join(TARGET_DIR, f))
      .filter(f => f !== targetFile);

    // Pick Master DNA + up to 3 most recent angles
    const refSelection = [MASTER_DNA];
    for (let i = existingImgs.length - 1; i >= 0 && refSelection.length < 4; i--) {
      if (existingImgs[i] !== MASTER_DNA) {
        refSelection.push(existingImgs[i]);
      }
    }

    console.log(`[Gobi Runner] Attaching ${refSelection.length} reference images:`, refSelection.map(p => path.basename(p)));

    // Attach reference images
    await page.setInputFiles("input[aria-label=\"Attach photos\"]", refSelection);
    await page.waitForTimeout(4000);

    // Check if limit popup appeared
    const limitReached = await page.evaluate(() => {
      return document.body.innerText.includes("You've reached the limit for file attachments") ||
             document.body.innerText.includes("Upgrade to add more now");
    });

    if (limitReached) {
      console.log("[Gobi Runner] Quota limit reached on current account! Need rotation.");
      break;
    }

    // Type prompt
    const fullPrompt = `STRICT CONDITIONING: You must generate the EXACT SAME WOMAN as shown in the attached reference images. Maintain 100% identical facial features, eye shape, nose bridge, lips, hair, skin tone, and outfit. ${item.prompt}`;
    console.log(`[Gobi Runner] Typing prompt for #${item.id}...`);
    await page.click("div[contenteditable=true], #prompt-textarea, textarea");
    await page.keyboard.paste({ text: fullPrompt });
    await page.waitForTimeout(1000);

    // Send
    await page.keyboard.press("Enter");
    console.log(`[Gobi Runner] Sent! Waiting 25s for render...`);
    await page.waitForTimeout(25000);

    // Verify and download
    let saved = false;
    for (let retry = 0; retry < 3; retry++) {
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
        console.log(`[Gobi Runner] Successfully saved: ${targetFile}`);
        saved = true;
        break;
      } else {
        console.log(`[Gobi Runner] Still rendering, waiting 10s more (retry ${retry + 1}/3)...`);
        await page.waitForTimeout(10000);
      }
    }

    const shotPath = path.join(SHOTS_DIR, `gobi_step_${item.id}.png`);
    await page.screenshot({ path: shotPath });
    console.log(`[Gobi Runner] Progress screenshot saved to: ${shotPath}`);

    // Small delay between requests to avoid rate limits
    await page.waitForTimeout(3000);
  }

  console.log("[Gobi Runner] Batch step completed!");
}

await runBatch();
