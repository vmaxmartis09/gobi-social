const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

console.log("Navigating to chat 1: https://chatgpt.com/c/6ad671f4-2be4-83ec-b1ba-ae1de3600550...");
await page.goto("https://chatgpt.com/c/6ad671f4-2be4-83ec-b1ba-ae1de3600550");
await new Promise(r => setTimeout(r, 4000));

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/chat_1_content.png" });

const info1 = await page.evaluate(() => {
  const msgs = Array.from(document.querySelectorAll("[data-message-author-role]")).map(m => ({
    role: m.getAttribute("data-message-author-role"),
    text: m.innerText.slice(0, 200)
  }));
  return { msgs };
});

console.log("Chat 1 messages:", JSON.stringify(info1, null, 2));

console.log("Navigating to chat 2: https://chatgpt.com/c/6ad6715f-5bc0-83ec-886e-1804642607e3...");
await page.goto("https://chatgpt.com/c/6ad6715f-5bc0-83ec-886e-1804642607e3");
await new Promise(r => setTimeout(r, 4000));

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/chat_2_content.png" });

const info2 = await page.evaluate(() => {
  const msgs = Array.from(document.querySelectorAll("[data-message-author-role]")).map(m => ({
    role: m.getAttribute("data-message-author-role"),
    text: m.innerText.slice(0, 200)
  }));
  return { msgs };
});

console.log("Chat 2 messages:", JSON.stringify(info2, null, 2));
