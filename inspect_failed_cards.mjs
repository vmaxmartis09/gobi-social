const task = await claimTaskSpace(4);
const page = task.page("p2");

const errorDetails = await page.evaluate(() => {
  const failedCards = Array.from(document.querySelectorAll('flow-grid-tile-container')).filter(c => 
    c.textContent.includes("Không thành công") || c.textContent.includes("Rất tiếc")
  );
  
  return failedCards.map(c => {
    const errorText = c.textContent.trim();
    const buttons = Array.from(c.querySelectorAll('button')).map(b => ({
      ariaLabel: b.getAttribute('aria-label'),
      title: b.getAttribute('title'),
      text: b.textContent.trim()
    }));
    return { errorText, buttons };
  });
});

console.log("Failed cards details:", JSON.stringify(errorDetails, null, 2));
