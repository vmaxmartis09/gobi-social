const task = await taskSpace(35);
const p1 = task.page("p1");

console.log("[Worker02] Focusing input on p1...");

// Check if input element is available
const inputDetails = await p1.evaluate(() => {
  const inputs = Array.from(document.querySelectorAll("input"));
  return inputs.map(i => ({
    name: i.name,
    id: i.id,
    type: i.type,
    placeholder: i.placeholder,
    className: i.className
  }));
});
console.log("Inputs found on p1:", inputDetails);

const otpCode = "564632";
console.log(`[Worker02] Entering code: ${otpCode}`);

// Try multiple methods to fill
try {
  await p1.click("input");
  await p1.keyboard.type(otpCode, { delay: 150 });
} catch (e) {
  console.log("Keyboard type notice:", e.message);
}

await p1.evaluate((code) => {
  const input = document.querySelector("input[name=\"code\"], input[type=\"text\"], input[autocomplete=\"one-time-code\"], input");
  if (input) {
    input.focus();
    input.value = code;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  }
  const btn = Array.from(document.querySelectorAll("button")).find(b => 
    b.innerText?.toLowerCase().includes("continue") || 
    b.innerText?.toLowerCase().includes("tiếp tục")
  );
  if (btn) btn.click();
}, otpCode);

await new Promise(r => setTimeout(r, 6000));
await p1.screenshot({ path: "/Volumes/Data/gobi-social/shots/p1_after_otp_submit.png" });

console.log("P1 URL after OTP submit:", p1.url());
