/**
 * Script render Cảnh 1 (Hook) trên Google Flow qua Ego Lite
 */

const task = await taskSpace("VMAX_Flow_Scene1_" + Date.now());
const page = task.page("p1");

console.log("[Ego] Dang mo Google Flow Project Studio...");
await page.goto("https://flow.google.com/u/1/project/905a28b7-ceb4-4cf9-b92d-443050bd2d43", {
  waitUntil: "domcontentloaded",
  timeout: 30000
});

// Cho giao dien studio on dinh
await page.waitForTimeout(4000);

// Kiem tra o nhap ProseMirror
console.log("[Ego] Dang tim o nhap prompt...");
await page.waitForSelector("div.ProseMirror", { timeout: 15000 });
await page.click("div.ProseMirror");
await page.waitForTimeout(600);

const scene1Prompt = "Animate this frame into an 8-second cinematic clip featuring Gobi. CRITICAL: preserve EXACTLY the same warm minimalist Korean aesthetic lookbook, lighting, and color palette shown. Scene: Gobi gently turns her body toward the full-length mirror, softly smiling with a subtle head tilt, showcasing the high-waisted beige trousers. Slow cinematic push-in toward the subject with shallow depth of field. Natural eye contact, realistic breathing motion, smooth natural motion, no jump cuts, no text.";

console.log("[Ego] Dang dan prompt Canh 1 vao ProseMirror...");
await page.keyboard.press("ControlOrMeta+A");
await page.keyboard.press("Backspace");
await page.keyboard.paste({ text: scene1Prompt });
await page.waitForTimeout(1500);

// Chup anh xac nhan da dan prompt
const shotBefore = "shots/ego_flow_scene1_prompt_ready.png";
await page.screenshot({ path: shotBefore });
console.log("[Ego] Da chup anh truoc khi submit:", shotBefore);

// Tim va click nut submit
console.log("[Ego] Dang tim va click nut gui (Submit)...");
const clickResult = await page.evaluate(() => {
  const buttons = Array.from(document.querySelectorAll("button"));
  // Nut submit la nut arrow_forward hoac nut nam o goc phai thanh prompt
  const submitBtn = buttons.find(b => {
    const txt = (b.innerText || '').trim();
    const aria = (b.getAttribute("aria-label") || '').toLowerCase();
    return txt.includes("arrow_forward") || aria.includes("gửi") || aria.includes("submit") || aria.includes("tạo");
  }) || buttons.find(b => {
    // Fallback: tim nut co chua svg mui ten hoac class lien quan
    return b.querySelector("svg, [class*='arrow'], [class*='send']") && b.closest("[class*='prompt'], [class*='bottom']");
  });

  if (submitBtn) {
    submitBtn.scrollIntoView();
    submitBtn.click();
    return { success: true, text: submitBtn.innerText, aria: submitBtn.getAttribute("aria-label") };
  }
  return { success: false };
});

console.log("[Ego] Ket qua click nut submit:", JSON.stringify(clickResult));

// Neu click DOM khong duoc, fallback sang Enter
if (!clickResult.success) {
  console.log("[Ego] Fallback sang Enter key...");
  await page.keyboard.press("Enter");
}

await page.waitForTimeout(3000);

// Chup anh xac nhan sau khi submit
const shotAfter = "shots/ego_flow_scene1_submitted.png";
await page.screenshot({ path: shotAfter });
console.log("[Ego] Da chup anh sau khi submit:", shotAfter);

// Theo doi tien do render (chup anh dinh ky moi 10s)
console.log("[Ego] Bat dau giam sat tien do render...");
for (let i = 1; i <= 6; i++) {
  await page.waitForTimeout(10000);
  const progressShot = `shots/ego_flow_scene1_rendering_${i * 10}s.png`;
  await page.screenshot({ path: progressShot });
  console.log(`[Ego] Tien do ${i * 10}s: da luu anh tai ${progressShot}`);
  
  // Kiem tra trang thai thumbnail render
  const renderStatus = await page.evaluate(() => {
    const text = document.body.innerText || '';
    const hasProgress = /\d+%\s*(hoàn thành|complete|rendering)/i.test(text);
    return { hasProgress, bodySnippet: text.slice(0, 300) };
  });
  console.log(`[Ego] Trang thai phan hoi ${i * 10}s:`, JSON.stringify(renderStatus));
}

// Giu nguyen tab tren trinh duyet Ego Lite
await task.finish({ keep: ["p1"] });
console.log("[Ego] Hoan tat quy trinh render Canh 1!");
