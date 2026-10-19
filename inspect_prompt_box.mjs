const task = await claimTaskSpace(4);
const page = task.page("p2");

const promptDetails = await page.evaluate(() => {
  const container = document.querySelector('.bottom-panel, .prompt-box, flow-prompt-input, [role="textbox"]')?.closest('div');
  const chips = Array.from(document.querySelectorAll('mat-chip, .mat-mdc-chip, .ingredient-chip, [role="option"]')).map(c => ({
    text: c.textContent.trim(),
    ariaLabel: c.getAttribute('aria-label')
  }));
  const textBox = document.querySelector('[contenteditable="true"], textarea, input[type="text"]');
  const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
    text: b.textContent.trim(),
    ariaLabel: b.getAttribute('aria-label'),
    disabled: b.disabled
  }));
  
  return {
    chips,
    textBoxHtml: textBox ? textBox.innerHTML : null,
    textBoxText: textBox ? textBox.textContent : null,
    buttons: buttons.filter(b => b.text || b.ariaLabel).slice(-10)
  };
});

console.log("Prompt box details:", JSON.stringify(promptDetails, null, 2));
