/**
 * Inspect Kling AI video creation UI
 */
const task = await claimTaskSpace(2);
const pages = task.pages();
console.log("[Ego] Managed pages count:", pages.length);

// Find the page that is Kling
let klingPage = null;
for (const p of pages) {
  const url = await p.evaluate(() => window.location.href);
  if (url.includes("kling")) {
    klingPage = p;
    break;
  }
}

if (!klingPage) {
  console.log("[!] Kling page not found, creating new one...");
  klingPage = await task.newPage();
  await klingPage.goto("https://kling.ai/app/creations/grid", { waitUntil: "domcontentloaded" });
  await klingPage.waitForTimeout(3000);
}

// Inspect Kling UI buttons and inputs
const info = await klingPage.evaluate(() => {
  const tabs = Array.from(document.querySelectorAll("button, div[role='tab'], li")).map(el => ({
    text: (el.innerText || '').trim(),
    className: el.className,
    role: el.getAttribute('role')
  })).filter(el => el.text && el.text.length < 25);

  const fileInputs = Array.from(document.querySelectorAll("input[type='file']")).map(inp => ({
    className: inp.className,
    accept: inp.getAttribute('accept')
  }));

  const textareas = Array.from(document.querySelectorAll("textarea, [contenteditable='true']")).map(t => ({
    placeholder: t.getAttribute('placeholder') || t.getAttribute('data-placeholder'),
    className: t.className
  }));

  return { tabs: tabs.slice(0, 30), fileInputs, textareas };
});

console.log("[Ego] Kling File Inputs:", JSON.stringify(info.fileInputs, null, 2));
console.log("[Ego] Kling Textareas:", JSON.stringify(info.textareas, null, 2));
console.log("[Ego] Sample Tabs/Buttons:", JSON.stringify(info.tabs.slice(0, 15), null, 2));

const shot = "/Volumes/Data/gobi-social/shots/kling_creation_detail.png";
await klingPage.screenshot({ path: shot });
console.log("[Ego] Detail screenshot saved to:", shot);

await task.finish({ keep: pages.map(p => p.label) });
