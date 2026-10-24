/**
 * Click specifically on the "Nhân vật" nav list item
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const projectUrl = "https://flow.google.com/project/b3c2d9f6-d452-40a2-96f6-c7c92fd7bf7a";
await page.goto(projectUrl, { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);

const clickedChar = await page.evaluate(() => {
  const listItems = Array.from(document.querySelectorAll("mat-list-item, .mat-mdc-list-item"));
  const charItem = listItems.find(el => el.innerText.includes("Nhân vật"));
  if (charItem) {
    charItem.click();
    return { success: true, text: charItem.innerText.trim() };
  }
  return { success: false };
});

console.log("[Ego] Clicked Character List Item:", JSON.stringify(clickedChar));
await page.waitForTimeout(3000);

const mainViewContent = await page.evaluate(() => {
  const main = document.querySelector("main") || document.querySelector(".main-content") || document.body;
  const buttons = Array.from(main.querySelectorAll("button, [role='button']")).map(b => (b.innerText || b.getAttribute('aria-label') || '').trim()).filter(Boolean);
  const headings = Array.from(main.querySelectorAll("h1, h2, h3, h4, [class*='title'], [class*='empty']")).map(h => (h.innerText || '').trim()).filter(Boolean);
  return { headings, buttons };
});

console.log("[Ego] Main View:", JSON.stringify(mainViewContent, null, 2));

const shotCharView = "/Volumes/Data/gobi-social/shots/google_flow_character_main_view.png";
await page.screenshot({ path: shotCharView });
console.log("[Ego] Main view screenshot saved to:", shotCharView);

await task.finish({ keep: [page.label] });
