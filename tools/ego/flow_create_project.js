// Script bấm "+ Dự án mới" và vào Studio trên Google Flow
const spaces = await listTaskSpaces();
console.log("[Ego] Spaces:", JSON.stringify(spaces));

let task;
if (spaces.length > 0) {
  task = await taskSpace(spaces[0].name || spaces[0].id);
} else {
  task = await taskSpace("Google Flow Production");
}
const page = task.page("p1");

console.log("[Ego] URL hien tai:", await page.url());

// Click vao nut "Dự án mới"
console.log("[Ego] Dang tim va click nut 'Dự án mới'...");
const clicked = await page.evaluate(() => {
  const all = Array.from(document.querySelectorAll('button, div, a'));
  const target = all.find(el => {
    const txt = el.innerText || el.textContent || '';
    return txt.includes('Dự án mới') || txt.includes('New project');
  });
  if (target) {
    target.click();
    return true;
  }
  return false;
});

console.log("[Ego] Ket qua click nut Du an moi:", clicked);

// Cho giao dien studio load
await page.waitForTimeout(4000);
const studioUrl = await page.url();
console.log("[Ego] URL sau khi vao studio:", studioUrl);

// Chup anh man hinh studio
const shotPath = "C:/Users/HAI/OneDrive/Tài liệu/vmax/shots/ego_flow_studio_ready.png";
await page.screenshot({ path: shotPath });
console.log("[Ego] Da chup anh studio:", shotPath);

// Kiem tra cac selector quan trong trong Studio
const studioInspect = await page.evaluate(() => {
  const slate = !!document.querySelector("[data-slate-editor='true'], [contenteditable='true']");
  const buttons = Array.from(document.querySelectorAll('button')).map(b => (b.innerText || '').trim()).filter(Boolean);
  return { slate, buttonsCount: buttons.length, sampleButtons: buttons.slice(0, 10) };
});
console.log("[Ego] Thong tin Studio:", JSON.stringify(studioInspect, null, 2));

// Giu nguyen trang
await task.finish({ keep: ["p1"] });
