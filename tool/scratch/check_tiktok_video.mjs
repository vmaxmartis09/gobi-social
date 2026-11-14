import { writeFile } from "node:fs/promises";

const task = await taskSpace("check tiktok video");
const page = task.page("p1");

// Listen to network requests or responses if possible, or evaluate page after load
await page.goto("https://www.tiktok.com/@beenalth/video/7678960622423330066");
await new Promise(r => setTimeout(r, 5000));

const pageInfo = await page.evaluate(() => {
  // Check for universal data or sigi state or script tags
  const scripts = Array.from(document.querySelectorAll("script")).map(s => ({
    id: s.id,
    src: s.src,
    textLength: s.textContent ? s.textContent.length : 0,
    textSample: s.textContent ? s.textContent.slice(0, 200) : ""
  }));

  const bodyText = document.body.innerText;
  
  // Check any anchors or links on page
  const links = Array.from(document.querySelectorAll("a")).map(a => ({
    href: a.href,
    text: a.innerText,
    className: a.className
  }));

  // Look for any global variables like __UNIVERSAL_DATA_FOR_REHYDRATION__ or SIGI_STATE
  let universalData = null;
  const uDataEl = document.getElementById("__UNIVERSAL_DATA_FOR_REHYDRATION__");
  if (uDataEl) {
    try {
      universalData = JSON.parse(uDataEl.textContent);
    } catch (e) {
      universalData = "PARSE_ERROR: " + e.message;
    }
  }

  let sigiState = null;
  const sigiEl = document.getElementById("SIGI_STATE");
  if (sigiEl) {
    try {
      sigiState = JSON.parse(sigiEl.textContent);
    } catch (e) {
      sigiState = "PARSE_ERROR: " + e.message;
    }
  }

  return {
    title: document.title,
    scripts,
    hasUniversalData: !!uDataEl,
    hasSigiState: !!sigiEl,
    linksCount: links.length,
    links: links.filter(l => l.href.includes("shop") || l.href.includes("product") || l.href.includes("pdp")),
    bodySnippet: bodyText.slice(0, 1000)
  };
});

console.log("PAGE INFO:", JSON.stringify({
  title: pageInfo.title,
  hasUniversalData: pageInfo.hasUniversalData,
  hasSigiState: pageInfo.hasSigiState,
  shopLinks: pageInfo.links
}, null, 2));

// Save full data if universal data exists
if (pageInfo.hasUniversalData) {
  const fullUniversal = await page.evaluate(() => {
    return document.getElementById("__UNIVERSAL_DATA_FOR_REHYDRATION__")?.textContent;
  });
  await writeFile("/Volumes/Data/gobi-social/scratch/universal_data.json", fullUniversal || "");
  console.log("Saved universal_data.json, size:", (fullUniversal || "").length);
}

await task.finish({ keep: [] });
