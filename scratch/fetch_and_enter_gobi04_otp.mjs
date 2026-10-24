const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com") || t.url?.includes("openai.com"));
const gmailTab = tabs.find(t => t.url?.includes("mail.google.com"));

const page = chatgptTab.page;
const gmailPage = gmailTab.page;

console.log("[OTP] Navigating Gmail to Spam folder...");
await gmailPage.goto("https://mail.google.com/mail/u/0/#spam");
await new Promise(r => setTimeout(r, 4000));

await gmailPage.screenshot({ path: "/Volumes/Data/gobi-social/shots/gmail_spam_for_gobi04.png" });

// Get list of emails in Spam
const spamRows = await gmailPage.evaluate(() => {
  const rows = Array.from(document.querySelectorAll("div[role=\"main\"] tr.zA"));
  return rows.map((r, i) => ({
    i,
    text: r.innerText.replace(/\n/g, " | ")
  }));
});
console.log("Spam rows:", JSON.stringify(spamRows, null, 2));

// Open top item
console.log("[OTP] Opening top spam email...");
await gmailPage.evaluate(() => {
  const rows = Array.from(document.querySelectorAll("div[role=\"main\"] tr.zA"));
  if (rows.length > 0) rows[0].click();
});
await new Promise(r => setTimeout(r, 4000));

await gmailPage.screenshot({ path: "/Volumes/Data/gobi-social/shots/gmail_gobi04_opened.png" });

const detail = await gmailPage.evaluate(() => {
  const text = document.querySelector("div[role=\"main\"]")?.innerText || document.body.innerText;
  const match = text.match(/\b\d{6}\b/);
  return {
    code: match ? match[0] : null,
    snippet: text.slice(0, 1000)
  };
});
console.log("[OTP] Extracted Code:", detail.code);

if (detail.code) {
  console.log(`[OTP] Submitting code ${detail.code} on ChatGPT page...`);
  await page.evaluate((code) => {
    const input = document.querySelector("input[name=\"code\"], input[type=\"text\"], input[autocomplete=\"one-time-code\"], input");
    if (input) {
      input.focus();
      input.value = code;
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
    }
    const cont = Array.from(document.querySelectorAll("button")).find(b => 
      b.innerText?.trim() === "Continue" || b.innerText?.trim() === "Tiếp tục"
    );
    if (cont) cont.click();
  }, detail.code);

  await new Promise(r => setTimeout(r, 6000));
  await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/after_entering_gobi04_otp.png" });

  // Onboarding (Name & Birthday if prompted)
  console.log("[OTP] Checking onboarding form...");
  await page.evaluate(() => {
    const nameInput = document.querySelector("input[name=\"name\"], input[placeholder*=\"Full name\"], input[type=\"text\"]");
    if (nameInput) {
      nameInput.focus();
      nameInput.value = "Nguyen Thanh Gobi";
      nameInput.dispatchEvent(new Event("input", { bubbles: true }));
      nameInput.dispatchEvent(new Event("change", { bubbles: true }));
    }
    const cont = Array.from(document.querySelectorAll("button")).find(b => 
      b.innerText?.toLowerCase().includes("agree") || 
      b.innerText?.toLowerCase().includes("tiếp tục") || 
      b.innerText?.toLowerCase().includes("continue")
    );
    if (cont) cont.click();
  });

  await new Promise(r => setTimeout(r, 6000));
  await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/gobi04_logged_in.png" });
  console.log("[OTP] Registration flow complete!");
} else {
  console.error("[OTP] Failed to find OTP code!");
}
