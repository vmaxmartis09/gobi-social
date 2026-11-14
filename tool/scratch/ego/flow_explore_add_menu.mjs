/**
 * Explore Add Menu and Character creation in Google Flow
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const projectUrl = "https://flow.google.com/project/b3c2d9f6-d452-40a2-96f6-c7c92fd7bf7a";
await page.goto(projectUrl, { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);

// Click ".add-menu-trigger" ("Thêm thành phần vào ô nhập câu lệnh")
console.log("[Ego] Clicking Add Menu Trigger...");
await page.evaluate(() => {
  const addMenu = document.querySelector(".add-menu-trigger");
  if (addMenu) addMenu.click();
});
await page.waitForTimeout(2000);

// Inspect the popup menu that opened
const popupMenu = await page.evaluate(() => {
  const menuItems = Array.from(document.querySelectorAll("[role='menuitem'], .mat-mdc-menu-item, [class*='menu-item'], [class*='dropdown']")).map(el => ({
    text: (el.innerText || '').trim(),
    role: el.getAttribute('role'),
    className: el.className
  })).filter(el => el.text);

  return menuItems;
});

console.log("[Ego] Popup Menu Items:", JSON.stringify(popupMenu, null, 2));

const shotAddMenu = "/Volumes/Data/gobi-social/shots/google_flow_add_menu.png";
await page.screenshot({ path: shotAddMenu });
console.log("[Ego] Add Menu screenshot saved to:", shotAddMenu);

await task.finish({ keep: [page.label] });
