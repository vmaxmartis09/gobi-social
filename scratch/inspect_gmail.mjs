const task = await taskSpace(35);
const tabs = await task.tabs();
const gmailTab = tabs.find(t => t.url?.includes("mail.google.com"));

if (!gmailTab) {
  console.log("No Gmail tab found!");
  process.exit(1);
}

const page = gmailTab.page;
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/gmail_current_state.png" });

const info = await page.evaluate(() => {
  const emails = Array.from(document.querySelectorAll("tr[role=row]")).map(r => r.innerText.replace(/\n+/g, " | "));
  return {
    url: window.location.href,
    emailCount: emails.length,
    recent: emails.slice(0, 5)
  };
});

console.log("Gmail Info:", JSON.stringify(info, null, 2));
