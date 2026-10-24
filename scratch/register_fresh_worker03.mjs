const task = await taskSpace(35);
const p1 = task.page("p1");
const p2 = task.page("p2");

const TARGET_EMAIL = "koc.worker.03@gobikoc.anonaddy.com";
const TARGET_PASS = "GobiKoc2026@Pass!";

console.log(`[Signup Worker03] Navigating to ChatGPT login/signup with ${TARGET_EMAIL}...`);

// Navigate to signup
await p1.goto("https://chatgpt.com/auth/login");
await new Promise(r => setTimeout(r, 4000));

// Click Sign up button
await p1.evaluate(() => {
  const btns = Array.from(document.querySelectorAll("button, a"));
  const signup = btns.find(b => b.innerText?.toLowerCase().includes("sign up") || b.innerText?.toLowerCase().includes("đăng ký"));
  if (signup) signup.click();
});
await new Promise(r => setTimeout(r, 4000));

await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_worker03_step1.png" });

// Enter email
console.log(`[Signup Worker03] Filling email: ${TARGET_EMAIL}`);
await p1.evaluate((email) => {
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
await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_worker03_step2_pass.png" });

// Enter password
console.log("[Signup Worker03] Filling password...");
await p1.evaluate((pass) => {
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

await new Promise(r => setTimeout(r, 6000));
await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_worker03_step3_otp.png" });

console.log("[Signup Worker03] Password submitted. Waiting 10s for OTP to arrive in Gmail Spam...");
await new Promise(r => setTimeout(r, 10000));

// Check Gmail Spam for fresh OTP
await p2.goto("https://mail.google.com/mail/u/0/#spam");
await new Promise(r => setTimeout(r, 5000));

const topSpamText = await p2.evaluate(() => {
  const rows = Array.from(document.querySelectorAll("div[role=\"main\"] tr.zA"));
  if (rows.length > 0) {
    return rows[0].innerText.replace(/\n/g, " | ");
  }
  return null;
});
console.log("[Signup Worker03] Top spam row:", topSpamText);

// Click top spam row to open
await p2.evaluate(() => {
  const rows = Array.from(document.querySelectorAll("div[role=\"main\"] tr.zA"));
  if (rows.length > 0) rows[0].click();
});
await new Promise(r => setTimeout(r, 4000));

await p2.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_worker03_opened_email.png" });

const otpData = await p2.evaluate(() => {
  const text = document.querySelector("div[role=\"main\"]")?.innerText || document.body.innerText;
  const match = text.match(/\b\d{6}\b/);
  return {
    otp: match ? match[0] : null,
    snippet: text.slice(0, 1000)
  };
});

console.log(`[Signup Worker03] Extracted OTP: ${otpData.otp}`);

if (otpData.otp) {
  // Go back to p1 and enter OTP
  console.log(`[Signup Worker03] Entering OTP ${otpData.otp} into p1...`);
  await p1.evaluate((code) => {
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
  await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_worker03_after_otp.png" });

  // Check if onboarding form asks for Name & Birthday
  await p1.evaluate(() => {
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
  await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/signup_worker03_final.png" });
  console.log("[Signup Worker03] Worker03 setup completed!");
} else {
  console.error("[Signup Worker03] Failed to retrieve OTP for worker03.");
}
