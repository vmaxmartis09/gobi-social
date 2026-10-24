import fs from "fs";
import path from "path";

const task = await claimTaskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com"));
const gmailTab = tabs.find(t => t.url?.includes("mail.google.com"));

const page = chatgptTab.page;
const gmailPage = gmailTab ? gmailTab.page : await task.newPage("https://mail.google.com/mail/u/0/#inbox");

const NEW_EMAIL = "worker02.gobi@gobikoc.anonaddy.me";
const NEW_PASS = "GobiKoc2026@Pass!";

console.log(`[Register] Target Email: ${NEW_EMAIL}`);

// 1. Click Sign up for free
console.log("[Register] Clicking 'Sign up for free'...");
await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll("button, a"));
  const signup = btns.find(b => b.innerText?.toLowerCase().includes("sign up"));
  if (signup) signup.click();
});
await page.waitForTimeout(3000);

// Screenshot to see signup form
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_screen_01.png" });

// 2. Type email
console.log("[Register] Filling email...");
await page.fill("input[name=\"email\"], input[type=\"email\"], #email-input", NEW_EMAIL);
await page.waitForTimeout(1000);

// Click Continue
await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll("button[type=\"submit\"], button"));
  const cont = btns.find(b => b.innerText?.toLowerCase().includes("continue") || b.innerText?.toLowerCase().includes("tiếp tục"));
  if (cont) cont.click();
});
await page.waitForTimeout(3000);

// Screenshot password form
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_screen_02_password.png" });

// 3. Type password
console.log("[Register] Filling password...");
await page.fill("input[name=\"password\"], input[type=\"password\"], #password", NEW_PASS);
await page.waitForTimeout(1000);

// Click Continue
await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll("button[type=\"submit\"], button"));
  const cont = btns.find(b => b.innerText?.toLowerCase().includes("continue") || b.innerText?.toLowerCase().includes("tiếp tục"));
  if (cont) cont.click();
});
await page.waitForTimeout(5000);

// Screenshot OTP screen
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_screen_03_otp.png" });
console.log("Password submitted. Waiting 10s for OTP email to arrive in Gmail...");
await page.waitForTimeout(10000);

// 4. Fetch OTP from Gmail
console.log("[Register] Fetching OTP from Gmail tab...");
await gmailPage.bringToFront();
await gmailPage.goto("https://mail.google.com/mail/u/0/#inbox");
await gmailPage.waitForTimeout(4000);

const otpCode = await gmailPage.evaluate(() => {
  const rows = Array.from(document.querySelectorAll("tr.zA, div.y6, span.bog"));
  for (const r of rows) {
    const text = r.innerText || "";
    if (text.includes("OpenAI") || text.includes("ChatGPT") || text.includes("verification code")) {
      const match = text.match(/\b\d{6}\b/);
      if (match) return match[0];
    }
  }
  const bodyText = document.body.innerText;
  const matches = bodyText.match(/\b\d{6}\b/g);
  return matches && matches.length > 0 ? matches[0] : null;
});

console.log(`[Register] Retrieved OTP Code: ${otpCode}`);
await gmailPage.screenshot({ path: "/Volumes/Data/gobi-social/shots/gmail_latest_otp.png" });

if (!otpCode) {
  console.error("Could not find OTP code in Gmail!");
  process.exit(1);
}

// 5. Enter OTP in ChatGPT
await page.bringToFront();
console.log(`[Register] Entering OTP code: ${otpCode}`);
await page.fill("input[name=\"code\"], input[type=\"text\"][maxlength=\"6\"], input[autocomplete=\"one-time-code\"], #code", otpCode);
await page.waitForTimeout(4000);

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_screen_04_after_otp.png" });

// 6. Fill details (Name and birthday if prompted)
console.log("[Register] Checking onboarding details...");
await page.evaluate(() => {
  const nameInputs = Array.from(document.querySelectorAll("input[type=\"text\"], input[name*=\"name\"]"));
  if (nameInputs.length > 0) nameInputs[0].value = "Nguyen Thanh Gobi";
});
await page.waitForTimeout(1000);

await page.evaluate(() => {
  const submitBtn = Array.from(document.querySelectorAll("button")).find(b => 
    b.innerText?.toLowerCase().includes("agree") || 
    b.innerText?.toLowerCase().includes("tiếp tục") || 
    b.innerText?.toLowerCase().includes("continue")
  );
  if (submitBtn) submitBtn.click();
});
await page.waitForTimeout(5000);

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_screen_05_finished.png" });
console.log("[Register] Worker02 registration complete and logged in!");
