const task = await taskSpace("Gobi_Campaign_NEAU");
console.log("Created task space id:", task.id, "name:", task.name);
const page = await task.newPage();
await page.goto("https://chatgpt.com/");
await new Promise(r => setTimeout(r, 4000));
console.log("ChatGPT page title:", await page.title());
const userBtn = await page.evaluate(() => {
  const btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Gobi") || b.innerText.includes("Martis") || b.innerText.includes("Free"));
  return btn ? btn.innerText : "Not found";
});
console.log("Logged in user:", userBtn);
