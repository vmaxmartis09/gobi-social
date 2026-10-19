import path from "node:path";

const shotsDir = "C:/Users/HAI/OneDrive/Tài liệu/vmax/shots";
const shotPath = `${shotsDir}/tiktok_space_live.png`;

console.log("[Ego] Khởi tạo / Kết nối Task Space: 'TikTok Space'...");
const task = await taskSpace("TikTok Space");
console.log(`[Ego] Task Space ID: ${task.spaceId}`);

const page = task.page("p1");
console.log("[Ego] Đang mở TikTok (@me)...");
await page.goto("https://www.tiktok.com/@me");

try {
  await page.waitForLoadState("domcontentloaded", { timeout: 15000 });
} catch (e) {
  console.log("[Ego] Load state warning:", e.message);
}

// Chờ 3 giây để TikTok nạp session và render giao diện
await page.waitForTimeout(3000);

const currentUrl = page.url();
console.log(`[Ego] URL hiện tại: ${currentUrl}`);

await page.screenshot({ path: shotPath });
console.log(`[Ego] Đã chụp ảnh trạng thái lưu tại: ${shotPath}`);

// Chuyển giao quyền điều khiển Task Space cho người dùng trên Ego Lite
console.log("[Ego] Bàn giao Task Space cho người dùng trên Ego Lite...");
await task.handOff();
console.log("[Ego] Hoàn tất! Task Space 'TikTok Space' hiện đang mở sẵn trên Ego Lite.");
