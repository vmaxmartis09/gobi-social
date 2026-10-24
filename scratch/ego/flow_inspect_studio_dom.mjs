/**
 * Inspect Google Flow Studio DOM and controls
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

await page.goto("https://flow.google.com/", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);

// Click New Project
await page.evaluate(() => {
  const btn = document.querySelector(".new-project-button") || 
              Array.from(document.querySelectorAll("button")).find(b => (b.innerText || '').includes("Dự án mới"));
  if (btn) btn.click();
});
await page.waitForTimeout(6000);

const currentUrl = await page.evaluate(() => window.location.href);
console.log("[Ego] Flow Studio URL:", currentUrl);

const domInfo = await page.evaluate(() => {
  // Find all visible text, tools, buttons
  const allText = document.body.innerText;
  const buttons = Array.from(document.querySelectorAll("button, [role='button'], .mat-mdc-button-base")).map(b => ({
    text: (b.innerText || '').trim(),
    ariaLabel: b.getAttribute('aria-label'),
    className: b.className
  })).filter(b => b.text || b.ariaLabel);

  const inputs = Array.from(document.querySelectorAll("input, textarea, [contenteditable='true']")).map(inp => ({
    type: inp.getAttribute('type'),
    placeholder: inp.getAttribute('placeholder'),
    className: inp.className
  }));

  return { allTextSnippet: allText.slice(0, 500), buttons: buttons.slice(0, 30), inputs };
});

console.log("[Ego] DOM Snippet:", domInfo.allTextSnippet);
console.log("[Ego] Inputs:", JSON.stringify(domInfo.inputs, null, 2));
console.log("[Ego] Buttons Sample:", JSON.stringify(domInfo.buttons.slice(0, 15), null, 2));

const shotStudio = "/Volumes/Data/gobi-social/shots/google_flow_studio_full.png";
await page.screenshot({ path: shotStudio });
console.log("[Ego] Full Studio screenshot saved to:", shotStudio);

await task.finish({ keep: [page.label] });
