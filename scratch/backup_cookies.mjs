import fs from "fs";

const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

const { cookies } = await page.cdp('Network.getAllCookies');
const openaiCookies = cookies.filter(c => c.domain.includes('openai.com') || c.domain.includes('chatgpt.com'));

fs.writeFileSync("/Volumes/Data/gobi-social/scratch/martis_cookies_backup.json", JSON.stringify(openaiCookies, null, 2));
console.log(`Saved ${openaiCookies.length} cookies to scratch/martis_cookies_backup.json`);
