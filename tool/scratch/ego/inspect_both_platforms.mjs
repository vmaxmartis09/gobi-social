/**
 * Navigate to Google Flow home and Kling AI via fresh newPage
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

console.log("[Ego] Navigating to Google Flow root...");
await page.goto("https://flow.google.com/", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});
await page.waitForTimeout(4000);

const flowTitle = await page.title();
const flowUrl = page.url();
console.log("[Ego] Flow Root URL:", flowUrl);
console.log("[Ego] Flow Root Title:", flowTitle);

const shotFlow = "/Volumes/Data/gobi-social/shots/google_flow_home.png";
await page.screenshot({ path: shotFlow });

// Now let's open Kling AI in a second page
const p2 = await task.newPage();
console.log("[Ego] Opening Kling AI...");
await p2.goto("https://kling.ai/app/creations/grid", {
  waitUntil: "domcontentloaded",
  timeout: 45000
});
await p2.waitForTimeout(4000);

const klingTitle = await p2.title();
const klingUrl = p2.url();
console.log("[Ego] Kling URL:", klingUrl);
console.log("[Ego] Kling Title:", klingTitle);

const shotKling = "/Volumes/Data/gobi-social/shots/kling_current_state.png";
await p2.screenshot({ path: shotKling });

// Check Kling UI state: buttons, login status, etc.
const klingState = await p2.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button, a, span")).map(b => (b.innerText || '').trim()).filter(t => t.length > 2 && t.length < 30);
  const isLogin = !buttons.some(t => t.toLowerCase() === "sign in" || t.toLowerCase() === "log in");
  return {
    isLogin,
    buttonsSample: buttons.slice(0, 20)
  };
});

console.log("[Ego] Kling State:", JSON.stringify(klingState, null, 2));

await task.finish({ keep: [page.label, p2.label] });
