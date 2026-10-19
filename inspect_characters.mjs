const task = await taskSpace("AI Flow Video Production");
const page = task.page("p2");

// Let's inspect all character elements and canvas cards
const elements = await page.evaluate(() => {
  const allCards = Array.from(document.querySelectorAll('*')).filter(el => {
    const text = el.textContent?.trim();
    return text === "Gobi (ADN Mới)" || text === "Gobi";
  }).map(el => {
    let p = el;
    while (p && p.parentElement && !p.classList.contains('cdk-drag') && p.tagName !== 'MAT-CARD' && !p.getAttribute('role')) {
      p = p.parentElement;
    }
    const rect = el.getBoundingClientRect();
    return {
      tagName: el.tagName,
      className: el.className,
      text: el.textContent.trim(),
      parentTag: p?.tagName,
      parentClass: p?.className,
      rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
    };
  });
  
  return { allCards };
});

console.log("Character cards:", JSON.stringify(elements, null, 2));
