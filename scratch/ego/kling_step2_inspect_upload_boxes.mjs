/**
 * Inspect upload boxes and mode selectors in Kling AI
 */
const task = await claimTaskSpace(2);
const page = task.userPage() || (task.tabs ? (await task.tabs())[0] : null) || await task.newPage();

const uploadBoxes = await page.evaluate(() => {
  const uploadContainers = Array.from(document.querySelectorAll(".el-upload, [class*='upload'], [class*='frame']")).map(el => ({
    text: (el.innerText || '').trim().replace(/\s+/g, ' '),
    className: el.className,
    ariaLabel: el.getAttribute('aria-label')
  })).filter(el => el.text && el.text.length < 50);

  const modeTriggers = Array.from(document.querySelectorAll("[role='tab'], .el-radio-button, [class*='mode'], [class*='tab']")).map(el => ({
    text: (el.innerText || '').trim(),
    className: el.className
  })).filter(el => el.text && el.text.length < 30);

  return { uploadContainers, modeTriggers };
});

console.log("[Ego] Upload Containers:", JSON.stringify(uploadBoxes.uploadContainers.slice(0, 10), null, 2));
console.log("[Ego] Mode Triggers:", JSON.stringify(uploadBoxes.modeTriggers.slice(0, 15), null, 2));

await task.finish({ keep: [page.label] });
