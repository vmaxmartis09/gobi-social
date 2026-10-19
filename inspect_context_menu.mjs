const task = await taskSpace("AI Flow Video Production");
const page = task.page("p2");

// Right click on the old Gobi card to see menu
await page.evaluate(() => {
  const cards = Array.from(document.querySelectorAll('.character-tile-name'));
  const oldGobi = cards.find(c => c.textContent.trim() === "Gobi");
  if (oldGobi) {
    const tile = oldGobi.closest('flow-grid-tile-container') || oldGobi;
    tile.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: 750, clientY: 550 }));
  }
});

await page.waitForTimeout(1000);
await page.screenshot({ path: "C:/Users/HAI/OneDrive/Tài liệu/vmax/shots/ego_gobi_context_menu.png" });

const menuItems = await page.evaluate(() => {
  const menus = Array.from(document.querySelectorAll('.mat-menu-content, .mat-mdc-menu-content, [role="menu"], [role="menuitem"]')).map(m => m.textContent.trim());
  return menus;
});
console.log("Context menu items:", menuItems);
