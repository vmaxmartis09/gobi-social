// Script mở project trong space mới và kiểm tra ô nhập prompt
const task = await taskSpace("Flow Batch 2");
const page = task.page("p1");

console.log("[Ego] Dang mo project Gobi...");
await page.goto("https://flow.google.com/u/1/project/905a28b7-ceb4-4cf9-b92d-443050bd2d43");
await page.waitForLoadState();
await page.waitForTimeout(3000);

// Chup anh kiem tra
const shotPath = "shots/ego_flow_batch2_loaded.png";
await page.screenshot({ path: shotPath });
console.log("[Ego] Da chup anh:", shotPath);

// Tim the input nhap lieu
const editorInfo = await page.evaluate(() => {
  const all = Array.from(document.querySelectorAll('*'));
  const inputs = all.filter(el => {
    return el.tagName === 'TEXTAREA' || 
           el.getAttribute('contenteditable') === 'true' || 
           el.getAttribute('data-slate-editor') === 'true';
  }).map(el => ({
    tag: el.tagName,
    classes: el.className,
    contentEditable: el.getAttribute('contenteditable'),
    slate: el.getAttribute('data-slate-editor'),
    text: el.innerText
  }));
  return { inputs };
});

console.log("[Ego] Cac o nhap lieu tim thay:", JSON.stringify(editorInfo, null, 2));

// Giu tab cho nguoi dung
await task.finish({ keep: ["p1"] });
