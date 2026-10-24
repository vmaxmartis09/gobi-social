const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("openai.com") || t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

const fields = await page.evaluate(() => {
  return Array.from(document.querySelectorAll("input, button")).map(el => ({
    tag: el.tagName,
    name: el.name,
    id: el.id,
    type: el.type,
    placeholder: el.placeholder,
    text: el.innerText
  }));
});

console.log("About you fields:", JSON.stringify(fields, null, 2));
