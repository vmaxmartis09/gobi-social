const task = await taskSpace("AI Flow Video Production");
const page = task.page("p2");

const details = await page.evaluate(() => {
  // Find all cards or elements in canvas and chat
  const cards = Array.from(document.querySelectorAll('[role="button"], [role="img"], [role="article"], .cdk-drag, mat-card, .asset-card, [tabindex="0"]')).map(el => {
    return {
      tagName: el.tagName,
      className: el.className,
      ariaLabel: el.getAttribute('aria-label'),
      text: el.textContent?.trim().slice(0, 100),
      rect: el.getBoundingClientRect()
    };
  });
  
  // Find all image sources
  const imgs = Array.from(document.querySelectorAll('img')).map(img => ({
    src: img.src?.slice(0, 100),
    alt: img.alt,
    ariaLabel: img.getAttribute('aria-label'),
    w: img.naturalWidth,
    h: img.naturalHeight
  }));
  
  // Find all videos
  const vids = Array.from(document.querySelectorAll('video')).map(v => ({
    src: v.src,
    currentSrc: v.currentSrc,
    duration: v.duration
  }));

  return { cards: cards.filter(c => c.ariaLabel || c.text?.includes("Gobi") || c.text?.includes("play")), imgs, vids };
});

console.log("Details:", JSON.stringify(details, null, 2));
