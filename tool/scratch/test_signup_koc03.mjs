const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("openai.com") || t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

console.log("Navigating to https://chatgpt.com/auth/login...");
await page.goto("https://chatgpt.com/auth/login");
await new Promise(r => setTimeout(r, 4000));

console.log("Filling email koc03@gobikoc.anonaddy.me...");
await page.fill("input#email", "koc03@gobikoc.anonaddy.me");
await new Promise(r => setTimeout(r, 1000));

console.log("Submitting Continue...");
await page.click("button[type=submit]");
await new Promise(r => setTimeout(r, 5000));

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/chatgpt_signup_koc03.png" });

const state = await page.evaluate(() => {
  return {
    url: window.location.href,
    title: document.title,
    body: document.body.innerText.slice(0, 500)
  };
});
console.log("State after submit koc03:", state);
