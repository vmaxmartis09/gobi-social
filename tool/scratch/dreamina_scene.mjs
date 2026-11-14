// Usage: ego-browser nodejs < dreamina_scene.mjs   (SCENE injected by sed below)
const fs = await import("node:fs/promises");
const SCENE = "__SCENE__";
const PROMPT = `__PROMPT__`;
const b64 = (await fs.readFile("/Volumes/Data/gobi-social/assets/koc_dna/MASTER_GOBI_OFFICIAL.jpg")).toString("base64");
const task = await taskSpace("gobi video tool comparison");
const page = task.page("p1");
await page.goto("https://dreamina.capcut.com/ai-tool/generate/?type=video");
await page.waitForLoadState();
await page.waitForTimeout(3000);
await page.evaluate((b64) => {
  const bin = atob(b64); const u = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
  const dt = new DataTransfer(); dt.items.add(new File([u], "MASTER_GOBI_OFFICIAL.jpg", { type: "image/jpeg" }));
  const t = document.querySelector("[contenteditable=true]"); t.focus();
  t.dispatchEvent(new ClipboardEvent("paste", { clipboardData: dt, bubbles: true, cancelable: true }));
}, b64);
await page.waitForTimeout(5000);
await page.evaluate(() => { const el = [...document.querySelectorAll("*")].filter(e => e.children.length === 0 && e.textContent.trim() === "16:9").pop(); el && el.click(); });
await page.waitForTimeout(800);
await page.evaluate(() => { const el = [...document.querySelectorAll("*")].filter(e => e.children.length === 0 && e.textContent.trim() === "9:16").pop(); el && el.click(); });
await page.keyboard.press("Escape");
await page.evaluate(() => { const e = document.querySelector("[contenteditable=true]"); e.focus(); const r = document.createRange(); r.selectNodeContents(e); r.collapse(false); const s = getSelection(); s.removeAllRanges(); s.addRange(r); });
await page.keyboard.insertText(" " + PROMPT);
await page.waitForTimeout(800);
console.log(SCENE, "typed:", await page.evaluate(() => document.querySelector("[contenteditable=true]").innerText.slice(0, 120)));
console.log(await page.screenshot());
