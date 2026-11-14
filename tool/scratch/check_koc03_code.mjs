const task = await taskSpace(35);
const tabs = await task.tabs();
const addyTab = tabs.find(t => t.url?.includes("addy.io"));
const gmailTab = tabs.find(t => t.url?.includes("mail.google.com"));

console.log("Checking Addy aliases...");
await addyTab.page.goto("https://app.addy.io/aliases");
await new Promise(r => setTimeout(r, 4000));

const aliases = await addyTab.page.evaluate(() => {
  return Array.from(document.querySelectorAll("tr")).map(r => r.innerText.replace(/\n+/g, " | "));
});
console.log("Addy top 3 rows:", aliases.slice(0, 3));

console.log("Checking Gmail search...");
await gmailTab.page.goto("https://mail.google.com/mail/u/0/#search/koc03");
await new Promise(r => setTimeout(r, 4000));

const emails = await gmailTab.page.evaluate(() => {
  return Array.from(document.querySelectorAll("tr[role=row]")).map(r => r.innerText.replace(/\n+/g, " | ")).slice(0, 3);
});
console.log("Top Gmail search rows for koc03:", emails);
