/**
 * Inspect Google Flow to create a new Project
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

console.log("[Ego] Connecting to Google Flow home...");
await page.goto("https://flow.google.com/", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

// Find project creation elements
const creationButtons = await page.evaluate(() => {
  const elements = Array.from(document.querySelectorAll("button, a, div[role='button']")).map(el => ({
    text: (el.innerText || '').trim(),
    ariaLabel: el.getAttribute('aria-label'),
    href: el.getAttribute('href'),
    className: el.className
  })).filter(el => {
    const t = (el.text || el.ariaLabel || '').toLowerCase();
    return t.includes("dự án") || t.includes("project") || t.includes("tạo") || t.includes("create") || t.includes("mới") || t.includes("new");
  });

  return elements;
});

console.log("[Ego] Creation Buttons:", JSON.stringify(creationButtons, null, 2));

// If there's a button like "Dự án mới" or "New Project" or "add", let's click it!
const clicked = await page.evaluate(() => {
  const btn = Array.from(document.querySelectorAll("button, a, div[role='button']")).find(el => {
    const t = (el.innerText || el.getAttribute('aria-label') || '').toLowerCase();
    return t.includes("dự án mới") || t.includes("new project") || t.includes("tạo dự án") || t.includes("create project");
  });
  if (btn) {
    btn.click();
    return { success: true, text: btn.innerText || btn.getAttribute('aria-label') };
  }
  return { success: false };
});

console.log("[Ego] Click New Project:", JSON.stringify(clicked));
await page.waitForTimeout(4000);

const flowUrl = page.url();
console.log("[Ego] Current Flow URL:", flowUrl);

const shotFlowCanvas = "/Volumes/Data/gobi-social/shots/google_flow_canvas_created.png";
await page.screenshot({ path: shotFlowCanvas });
console.log("[Ego] Flow Canvas screenshot saved to:", shotFlowCanvas);

await task.finish({ keep: [page.label] });
