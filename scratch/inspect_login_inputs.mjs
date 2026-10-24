const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
const page = chatgptTab.page;

const inputs = await page.evaluate(() => {
  return Array.from(document.querySelectorAll("input, button, a")).map(el => ({
    tag: el.tagName,
    type: el.type,
    name: el.name,
    id: el.id,
    text: el.innerText,
    ariaLabel: el.getAttribute("aria-label"),
    placeholder: el.placeholder
  }));
});

console.log("Inputs and interactive elements:", JSON.stringify(inputs.filter(i => i.placeholder || i.name || i.text), null, 2));
