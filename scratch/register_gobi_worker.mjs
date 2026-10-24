const task = await taskSpace(35);
const tabs = await task.tabs();
const chatgptTab = tabs.find(t => t.url?.includes("chatgpt.com") || t.url?.includes("openai.com"));
const gmailTab = tabs.find(t => t.url?.includes("mail.google.com"));

const page = chatgptTab.page;
const gmailPage = gmailTab ? gmailTab.page : await task.newPage("https://mail.google.com/mail/u/0/#spam");

const TARGET_EMAIL = "koc.gobi.04@gobikoc.anonaddy.com";
const TARGET_PASS = "GobiKoc2026@Pass!";

console.log(`[Auto Signup] Target Email: ${TARGET_EMAIL}`);

// 1. Clear cookies
console.log("[Auto Signup] Clearing OpenAI cookies...");
const { cookies } = await page.cdp("Network.getAllCookies");
for (const c of cookies.filter(c => c.domain.includes("openai.com") || c.domain.includes("chatgpt.com"))) {
  await page.cdp("Network.deleteCookies", { name: c.name, domain: c.domain, path: c.path });
}

// 2. Navigate to signup
console.log("[Auto Signup] Going to https://chatgpt.com/auth/login...");
await page.goto("https://chatgpt.com/auth/login");
await new Promise(r => setTimeout(r, 4000));

console.log("[Auto Signup] Clicking Sign up...");
await page.evaluate(() => {
  const btns = Array.from(document.querySelectorAll("button, a"));
  const signup = btns.find(b => b.innerText?.toLowerCase().includes("sign up") || b.innerText?.toLowerCase().includes("đăng ký"));
  if (signup) signup.click();
});
await new Promise(r => setTimeout(r, 4000));

await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_screen_email.png" });

// 3. Type email
console.log("[Auto Signup] Typing email...");
await page.evaluate((email) => {
  const input = document.querySelector("input[name=\"email\"], input[type=\"email\"], #email-input, input");
  if (input) {
    input.focus();
    input.value = email;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  }
  const cont = Array.from(document.querySelectorAll("button[type=\"submit\"], button")).find(b => 
    b.innerText?.toLowerCase().includes("continue") || b.innerText?.toLowerCase().includes("tiếp tục")
  );
  if (cont) cont.click();
}, TARGET_EMAIL);

await new Promise(r => setTimeout(r, 4000));
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_screen_pass.png" });

// 4. Type password
console.log("[Auto Signup] Typing password...");
await page.evaluate((pass) => {
  const input = document.querySelector("input[name=\"password\"], input[type=\"password\"], #password");
  if (input) {
    input.focus();
    input.value = pass;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  }
  const cont = Array.from(document.querySelectorAll("button[type=\"submit\"], button")).find(b => 
    b.innerText?.toLowerCase().includes("continue") || b.innerText?.toLowerCase().includes("tiếp tục")
  );
  if (cont) cont.click();
}, TARGET_PASS);

await new Promise(r => setTimeout(r, 7000));
await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_screen_otp.png" });

console.log("[Auto Signup] Password submitted. Waiting 12s for OTP email to arrive in Gmail Spam...");
await new Promise(r => setTimeout(r, 12000));

// 5. Check Gmail Spam
console.log("[Auto Signup] Checking Gmail spam for new OTP...");
await gmailPage.goto("https://mail.google.com/mail/u/0/#spam");
await new Promise(r => setTimeout(r, 4000));

// Click top spam row
await gmailPage.evaluate(() => {
  const rows = Array.from(document.querySelectorAll("div[role=\"main\"] tr.zA"));
  if (rows.length > 0) rows[0].click();
});
await new Promise(r => setTimeout(r, 4000));

await gmailPage.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_otp_email_body.png" });

const otpData = await gmailPage.evaluate(() => {
  const text = document.querySelector("div[role=\"main\"]")?.innerText || document.body.innerText;
  const match = text.match(/\b\d{6}\b/);
  return {
    otp: match ? match[0] : null,
    snippet: text.slice(0, 500)
  };
});
console.log("[Auto Signup] Extracted OTP code:", otpData.otp);

if (otpData.otp) {
  console.log(`[Auto Signup] Entering OTP ${otpData.otp} into ChatGPT...`);
  await page.evaluate((code) => {
    const input = document.querySelector("input[name=\"code\"], input[type=\"text\"], input[autocomplete=\"one-time-code\"], input");
    if (input) {
      input.focus();
      input.value = code;
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
    }
    const cont = Array.from(document.querySelectorAll("button")).find(b => 
      b.innerText?.toLowerCase().includes("continue") || b.innerText?.toLowerCase().includes("tiếp tục")
    );
    if (cont) cont.click();
  }, otpData.otp);

  await new Promise(r => setTimeout(r, 6000));

  // Handle Full Name & Onboarding if prompted
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
  await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_success_state.png" });
  console.log("[Auto Signup] Registration and login completed successfully!");
} else {
  console.error("[Auto Signup] OTP code could not be found!");
}
