const task = await taskSpace(35);
const p2 = task.page("p2");
await p2.goto("https://mail.google.com/mail/u/0/#search/in:anywhere+564632");
await new Promise(r => setTimeout(r, 4000));
await p2.screenshot({ path: "/Volumes/Data/gobi-social/shots/gmail_search_564632.png" });

const searchInfo = await p2.evaluate(() => {
  const rows = Array.from(document.querySelectorAll("tr.zA, tr[role=\"row\"]"));
  return rows.map((r, i) => ({
    i,
    text: r.innerText.replace(/\n/g, " | ")
  }));
});
console.log("Search 564632 results:", searchInfo);

// If found, click it directly
if (searchInfo.length > 0) {
  await p2.evaluate(() => {
    const el = document.querySelector("tr.zA");
    if (el) el.click();
  });
  await new Promise(r => setTimeout(r, 4000));
  await p2.screenshot({ path: "/Volumes/Data/gobi-social/shots/gmail_564632_opened.png" });
  const bodyText = await p2.evaluate(() => document.body.innerText.slice(0, 2000));
  console.log("Opened body text:", bodyText);
}
