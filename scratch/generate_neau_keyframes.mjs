import fs from "fs";
import path from "path";

const TARGET_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/campaign_neau";
const MASTER_DNA = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36/00_MASTER_DNA_ANCHOR.jpg";
const BEAUTY_REF = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36/gobi_angle_01_front_beauty.jpg";
const OUTFIT_REF = "/Volumes/Data/gobi-social/assets/datasets/koc/campaign_neau/ref_outfit_grey.jpg";
const SHOTS_DIR = "/Volumes/Data/gobi-social/shots/campaign_neau";

const SHOTS = [
  {
    id: 1,
    name: "shot_01_hook",
    title: "Gobi Cận Mặt Hook Mặc Áo Thun NEAU Bodyfit",
    prompt: "STRICT MULTI-REFERENCE CONDITIONING: 1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical eyes, nose bridge, lips, hair color and facial features of Gobi). 2. OUTFIT & STYLING: Dress her in the exact outfit shown in the outfit reference: a sleek, ultra-comfortable long-sleeve crewneck bodyfit athletic t-shirt in heather taupe/grey, tucked cleanly into light blue high-waisted wide-leg denim jeans. Elegant delicate gold pendant necklace, chic chain shoulder bag. Upper-body medium beauty portrait looking directly at camera with bright, engaging, confident creator smile. Modern bright sunlit studio loft interior, sharp focus, 8k resolution, vertical 9:16 aspect ratio."
  },
  {
    id: 2,
    name: "shot_02_walk",
    title: "Gobi Toàn Thân Bước Đi Lookbook Lên Dáng Áo & Quần Suông",
    prompt: "STRICT MULTI-REFERENCE CONDITIONING: 1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical eyes, nose bridge, lips, long dark hair of Gobi). 2. OUTFIT & FULL BODY POSE: Full body fashion walk shot of this exact woman walking forward mid-stride towards camera in a modern minimalist luxury apartment. Wearing the exact heather grey long-sleeve bodyfit crewneck top tucked cleanly into high-waisted light blue wide-leg denim jeans, showcasing a slim flattering waistline and elongated leg proportions. Black leather chain shoulder bag. Editorial lookbook lighting, photorealistic, 8k resolution, vertical 9:16 aspect ratio."
  },
  {
    id: 3,
    name: "shot_03_fabric",
    title: "Gobi Cận Cảnh Chất Vải Micro-Mesh Co Giãn",
    prompt: "STRICT MULTI-REFERENCE CONDITIONING: 1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical face and delicate features of Gobi). 2. MACRO DETAIL: Extreme close-up shot focusing on her hand delicately stretching the seamless micro-mesh fabric of the heather grey bodyfit long-sleeve shirt near her collarbone and shoulder. Emphasize the ultra-soft, smooth, breathable athletic fabric texture, flawless seamless collar, and smooth glowing collarbone. Soft warm natural light, pristine macro clarity, 8k resolution, vertical 9:16 aspect ratio."
  },
  {
    id: 4,
    name: "shot_04_blazer",
    title: "Gobi Phối Layering Áo Blazer Ngoài",
    prompt: "STRICT MULTI-REFERENCE CONDITIONING: 1. FACE & IDENTITY: You must generate the EXACT SAME WOMAN as shown in the Master DNA face reference images (identical face, eyes, lips, and hair of Gobi). 2. STYLING & POSE: Medium shot of this exact woman standing relaxed, wearing a stylish oversized beige/camel tailored blazer layered over the heather grey bodyfit crewneck t-shirt. Chic effortless autumn/winter fashion layering, confident charming smile, looking at camera. Modern architectural loft background, editorial lighting, 8k resolution, vertical 9:16 aspect ratio."
  }
];

async function runKeyframes() {
  console.log("===============================================================");
  console.log("=== GOBI CAMPAIGN NEAU: KEYFRAME GENERATION ENGINE ===");
  console.log("===============================================================");

  const task = await taskSpace("Gobi_Campaign_NEAU");
  const tabs = await task.tabs();
  let chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
  const page = chatgptTab ? chatgptTab.page : await task.newPage();

  for (const s of SHOTS) {
    const targetFile = path.join(TARGET_DIR, `${s.name}.jpg`);
    if (fs.existsSync(targetFile)) {
      const stats = fs.statSync(targetFile);
      if (stats.size > 500000) {
        console.log(`[Campaign] ${s.name} already exists (${(stats.size / 1024 / 1024).toFixed(2)} MB), skipping.`);
        continue;
      }
    }

    console.log(`\n===============================================================`);
    console.log(`[Campaign] STARTING SHOT #${s.id}: ${s.title}`);
    console.log(`===============================================================`);

    let success = false;
    let attempts = 0;

    while (!success && attempts < 3) {
      attempts++;
      console.log(`[Campaign] Attempt ${attempts} for Shot #${s.id}...`);

      try {
        console.log("[Campaign] Navigating to clean https://chatgpt.com/...");
        await page.goto("https://chatgpt.com/");
        await new Promise(r => setTimeout(r, 4500));

        // Attach 3 references: Master DNA, Beauty Ref, and Outfit Ref
        const refFiles = [MASTER_DNA, BEAUTY_REF, OUTFIT_REF];
        console.log(`[Campaign] Attaching 3 files:`, refFiles.map(f => path.basename(f)));
        await page.setInputFiles("input[aria-label=\"Attach photos\"]", refFiles);

        console.log("[Campaign] Waiting 6s for uploads to complete...");
        await new Promise(r => setTimeout(r, 6000));

        // Check upload status
        const uploadState = await page.evaluate(() => {
          const bodyText = document.body.innerText;
          const failed = bodyText.includes("Upload failed");
          const limit = bodyText.includes("limit for file attachments");
          return { failed, limit };
        });

        if (uploadState.failed || uploadState.limit) {
          console.warn("[Campaign] Upload error:", uploadState);
          await page.screenshot({ path: path.join(SHOTS_DIR, `shot_${s.id}_upload_err.png`) });
          break;
        }

        console.log("[Campaign] Entering prompt...");
        await page.click("div[contenteditable=true], #prompt-textarea, textarea");
        await page.keyboard.paste({ text: s.prompt });
        await new Promise(r => setTimeout(r, 1200));

        console.log("[Campaign] Submitting prompt...");
        await page.keyboard.press("Enter");

        // Poll for generation
        console.log("[Campaign] Polling for generation completion...");
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
            console.log(`[Campaign] Poll ${poll + 1}/45: generating=${status.isGenerating}, imgs=${status.imgCount}`);
          }

          if (!status.isGenerating && status.imgCount > 0 && poll > 4) {
            console.log(`[Campaign] Generation confirmed complete at poll ${poll + 1}!`);
            done = true;
            break;
          }
        }

        if (done) {
          console.log("[Campaign] Downloading generated image blob...");
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
            console.log(`[Campaign] SUCCESSFULLY SAVED: ${s.name}.jpg (${(stats.size / 1024 / 1024).toFixed(2)} MB)`);
            success = true;
            await page.screenshot({ path: path.join(SHOTS_DIR, `${s.name}_saved.png`) });
          } else {
            console.log("[Campaign] Could not extract base64 data.");
          }
        } else {
          console.log("[Campaign] Generation timed out.");
          await page.screenshot({ path: path.join(SHOTS_DIR, `${s.name}_timeout.png`) });
        }
      } catch (err) {
        console.error(`[Campaign] Error on Shot #${s.id}:`, err.message);
        await new Promise(r => setTimeout(r, 4000));
      }
    }

    if (!success) {
      console.error(`[Campaign] FAILED Shot #${s.id}`);
    }

    console.log("[Campaign] Resting 5s before next shot...");
    await new Promise(r => setTimeout(r, 5000));
  }

  console.log("\n===============================================================");
  console.log("=== KEYFRAME GENERATION COMPLETE ===");
  console.log("===============================================================");
}

await runKeyframes();
