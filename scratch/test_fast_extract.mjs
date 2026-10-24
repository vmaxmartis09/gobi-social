const start = Date.now();
const task = await taskSpace("fast tiktok extract");
const page = task.page("p1");

const url = "https://www.tiktok.com/@beenalth/video/7678960622423330066";
await page.goto(url);

// Wait for script tag in DOM
for (let i = 0; i < 20; i++) {
  const ready = await page.evaluate(() => {
    const el = document.getElementById("__UNIVERSAL_DATA_FOR_REHYDRATION__");
    return el && el.textContent.length > 1000;
  });
  if (ready) break;
  await new Promise(r => setTimeout(r, 500));
}

const result = await page.evaluate(() => {
  const el = document.getElementById("__UNIVERSAL_DATA_FOR_REHYDRATION__");
  if (!el) return null;
  const data = JSON.parse(el.textContent);
  const item = data?.["__DEFAULT_SCOPE__"]?.["webapp.video-detail"]?.["itemInfo"]?.["itemStruct"];
  if (!item) return null;
  
  const anchors = item.anchors || [];
  const products = [];
  
  for (const a of anchors) {
    if (a.type === 35 || a.component_key === "anchor_shop") {
      try {
        const extra = JSON.parse(a.extra);
        for (const p of extra) {
          const inner = JSON.parse(p.extra || "{}");
          products.push({
            id: p.id,
            keyword: p.keyword,
            title: inner.title,
            seo_url: inner.seo_url,
            clean_pdp_url: `https://shop.tiktok.com/vn/pdp/${p.id}`,
            cover_url: inner.cover_url,
            seller_id: inner.seller_id,
            price: inner.price,
            currency: inner.currency,
            categories: inner.categories
          });
        }
      } catch (err) {}
    }
  }
  
  return {
    videoId: item.id,
    videoDesc: item.desc,
    author: item.author?.uniqueId,
    products
  };
});

console.log("EXEC_TIME_MS:", Date.now() - start);
console.log("RESULT:", JSON.stringify(result, null, 2));

await task.finish({ keep: [] });
