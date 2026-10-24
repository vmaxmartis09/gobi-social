/**
 * Check Generate button and credit balance in Kling AI
 */
const task = await claimTaskSpace(2);
const page = task.userPage() || await task.newPage();

const btnInfo = await page.evaluate(() => {
  const genBtn = Array.from(document.querySelectorAll("button")).find(b => (b.innerText || '').trim().includes("Generate"));
  const creditEls = Array.from(document.querySelectorAll("[class*='credit'], [class*='balance'], [class*='point'], [class*='coin']")).map(el => (el.innerText || '').trim()).filter(Boolean);
  
  return {
    buttonFound: !!genBtn,
    buttonText: genBtn ? genBtn.innerText : null,
    buttonDisabled: genBtn ? genBtn.disabled || genBtn.classList.contains("is-disabled") : null,
    creditSample: creditEls.slice(0, 5)
  };
});

console.log("[Ego] Generate Button Info:", JSON.stringify(btnInfo, null, 2));

await task.finish({ keep: [page.label] });
