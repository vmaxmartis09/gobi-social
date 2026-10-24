/**
 * Inspect Google Flow Project Creation
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

console.log("[Ego] Connecting to Google Flow home...");
await page.goto("https://flow.google.com/", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

// Find "New Project" or "Create Project" or "+" buttons
const flowActions = await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, a, div[role='button']")).map(b => ({
    text: (b.innerText || '').trim(),
    ariaLabel: b.getAttribute('aria-label'),
    href: b.getAttribute('href'),
    className: b.className
  })).filter(b => b.text || b.ariaLabel);

  return buttons;
});

console.log("[Ego] Flow Actions Sample:", JSON.stringify(flowActions.slice(0, 15), null, 2));

const shotFlow = "/Volumes/Data/gobi-social/shots/google_flow_dashboard.png";
await page.screenshot({ path: shotFlow });
console.log("[Ego] Screenshot saved to:", shotFlow);

await task.finish({ keep: [page.label] });
