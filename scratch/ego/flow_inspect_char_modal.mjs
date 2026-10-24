/**
 * Inspect Google Flow Character modal / panel state
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const projectUrl = "https://flow.google.com/project/b3c2d9f6-d452-40a2-96f6-c7c92fd7bf7a";
await page.goto(projectUrl, { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);

// Inspect the current DOM state in Flow
const modalDetails = await page.evaluate(() => {
  const allInputs = Array.from(document.querySelectorAll("input, textarea, [contenteditable='true']")).map(el => ({
    tag: el.tagName,
    type: el.getAttribute('type'),
    placeholder: el.getAttribute('placeholder'),
    value: el.value || el.innerText,
    className: el.className
  }));

  const allButtons = Array.from(document.querySelectorAll("button, [role='button']")).map(b => ({
    text: (b.innerText || '').trim(),
    ariaLabel: b.getAttribute('aria-label'),
    disabled: b.disabled || b.classList.contains("mat-mdc-button-disabled") || b.getAttribute('aria-disabled') === "true",
    className: b.className
  })).filter(b => b.text || b.ariaLabel);

  const images = Array.from(document.querySelectorAll("img")).map(img => ({
    src: img.src ? img.src.slice(0, 80) : '',
    alt: img.alt,
    className: img.className
  })).filter(img => img.src && !img.src.includes("googlelogo"));

  return { allInputs, allButtons: allButtons.slice(0, 20), images };
});

console.log("[Ego] Modal Inputs:", JSON.stringify(modalDetails.allInputs, null, 2));
console.log("[Ego] Modal Buttons:", JSON.stringify(modalDetails.allButtons.slice(0, 15), null, 2));
console.log("[Ego] Images in View:", JSON.stringify(modalDetails.images, null, 2));

await task.finish({ keep: [page.label] });
