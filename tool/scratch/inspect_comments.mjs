const task = await taskSpace("Inspect FB Comments");
const page = task.page("p1");

try {
  await page.goto("https://www.facebook.com/reel/1104369265315017", { waitUntil: "domcontentloaded", timeout: 20000 });
  await new Promise(r => setTimeout(r, 4000));
  
  // Click on the comments icon/button if needed
  // In the screenshot, the comments count is "815" with a speech bubble icon.
  const commentButtons = await page.evaluate(() => {
    // Find elements containing 815 or comment aria labels
    const all = Array.from(document.querySelectorAll('*'));
    for (const el of all) {
      if (el.innerText && el.innerText.includes('815') && el.offsetHeight > 0) {
        el.click();
        return "Clicked element with 815";
      }
    }
    return "Not found";
  });
  console.log("Comment click result:", commentButtons);
  
  await new Promise(r => setTimeout(r, 3000));
  
  // Extract comments
  const comments = await page.evaluate(() => {
    // Collect all text from comments container or dialog
    const textNodes = Array.from(document.querySelectorAll('div[role="article"], div[dir="auto"], span[dir="auto"]'))
      .map(el => el.innerText?.trim())
      .filter(t => t && t.length > 5 && !t.includes("cybersecurity") && !t.includes("سيكلينك"));
    return Array.from(new Set(textNodes)).slice(0, 50);
  });
  
  console.log("Extracted comments:", comments);
  
  await page.screenshot({ path: "/Volumes/Data/gobi-social/shots/reel_comments.png" });
} catch (e) {
  console.error(e);
} finally {
  await task.finish({ keep: [] });
}
