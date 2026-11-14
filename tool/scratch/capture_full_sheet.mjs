const task = await taskSpace(35);
const page = await task.newPage();
await page.goto("file:///Volumes/Data/gobi-social/shots/gobi_36_contact_sheet.html");
await new Promise(r => setTimeout(r, 2000));
await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight / 2));
await new Promise(r => setTimeout(r, 1000));
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/gobi_36_contact_sheet_middle.png" });

await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
await new Promise(r => setTimeout(r, 1000));
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/gobi_36_contact_sheet_bottom.png" });

console.log("Full contact sheet captured!");
await page.close();
