// Usage: ego-browser nodejs < dreamina_scene.mjs   (SCENE injected by sed below)
const fs = await import("node:fs/promises");
const SCENE = "scene1_hook";
const PROMPT = `Close-up of the woman from the reference image in a cozy cafe, soft smile to camera, gently touching the collar of her cream thin-knit cardigan with pearl shell buttons. She says in Vietnamese: gợi ý chiếc cardigan len mỏng chuẩn vibe nàng thơ đi cafe cuối tuần. Soft natural light, consistent face, cinematic fashion KOC vlog style, vertical 9:16, subject inside TikTok safe zone, no text, no logo.`;
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
