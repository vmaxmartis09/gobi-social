// Script test nhap lieu vao ProseMirror tren Google Flow bang taskSpace moi
const task = await taskSpace("VMAX_Flow_Run");
const page = task.page("p1");

console.log("[Ego] Dang mo project Gobi...");
await page.goto("https://flow.google.com/u/1/project/905a28b7-ceb4-4cf9-b92d-443050bd2d43");
await page.waitForLoadState();
await page.waitForTimeout(3000);

console.log("[Ego] Dang click vao o nhap ProseMirror...");
await page.click("div.ProseMirror");
await page.waitForTimeout(500);

const testPrompt = "Test Gobi cinematic 9:16 scene";
console.log("[Ego] Dang nhap text qua keyboard.paste...");
await page.keyboard.paste({ text: testPrompt });
await page.waitForTimeout(1000);

// Chup anh kiem tra text da vao o chua
const shotPath = "C:/Users/HAI/OneDrive/Tài liệu/vmax/shots/ego_flow_input_typed.png";
await page.screenshot({ path: shotPath });
console.log("[Ego] Da chup anh xac nhan text da vao:", shotPath);

// Kiem tra trang thai sau khi nhap
const submitState = await page.evaluate(() => {
  const editor = document.querySelector("div.ProseMirror");
  return {
    editorText: editor ? editor.innerText : null
  };
});
console.log("[Ego] Text trong editor:", JSON.stringify(submitState));

// Xoa lai text de giu sach
await page.keyboard.press("ControlOrMeta+A");
await page.keyboard.press("Backspace");
await page.waitForTimeout(500);

// Dong task space gon gang
await task.finish({ keep: [] });
console.log("[Ego] Test hoan tat thanh cong my man!");
