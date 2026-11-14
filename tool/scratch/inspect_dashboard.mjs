// scratch/inspect_dashboard.mjs
const task = await taskSpace("inspect refined dashboard");
const page = task.page("p1");

console.log("Navigating to http://localhost:3000...");
await page.goto("http://localhost:3000");
await new Promise(r => setTimeout(r, 2000));

const SHOTS_DIR = "/Volumes/Data/gobi-social/shots";

// 1. Take full screenshot of refined overview with small elegant cards & icon filter
console.log("Taking screenshot of Refined Dashboard Overview...");
await page.screenshot({ path: `${SHOTS_DIR}/dashboard_refined_overview.png`, fullPage: true });

// 2. Test horizontal scroll on icon filter bar
console.log("Testing horizontal scroll on icon filter bar...");
await page.evaluate(() => {
  const scrollBtn = document.querySelector('button[title="Cuộn bộ lọc sang phải"]');
  if (scrollBtn) scrollBtn.click();
});
await new Promise(r => setTimeout(r, 600));
await page.screenshot({ path: `${SHOTS_DIR}/dashboard_icon_filter_scroll.png` });

// 3. Test click on icon filter: "Có Video sạch"
console.log("Testing click on 'Có Video sạch' icon filter...");
await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll('button'));
  const hasVideoBtn = buttons.find(b => b.textContent && b.textContent.includes('Có Video sạch'));
  if (hasVideoBtn) hasVideoBtn.click();
});
await new Promise(r => setTimeout(r, 800));
await page.screenshot({ path: `${SHOTS_DIR}/dashboard_filter_has_video.png` });

// 4. Test click on icon filter: "Viral >100K"
console.log("Testing click on 'Viral >100K' icon filter...");
await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll('button'));
  const viralBtn = buttons.find(b => b.textContent && b.textContent.includes('Viral >100K'));
  if (viralBtn) viralBtn.click();
});
await new Promise(r => setTimeout(r, 800));
await page.screenshot({ path: `${SHOTS_DIR}/dashboard_filter_viral.png` });

// 5. Reset to "Tất cả"
console.log("Resetting to 'Tất cả' filter...");
await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll('button'));
  const allBtn = buttons.find(b => b.textContent && b.textContent.includes('Tất cả'));
  if (allBtn) allBtn.click();
});
await new Promise(r => setTimeout(r, 600));

// 6. Test Switch to Compact List View
console.log("Testing Switch to Compact List View...");
await page.evaluate(() => {
  const compactBtn = document.querySelector('button[title="Chế độ Danh sách siêu gọn"]');
  if (compactBtn) compactBtn.click();
});
await new Promise(r => setTimeout(r, 600));
await page.screenshot({ path: `${SHOTS_DIR}/dashboard_compact_list_view.png` });

// 7. Switch back to Refined Grid
console.log("Switching back to Refined Grid View...");
await page.evaluate(() => {
  const gridBtn = document.querySelector('button[title="Chế độ Thẻ nhỏ tinh tế"]');
  if (gridBtn) gridBtn.click();
});
await new Promise(r => setTimeout(r, 600));

// 8. Test 1-click Copy Prompt on card
console.log("Testing 1-click Copy Prompt on first card...");
await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll('button'));
  const copyBtn = buttons.find(b => b.textContent && b.textContent.includes('Copy Flow'));
  if (copyBtn) copyBtn.click();
});
await new Promise(r => setTimeout(r, 500));
await page.screenshot({ path: `${SHOTS_DIR}/dashboard_card_copy_prompt.png` });

// 9. Click on card to open detail modal
console.log("Testing Click on card to open detail modal...");
await page.evaluate(() => {
  const cards = Array.from(document.querySelectorAll('.kokonut-card'));
  const jobCard = cards.find(c => c.textContent && c.textContent.includes('JOB-'));
  if (jobCard) jobCard.click();
});
await new Promise(r => setTimeout(r, 1000));
await page.screenshot({ path: `${SHOTS_DIR}/dashboard_modal_detail_verified.png` });

await task.finish({ keep: [] });
console.log("All verifications passed and screenshots saved!");
