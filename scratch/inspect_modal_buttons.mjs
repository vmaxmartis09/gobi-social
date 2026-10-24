const task = await taskSpace(35);
const tabs = await task.tabs();
const addyTab = tabs.find(t => t.url?.includes("addy.io"));
const page = addyTab.page;

const modalButtons = await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll("button, input[type=submit]")).map(b => ({
    text: b.innerText,
    id: b.id,
    className: b.className
  }));
  return btns;
});

console.log("Modal buttons:", JSON.stringify(modalButtons, null, 2));
