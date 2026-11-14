const task = await taskSpace(35);
const p2 = task.page("p2");
await p2.goto("https://mail.google.com/mail/u/0/#search/in:anywhere+ChatGPT");
await new Promise(r => setTimeout(r, 4000));

// Click first row
await p2.evaluate(() => {
  const rows = Array.from(document.querySelectorAll("tr[role=\"row\"]"));
  if (rows.length > 0) rows[0].click();
});
await new Promise(r => setTimeout(r, 4000));

await p2.screenshot({ path: "/Volumes/Data/gobi-social/shots/gmail_row1_detail.png" });

const detail = await p2.evaluate(() => {
  return {
    url: window.location.href,
    text: document.body.innerText.slice(0, 2000)
  };
});
console.log("Row 1 Text:", detail.text);
