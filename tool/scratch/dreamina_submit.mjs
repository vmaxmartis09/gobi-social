const task = await taskSpace("gobi video tool comparison");
const page = task.page("p1");
const before = await page.evaluate(() => [...document.querySelectorAll("video")].map(v => v.currentSrc || v.src));
await page.evaluate(() => { const b = document.querySelector("button[aria-label=\"Tạo\"]"); b && b.click(); });
await page.waitForTimeout(2500);
await page.evaluate(() => { const b = [...document.querySelectorAll("button")].find(x => x.textContent.trim() === "Xác nhận"); b && b.click(); });
await page.waitForTimeout(8000);
let t = "";
for (let i = 0; i < 45; i++) {
  t = await page.evaluate(() => document.body.innerText);
  if (/Không thể tạo/.test(t)) { console.log("FAILED"); break; }
  if (!/Đang tạo|\d+%/.test(t) && i > 1) break;
  await page.waitForTimeout(6000);
}
const after = await page.evaluate(() => [...document.querySelectorAll("video")].map(v => v.currentSrc || v.src));
console.log("NEW:", JSON.stringify(after.filter(u => !before.includes(u))));
console.log(await page.screenshot());
