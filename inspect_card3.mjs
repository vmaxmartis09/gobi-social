const task = await claimTaskSpace(4);
const page = task.page("p2");

// Inspect Card 3 and Card 4
const cardDetails = await page.evaluate(() => {
  const cards = Array.from(document.querySelectorAll('flow-grid-tile-container'));
  return cards.map((c, i) => ({
    index: i,
    text: c.textContent.trim(),
    img: c.querySelector('img')?.src
  }));
});
console.log("All canvas cards:", JSON.stringify(cardDetails, null, 2));

// Click on Card 3 (the first successful looking video)
await page.evaluate(() => {
  const cards = Array.from(document.querySelectorAll('flow-grid-tile-container'));
  // Find card with "Gobi speaking cardigan review"
  const target = cards.find(c => c.textContent.includes("Gobi speaking cardigan review"));
  if (target) {
    target.click();
  }
});

await page.waitForTimeout(2000);
await page.screenshot({ path: "C:/Users/HAI/OneDrive/Tài liệu/vmax/shots/ego_gobi_card3_opened.png" });

// Inspect the opened video details
const openedInfo = await page.evaluate(() => {
  const title = document.querySelector('.media-header-title, .title, h1, h2')?.textContent;
  const prompt = document.querySelector('.prompt-text, .prompt-content, [role="article"]')?.textContent;
  const video = document.querySelector('video');
  const allTexts = Array.from(document.querySelectorAll('.panel-content, .drawer, .info-section')).map(el => el.textContent.trim());
  return {
    title,
    prompt,
    allTexts,
    hasVideo: !!video,
    videoDuration: video?.duration
  };
});
console.log("Opened video info:", JSON.stringify(openedInfo, null, 2));
