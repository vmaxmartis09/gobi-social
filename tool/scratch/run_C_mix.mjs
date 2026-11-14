// Usage: ego-browser nodejs < dreamina_scene.mjs   (SCENE injected by sed below)
const fs = await import("node:fs/promises");
const SCENE = "C_mix";
const PROMPT = `Full-body shot. The woman from the first reference image wearing exactly the off-white slub-knit long-sleeve henley top from the second reference image over a black skirt, in a bright elegant home interior with a staircase. She slowly turns around to show the relaxed straight fit, smooths the sleeve, and smiles to camera. No speech, only soft ambient sound. Consistent face and outfit, cinematic fashion KOC vlog style, vertical 9:16, subject inside TikTok safe zone, no text, no logo.`;
const FILES = ["/Volumes/Data/gobi-social/assets/koc_dna/MASTER_GOBI_OFFICIAL.jpg","/Volumes/Data/gobi-social/scratch/garment_BJ001.jpg"];
const imgs = [];
for (const f of FILES) imgs.push({name: f.split("/").pop(), b64: (await fs.readFile(f)).toString("base64")});
const task = await taskSpace("gobi video tool comparison");
const page = task.page("p1");
await page.goto("https://dreamina.capcut.com/ai-tool/generate/?type=video");
await page.waitForLoadState();
await page.waitForTimeout(3000);
for (const im of imgs) {
  await page.evaluate((im) => {
    const bin = atob(im.b64); const u = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    const dt = new DataTransfer(); dt.items.add(new File([u], im.name, { type: "image/jpeg" }));
    const t = document.querySelector("[contenteditable=true]"); t.focus();
    t.dispatchEvent(new ClipboardEvent("paste", { clipboardData: dt, bubbles: true, cancelable: true }));
  }, im);
  await page.waitForTimeout(3500);
}
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
