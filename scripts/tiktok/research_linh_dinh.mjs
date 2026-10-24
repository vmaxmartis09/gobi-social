const shotsDir = "shots/";
const shotPath = `${shotsDir}/fb_linh_dinh_reels.png`;

console.log("[Ego] Mở Task Space nghiên cứu Facebook Reels của Xuân Linh (mr.linh.dinh)...");
const task = await taskSpace("Linh Dinh Reels Research");
const page = task.page("p1");

console.log("[Ego] Đang truy cập https://www.facebook.com/mr.linh.dinh/reels/...");
await page.goto("https://www.facebook.com/mr.linh.dinh/reels/");

try {
  await page.waitForLoadState("domcontentloaded", { timeout: 20000 });
} catch (e) {
  console.log("[Ego] Warning:", e.message);
}

await page.waitForTimeout(4000);

const currentUrl = await page.url();
console.log(`[Ego] URL: ${currentUrl}`);

await page.screenshot({ path: shotPath });
console.log(`[Ego] Đã chụp ảnh lưu tại: ${shotPath}`);

// Lấy danh sách tiêu đề video hoặc text trên trang
try {
  const titles = await page.evaluate(() => {
    const textNodes = Array.from(document.querySelectorAll('span, a, div'))
      .map(el => el.textContent?.trim())
      .filter(t => t && t.length > 10 && t.length < 200);
    return Array.from(new Set(textNodes)).slice(0, 30);
  });
  console.log("[Ego] Nội dung quét được:", JSON.stringify(titles, null, 2));
} catch (e) {
  console.log("[Ego] Eval error:", e.message);
}

// Bàn giao lại cho người dùng xem trên Ego Lite
await task.handOff();
console.log("[Ego] Bàn giao Task Space cho người dùng!");
