import fs from "fs";

const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com") || t.url?.includes("accounts.google.com"));
const page = chatgptTab.page;

console.log("Restoring Martis cookies from backup...");
const raw = fs.readFileSync("/Volumes/Data/gobi-social/scratch/martis_cookies_backup.json", "utf-8");
const cookies = JSON.parse(raw);

for (const c of cookies) {
  try {
    await page.cdp('Network.setCookie', {
      name: c.name,
      value: c.value,
      domain: c.domain,
      path: c.path,
      secure: c.secure,
      httpOnly: c.httpOnly,
      expires: c.expires
    });
  } catch (e) {}
}

console.log("Navigating to https://chatgpt.com/...");
await page.goto("https://chatgpt.com/");
await new Promise(r => setTimeout(r, 4000));

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/chatgpt_restored_martis.png" });

const chats = await page.evaluate(() => {
  const links = Array.from(document.querySelectorAll("a[href*='/c/']")).map(a => ({
    title: a.innerText,
    href: a.href
  }));
  return {
    user: document.body.innerText.includes("Martis") ? "Martis" : "Other",
    links: links.slice(0, 10)
  };
});

console.log("Restored chats:", JSON.stringify(chats, null, 2));
