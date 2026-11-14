/**
 * Test Multi-Image Reference Upload (2-5 images) on Kling AI via Ego Lite
 */

const task = await taskSpace("Kling_KOC_Production");
const page = task.page("p1");

console.log("[Ego] Navigating to Kling AI Creations...");
await page.goto("https://kling.ai/app/creations/grid", { waitUntil: "domcontentloaded", timeout: 45000 });
await page.waitForTimeout(3000);

// Dismiss popup if present
await page.evaluate(() => {
  const gotIt = Array.from(document.querySelectorAll("button")).find(b => b.innerText?.includes("Got It") || b.innerText?.includes("Accept"));
  if (gotIt) gotIt.click();
});
await page.waitForTimeout(1000);

// Switch to Image Generation if needed
await page.evaluate(() => {
  const trigger = document.querySelector(".designer-type-selector__trigger");
  if (trigger && !trigger.innerText?.includes("Image Generation")) {
    trigger.click();
  }
});
await page.waitForTimeout(800);
await page.evaluate(() => {
  const imgItem = Array.from(document.querySelectorAll("div, li, span")).find(el => el.innerText?.trim() === "Image Generation");
  if (imgItem) imgItem.click();
});
await page.waitForTimeout(1500);

// Prepare 3 reference images
const refImages = [
  "/Volumes/Data/gobi-social/assets/datasets/koc/MASTER_KOC_DNA.jpg",
  "/Volumes/Data/gobi-social/assets/samples/sample_video/koc_matrix_panels/panel_01_chinh_dien_toan_than.jpg",
  "/Volumes/Data/gobi-social/assets/samples/sample_video/koc_matrix_panels/panel_02_chinh_dien_trung_canh.jpg"
];

console.log("[Ego] Uploading 3 reference images...");
const fileInput = await page.waitForSelector("input[type='file'].el-upload__input", { timeout: 10000 });
if (fileInput) {
  await page.setInputFiles("input[type='file'].el-upload__input", refImages);
  console.log("[Ego] Successfully set 3 reference images!");
}

await page.waitForTimeout(3000);

// Screenshot to verify the 3 images are populated in the reference box
const shotPath = "/Volumes/Data/gobi-social/shots/kling_multi_reference_uploaded.png";
await page.screenshot({ path: shotPath });
console.log("[Ego] Screenshot saved to:", shotPath);

// Keep the page open for continued operation
await task.finish({ keep: ["p1"] });
