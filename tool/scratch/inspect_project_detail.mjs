const task = await taskSpace("Google Flow Project Detail");
const page = task.page("p1");

const url = "https://flow.google.com/project/3216ade9-8f46-4a7b-bf2a-695e49698f15";
console.log("[Ego] Navigating to project:", url);
await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
await page.waitForTimeout(4000);

// Screenshot of project studio
const shotStudio = "/Volumes/Data/gobi-social/shots/ego_flow_project_studio.png";
await page.screenshot({ path: shotStudio });
console.log("[Ego] Studio screenshot saved to:", shotStudio);

// Check sidebar items (Nhân vật, Thư viện, Canvas, etc.)
const sidebarItems = await page.evaluate(() => {
  const items = Array.from(document.querySelectorAll("mat-list-item, .mat-mdc-list-item, [role='listitem'], nav a, aside button")).map(el => (el.innerText || '').trim().replace(/\n+/g, ' '));
  return items;
});
console.log("[Ego] Sidebar items:", sidebarItems);

// Navigate to "Nhân vật"
console.log("[Ego] Clicking 'Nhân vật' tab...");
const clickedChar = await page.evaluate(() => {
  const all = Array.from(document.querySelectorAll("mat-list-item, .mat-mdc-list-item, button, [role='button'], a, div"));
  const target = all.find(el => (el.innerText || '').trim() === "Nhân vật" || (el.innerText || '').includes("Nhân vật"));
  if (target) {
    target.click();
    return true;
  }
  return false;
});
console.log("[Ego] Clicked 'Nhân vật':", clickedChar);
await page.waitForTimeout(3000);

const shotCharTab = "/Volumes/Data/gobi-social/shots/ego_flow_characters_tab.png";
await page.screenshot({ path: shotCharTab });
console.log("[Ego] Characters tab screenshot saved to:", shotCharTab);

// Inspect existing characters in the character tab
const charList = await page.evaluate(() => {
  const tiles = Array.from(document.querySelectorAll("[class*='character'], [class*='char-card'], [class*='tile'], mat-card")).map(c => ({
    text: (c.innerText || '').trim().replace(/\n+/g, ' | '),
    className: c.className,
    imgSrc: c.querySelector("img")?.src || null
  }));
  const buttons = Array.from(document.querySelectorAll("button, [role='button']")).map(b => (b.innerText || b.getAttribute('aria-label') || '').trim()).filter(Boolean);
  return { tiles: tiles.slice(0, 10), buttons: buttons.slice(0, 15) };
});

console.log("[Ego] Characters List:", JSON.stringify(charList, null, 2));

await task.finish({ keep: ["p1"] });
