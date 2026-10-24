const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

const { cookies } = await page.cdp('Network.getAllCookies');
const openaiCookies = cookies.filter(c => c.domain.includes('openai.com') || c.domain.includes('chatgpt.com'));
console.log(`Found ${openaiCookies.length} OpenAI/ChatGPT cookies.`);
console.log("Cookie names:", openaiCookies.map(c => c.name));
