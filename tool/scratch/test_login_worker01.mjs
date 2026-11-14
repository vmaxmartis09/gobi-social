const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

console.log("Typing email worker01.gobi@gobikoc.anonaddy.me...");
await page.fill("input#email", "worker01.gobi@gobikoc.anonaddy.me");
await new Promise(r => setTimeout(r, 1000));

console.log("Clicking Continue submit button...");
await page.click("button[type=submit]");
await new Promise(r => setTimeout(r, 5000));

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/chatgpt_after_email_submit.png" });

const state = await page.evaluate(() => {
  return {
    url: window.location.href,
    title: document.title,
    bodySnippet: document.body.innerText.slice(0, 500)
  };
});

console.log("State after submit:", state);
