import path from "path";
import fs from "fs";

const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

console.log("Navigating to https://chatgpt.com/ to clear stuck elements...");
await page.goto("https://chatgpt.com/");
await new Promise(r => setTimeout(r, 4000));

const TARGET_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36";
const MASTER_DNA = path.join(TARGET_DIR, "00_MASTER_DNA_ANCHOR.jpg");
const BEAUTY_REF = path.join(TARGET_DIR, "gobi_angle_01_front_beauty.jpg");
const OLD_POSES_DIR = "/Volumes/Data/gobi-social/assets/datasets/koc/old_reference_poses";
const testPose = path.join(OLD_POSES_DIR, "26_buoc_di_tu_nhien.jpg");

console.log("Uploading test file:", testPose);
await page.setInputFiles("input[aria-label=\"Attach photos\"]", [MASTER_DNA, BEAUTY_REF, testPose]);
await new Promise(r => setTimeout(r, 6000));

const status = await page.evaluate(() => {
  const text = document.body.innerText;
  return {
    failed: text.includes("Upload failed"),
    limit: text.includes("limit for file attachments") || text.includes("You've reached our limit")
  };
});

console.log("Upload test result:", status);
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/test_upload_result.png" });
