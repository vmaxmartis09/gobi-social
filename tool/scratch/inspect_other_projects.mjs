const task = await taskSpace("Google Flow Check Projects");
const page = task.page("p1");

const projectIds = [
  "b3c2d9f6-d452-40a2-96f6-c7c92fd7bf7a",
  "97437688-2b73-4a07-9091-77969b802e73"
];

for (const pid of projectIds) {
  const url = `https://flow.google.com/project/${pid}`;
  console.log(`\n[Ego] Checking project: ${url}...`);
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
  await page.waitForTimeout(3000);
  
  // Click "Nhân vật"
  await page.evaluate(() => {
    const all = Array.from(document.querySelectorAll("mat-list-item, .mat-mdc-list-item, button, div"));
    const target = all.find(el => (el.innerText || '').trim().includes("Nhân vật"));
    if (target) target.click();
  });
  await page.waitForTimeout(2500);

  const status = await page.evaluate(() => {
    const tiles = Array.from(document.querySelectorAll("[class*='character-tile'], [class*='char-card'], .tile-container, [class*='character']")).map(t => ({
      text: (t.innerText || '').trim().replace(/\n+/g, ' | '),
      className: t.className,
      img: t.querySelector("img")?.src || null
    }));
    const isEmpty = !!document.querySelector(".is-empty");
    return { title: document.title, isEmpty, tilesCount: tiles.length, sampleTiles: tiles.slice(0, 5) };
  });

  console.log(`[Ego] Result for ${pid}:`, JSON.stringify(status, null, 2));
  const shotPath = `/Volumes/Data/gobi-social/shots/ego_check_char_${pid.slice(0, 8)}.png`;
  await page.screenshot({ path: shotPath });
  console.log(`[Ego] Saved screenshot to ${shotPath}`);
}

await task.finish({ keep: ["p1"] });
