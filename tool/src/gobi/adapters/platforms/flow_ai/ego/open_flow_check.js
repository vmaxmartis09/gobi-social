// Script mở và kiểm tra Google Flow trên Ego Lite
const task = await taskSpace("Google Flow Production");
const page = task.page("p1");

console.log("[Ego] Dang dieu huong den labs.google/flow...");
await page.goto("https://labs.google/flow");
await page.waitForLoadState();

const currentUrl = page.url();
const pageTitle = await page.title();
console.log("[Ego] URL hien tai:", currentUrl);
console.log("[Ego] Tieu de trang:", pageTitle);

const shotPath = "shots/ego_flow_live_check.png";
await page.screenshot({ path: shotPath });
console.log("[Ego] Da chup anh man hinh:", shotPath);

// Kiem tra cac phan tu chinh tren trang
const status = await page.evaluate(() => {
  const isSignIn = !!document.querySelector("a[href*='accounts.google.com'], button:has-text('Sign in')");
  const hasNewProject = !!document.querySelector("button:has-text('New project'), [aria-label*='New project']");
  const slateEditor = !!document.querySelector("[data-slate-editor='true'], [contenteditable='true']");
  return { isSignIn, hasNewProject, slateEditor, currentHref: window.location.href };
});
console.log("[Ego] Trang thai phan tu:", JSON.stringify(status, null, 2));

// Giu nguyen tab tren trinh duyet Ego Lite de nguoi dung theo doi
await task.finish({ keep: ["p1"] });
console.log("[Ego] Hoan tat khoi tao Google Flow tren Ego Lite!");
