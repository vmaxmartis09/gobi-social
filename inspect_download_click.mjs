const task = await claimTaskSpace(4);
const page = task.page("p2");

// Inspect what clicking download or play does
const res = await page.evaluate(async () => {
  const downloadBtn = document.querySelector('button[aria-label="Tải nội dung nghe nhìn xuống"]');
  if (downloadBtn) {
    downloadBtn.click();
  }
  return { clicked: !!downloadBtn };
});

await page.waitForTimeout(1000);
await page.screenshot({ path: "C:/Users/HAI/OneDrive/Tài liệu/vmax/shots/ego_download_clicked.png" });

const menuOrDialog = await page.evaluate(() => {
  const menus = Array.from(document.querySelectorAll('.mat-mdc-menu-content, mat-menu-panel, [role="menu"], [role="dialog"], [role="menuitem"]')).map(el => el.textContent.trim());
  return menus;
});
console.log("After download click:", res, "Menus:", menuOrDialog);
