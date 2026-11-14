// Inspect the cards in the Flow project gallery
const task = await taskSpace("VMAX_Flow_Inspect_Cards");
const page = task.page("p1");

await page.goto("https://flow.google.com/u/1/project/905a28b7-ceb4-4cf9-b92d-443050bd2d43");
await page.waitForLoadState();
await page.waitForTimeout(3000);

const cards = await page.evaluate(() => {
  const allCards = Array.from(document.querySelectorAll("[class*='card'], [class*='media'], [class*='item'], [class*='asset']"));
  return allCards.map(c => ({
    text: (c.innerText || '').trim(),
    role: c.getAttribute('role'),
    className: c.className
  })).filter(c => c.text);
});

console.log("[Ego] Cards:", JSON.stringify(cards, null, 2));
await task.finish({ keep: [] });
