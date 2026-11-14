const task = await taskSpace("Gobi Dashboard Fixed Review");
const page = task.page("p1");

console.log("[Ego] Navigating to http://localhost:3000...");
await page.goto("http://localhost:3000", { waitUntil: "domcontentloaded", timeout: 15000 });
await page.waitForTimeout(3000);

// Screenshot 1: Overview with all 4 jobs
const shotOverview = "/Volumes/Data/gobi-social/shots/dashboard_4_jobs_fixed.png";
await page.screenshot({ path: shotOverview });
console.log("[Ego] 4 Jobs Overview saved to:", shotOverview);

// Click the newly added job card (7678960622423330066)
await page.evaluate(() => {
  const cards = Array.from(document.querySelectorAll(".kokonut-card"));
  const target = cards.find(c => c.innerText.includes("7678960622423330066"));
  if (target) target.click();
});
await page.waitForTimeout(2000);

// Screenshot 2: Detail modal of newly ingested job
const shotModal = "/Volumes/Data/gobi-social/shots/dashboard_new_job_modal_fixed.png";
await page.screenshot({ path: shotModal });
console.log("[Ego] New Job Modal saved to:", shotModal);

await task.finish({ keep: ["p1"] });
