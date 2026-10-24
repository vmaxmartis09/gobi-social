const task = await taskSpace(35);
const page = await task.newPage();
await page.goto("file:///Volumes/Data/gobi-social/shots/gobi_36_contact_sheet.html");
await new Promise(r => setTimeout(r, 3000));
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/gobi_36_contact_sheet_preview.png", fullPage: false });
console.log("Contact sheet screenshot captured!");
await page.close();
