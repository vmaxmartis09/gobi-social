/**
 * Check Google Flow Character Generation Results
 */
const task = await claimTaskSpace(2);
const page = await task.newPage();

const projectUrl = "https://flow.google.com/project/b3c2d9f6-d452-40a2-96f6-c7c92fd7bf7a";
await page.goto(projectUrl, { waitUntil: "domcontentloaded" });
await page.waitForTimeout(4000);

// Navigate to "Nhân vật"
await page.evaluate(() => {
  const listItems = Array.from(document.querySelectorAll("mat-list-item, .mat-mdc-list-item"));
  const charItem = listItems.find(el => el.innerText.includes("Nhân vật"));
  if (charItem) charItem.click();
});
await page.waitForTimeout(4000);

const resultState = await page.evaluate(() => {
  const images = Array.from(document.querySelectorAll("img")).map(img => ({
    src: img.src ? img.src.slice(0, 100) : '',
    alt: img.alt,
    className: img.className
  })).filter(img => img.src && !img.src.includes("googlelogo") && !img.src.includes("ring"));

  const cards = Array.from(document.querySelectorAll("[class*='character'], [class*='card'], [class*='asset'], [class*='candidate']")).map(el => ({
    text: (el.innerText || '').trim(),
    className: el.className
  })).filter(c => c.text);

  const textSnippets = document.body.innerText.slice(0, 600);

  return { images, cards: cards.slice(0, 10), textSnippets };
});

console.log("[Ego] Character Images Generated:", JSON.stringify(resultState.images, null, 2));
console.log("[Ego] Character Cards:", JSON.stringify(resultState.cards, null, 2));
console.log("[Ego] Snippet:", resultState.textSnippets);

const shotResult = "/Volumes/Data/gobi-social/shots/google_flow_character_result.png";
await page.screenshot({ path: shotResult });
console.log("[Ego] Result screenshot saved to:", shotResult);

await task.finish({ keep: [page.label] });
