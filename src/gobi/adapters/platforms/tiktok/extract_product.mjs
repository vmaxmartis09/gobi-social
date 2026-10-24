import { readFile, writeFile } from "node:fs/promises";

async function main() {
  const configPath = process.argv[2] || "/tmp/gobi_tiktok_req.json";
  let inputUrl = "";
  try {
    const raw = await readFile(configPath, "utf8");
    const parsed = JSON.parse(raw);
    inputUrl = parsed.url;
  } catch (err) {
    console.error(JSON.stringify({ error: `Cannot read config file: ${err.message}` }));
    process.exit(1);
  }

  if (!inputUrl) {
    console.error(JSON.stringify({ error: "Missing TikTok video URL in config." }));
    process.exit(1);
  }

  const task = await taskSpace("tiktok product extractor");
  const page = task.page("p1");

  try {
    await page.goto(inputUrl);

    // Wait up to 10s for __UNIVERSAL_DATA_FOR_REHYDRATION__ script
    let foundScript = false;
    for (let i = 0; i < 20; i++) {
      foundScript = await page.evaluate(() => {
        const el = document.getElementById("__UNIVERSAL_DATA_FOR_REHYDRATION__");
        return el && el.textContent.length > 500;
      });
      if (foundScript) break;
      await new Promise(r => setTimeout(r, 500));
    }

    if (!foundScript) {
      console.log(JSON.stringify({
        success: false,
        error: "Không tìm thấy dữ liệu trang TikTok hoặc trang bị chặn xác thực."
      }));
      await task.finish({ keep: [] });
      return;
    }

    const result = await page.evaluate(() => {
      const el = document.getElementById("__UNIVERSAL_DATA_FOR_REHYDRATION__");
      if (!el) return { success: false, error: "Missing script data" };
      
      let data = null;
      try {
        data = JSON.parse(el.textContent);
      } catch (e) {
        return { success: false, error: `JSON parse error: ${e.message}` };
      }

      const scope = data?.["__DEFAULT_SCOPE__"] || {};
      const videoDetail = scope["webapp.video-detail"] || {};
      const item = videoDetail?.["itemInfo"]?.["itemStruct"];

      if (!item) {
        return {
          success: false,
          error: "Không tìm thấy thông tin video trong metadata (Video có thể ở chế độ riêng tư hoặc đã bị xóa)."
        };
      }

      const anchors = item.anchors || [];
      const products = [];

      for (const a of anchors) {
        // TikTok Shop anchors usually have type 35 or component_key == "anchor_shop"
        if (a.type === 35 || a.component_key === "anchor_shop") {
          try {
            const extra = JSON.parse(a.extra || "[]");
            for (const p of extra) {
              const inner = JSON.parse(p.extra || "{}");
              
              // Extract chain_key if available in schema
              let chainKey = "";
              let schema = inner.schema || "";
              if (schema) {
                try {
                  const urlObj = new URL(schema.replace("aweme://", "http://localhost/"));
                  const visitStr = urlObj.searchParams.get("visitReportParams");
                  if (visitStr) {
                    const visit = JSON.parse(visitStr);
                    chainKey = visit.chain_key || "";
                  }
                } catch (e) {}
              }

              const productId = String(p.id || inner.product_id || "");
              const cleanPdp = productId ? `https://shop.tiktok.com/vn/pdp/${productId}` : "";
              const seoUrl = inner.seo_url || (cleanPdp ? `${cleanPdp}?source=anchor` : "");
              let affiliatePdp = cleanPdp;
              if (cleanPdp && chainKey) {
                affiliatePdp = `${cleanPdp}?chain_key=${encodeURIComponent(chainKey)}&source=anchor`;
              }

              products.push({
                product_id: productId,
                keyword: p.keyword || inner.elastic_title || "",
                title: inner.title || "",
                pdp_url: cleanPdp,
                affiliate_pdp_url: affiliatePdp,
                seo_url: seoUrl,
                cover_url: inner.cover_url || (inner.img_url && inner.img_url[0]) || "",
                seller_id: inner.seller_id ? String(inner.seller_id) : "",
                price: inner.price || 0,
                currency: inner.currency || "VND",
                chain_key: chainKey,
                categories: inner.categories || []
              });
            }
          } catch (err) {}
        }
      }

      return {
        success: true,
        video_id: item.id,
        author: item.author?.uniqueId || "",
        nickname: item.author?.nickname || "",
        desc: item.desc || "",
        has_shop_anchor: products.length > 0,
        total_products: products.length,
        products
      };
    });

    console.log(JSON.stringify(result));
  } catch (err) {
    console.log(JSON.stringify({ success: false, error: err.message }));
  } finally {
    await task.finish({ keep: [] });
  }
}

await main();
