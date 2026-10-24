const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("openai.com") || t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/otp_screen.png" });

const elements = await page.evaluate(() => {
  return Array.from(document.querySelectorAll("input, button, a, form")).map(el => ({
    tag: el.tagName,
    type: el.type,
    name: el.name,
    id: el.id,
    placeholder: el.placeholder,
    className: el.className,
    text: el.innerText
  }));
});

console.log("OTP Screen Elements:", JSON.stringify(elements, null, 2));
