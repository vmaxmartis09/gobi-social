"""Seed script for populating the product warehouse."""

import os
import json
import shutil
from pathlib import Path
from gobi.services.product_manager import ProductManager
from gobi.domain.product_models import (
    ProductItem,
    ProductCategory,
    ProductStatus,
    ProductPricing,
    ProductSpecs,
    ProductVideoProduction,
    ProductSEOMetadata,
)

manager = ProductManager()

products = [
    ProductItem(
        product_code="SP-BJ-001",
        product_name="Áo Thun Giấy Tay Dài Cổ Henley Byjane Form Suông",
        category=ProductCategory.AO_THUN,
        pricing=ProductPricing(
            price_vnd=89000,
            original_price_vnd=149000,
            commission_rate_percent=22.0,
            commission_per_order_vnd=19580,
        ),
        specs=ProductSpecs(
            material="Thun giấy dệt xước (Slub Knit), mỏng nhẹ thoáng khí, sợi dệt đôi không nhăn",
            colors=["Trắng kem (Off-white)", "Đen basic", "Xám tiêu", "Be sữa"],
            sizes=["Freesize (40kg - 58kg)"],
            origin_shop="Byjane Official Store",
            usp_features=[
                "Cổ henley cài cúc linh hoạt, mở nút khoe xương quai xanh thanh thoát",
                "Form suông rủ tự nhiên che khuyết điểm bắp tay và eo",
                "Chất thun giấy mỏng nhẹ xuyên thấu tinh tế, phối bra màu nude sang trọng"
            ],
        ),
        production=ProductVideoProduction(
            status=ProductStatus.DA_DANG_VIDEO,
            assigned_koc="@gobiboutique",
            winning_format="Tactile Proof & Save Magnet (1 Item 3 Outfits)",
            vmax_panels=["Panel 03 (Cận mặt)", "Panel 14 (Cổ áo)", "Panel 25 (Thớ vải)", "Panel 26 (Bước đi)", "Panel 36 (Xoay người)"],
            benchmark_video_url="https://www.tiktok.com/@beenalth/video/7678960622423330066",
            benchmark_views=378500,
            published_video_url="https://www.tiktok.com/@gobiboutique/video/7678960622423330066",
            published_at="2026-10-20 14:50:00",
        ),
        seo=ProductSEOMetadata(
            primary_keywords=["áo thun giấy tay dài", "áo thun byjane", "áo thun giấy form rộng"],
            secondary_keywords=["áo thun mỏng mùa thu", "áo thun cổ henley", "phối đồ áo thun giấy", "áo thun mặc không lộ nội y"],
            search_intents=["cách phối áo thun giấy không lộ", "review áo thun giấy tay dài byjane", "áo thun giấy form rộng nữ"],
            hashtags=["#aothungiay", "#aothunbyjane", "#aothuntaydai", "#phoidonangtho", "#gobiboutique", "#tiktokshopaffiliate"],
            caption_template="Cách diện áo thun giấy tay dài Byjane vừa sang vừa hack dáng cho nàng thơ 🌷 Mấy bà thích Look 1 quần suông hay Look 2 chân váy hơn? Ghé góc trái giỏ hàng nha!"
        ),
    ),
    ProductItem(
        product_code="SP-QT-002",
        product_name="Quần Tây Ống Suông Lưng Cao Vải Tuyết Mưa Hack Dáng 1m7",
        category=ProductCategory.QUAN_TAY,
        pricing=ProductPricing(
            price_vnd=139000,
            original_price_vnd=219000,
            commission_rate_percent=20.0,
            commission_per_order_vnd=27800,
        ),
        specs=ProductSpecs(
            material="Vải tuyết mưa Vitex loại 1, đanh mịn, không xù lông, không nhăn khi ngồi",
            colors=["Đen tuyền", "Be kem Hàn Quốc", "Nâu tây", "Xám chì"],
            sizes=["S (40-46kg)", "M (47-52kg)", "L (53-58kg)", "XL (59-64kg)"],
            origin_shop="Linh Beauty Fashion",
            usp_features=[
                "Cạp cao trên rốn siết phẳng bụng dưới tức thì",
                "Ống suông thẳng đứng rủ chạm gót giày kéo dài tỷ lệ chân",
                "Khóa kéo kim loại YKK trơn tru kèm 2 túi xéo sâu đựng điện thoại"
            ],
        ),
        production=ProductVideoProduction(
            status=ProductStatus.DA_DANG_VIDEO,
            assigned_koc="@gobiboutique",
            winning_format="Body Hack Visuals (Cạp cao giấu bụng + Kéo chân 1m7)",
            vmax_panels=["Panel 01 (Toàn thân)", "Panel 14 (Trung cảnh eo)", "Panel 26 (Bước đi hack dáng)"],
            benchmark_video_url="https://www.tiktok.com/@nhat.linh.beauty/video/7589815833430330645",
            benchmark_views=2600000,
            published_video_url="https://www.tiktok.com/@gobiboutique/video/7697472862633921812",
            published_at="2026-10-18 20:00:00",
        ),
        seo=ProductSEOMetadata(
            primary_keywords=["quần tây ống suông", "quần tây cạp cao hack dáng", "quần tây nữ đi học"],
            secondary_keywords=["quần vải tuyết mưa", "quần ống suông che bụng dưới", "quần tây công sở nữ"],
            search_intents=["quần tây ống suông hack chân", "quần tây nữ lưng cao đi làm", "quần tây vải tuyết mưa không nhăn"],
            hashtags=["#quantayongsuong", "#quantaynu", "#quantaycapcao", "#phoidohackdang", "#gobiboutique", "#tiktokshopaffiliate"],
            caption_template="Chân ngắn, đùi to né gấp chiếc quần tây ống suông này kẻo bị nghi kéo chân! Vải tuyết mưa phẳng lì không nhăn, deal hời ở góc trái nha các nàng!"
        ),
    ),
    ProductItem(
        product_code="SP-QJ-003",
        product_name="Quần Jean Nữ Ống Rộng Cạp Cao Vintage Retro Hàn Quốc",
        category=ProductCategory.QUAN_JEAN,
        pricing=ProductPricing(
            price_vnd=159000,
            original_price_vnd=250000,
            commission_rate_percent=18.0,
            commission_per_order_vnd=28620,
        ),
        specs=ProductSpecs(
            material="Denim cotton 100% dày dặn 12oz, wash màu vintage không phai",
            colors=["Xanh retro nhạt", "Xanh đậm vintage", "Xám khói wash"],
            sizes=["S", "M", "L"],
            origin_shop="Hin Thanh Denim Studio",
            usp_features=[
                "Form đứng tôn mông, không bị xệ đáy khi ngồi",
                "Độ dài tiêu chuẩn che trọn giày sneaker/cao gót",
                "Màu wash cổ điển dễ phối mọi kiểu áo thun, croptop"
            ],
        ),
        production=ProductVideoProduction(
            status=ProductStatus.DANG_LAM,
            assigned_koc="@gobi.aries",
            winning_format="Shocking Comparison (Quần thường vs Quần jean ống rộng)",
            vmax_panels=["Panel 01 (Toàn thân)", "Panel 22 (Ngang hông)", "Panel 36 (Xoay người)"],
            benchmark_video_url="https://www.tiktok.com/@hinthanh806/video/7679350378198060296",
            benchmark_views=1000000,
            published_video_url=None,
            published_at=None,
        ),
        seo=ProductSEOMetadata(
            primary_keywords=["quần jean ống rộng", "quần jean nữ cạp cao", "quần bò ống suông"],
            secondary_keywords=["quần jean hack dáng", "quần jean vintage hàn quốc", "jean nữ gen z"],
            search_intents=["quần jean ống rộng nữ cạp cao", "phối đồ với quần jean ống suông", "quần jean nữ tôn dáng"],
            hashtags=["#quanjeanongrong", "#jeancapcao", "#jeanvintage", "#streetstyle", "#gobiaries"],
            caption_template="1 chiếc quần jean cạp cao cứu cánh cho mọi cô nàng chân cong, đùi to! Mix với croptop là 10 điểm không có nhưng ✨ Săn deal tại giỏ hàng nhé!"
        ),
    ),
    ProductItem(
        product_code="SP-QS-004",
        product_name="Quần Short Nắp Túi Cạp Trễ Tôn Dáng Y2K Năng Động",
        category=ProductCategory.QUAN_SHORT,
        pricing=ProductPricing(
            price_vnd=99000,
            original_price_vnd=160000,
            commission_rate_percent=20.0,
            commission_per_order_vnd=19800,
        ),
        specs=ProductSpecs(
            material="Kaki mềm co giãn nhẹ, giữ form nắp túi hộp sắc sảo",
            colors=["Xanh nhạt pastel", "Xám khói", "Đen basic", "Trắng kem"],
            sizes=["S", "M", "L"],
            origin_shop="Lumy Store Vietnam",
            usp_features=[
                "Thiết kế 2 nắp túi hộp tạo điểm nhấn vòng hông quyến rũ",
                "Gấu quần may cuốn mép tinh xảo, không sợ lộ khi vận động",
                "Phong cách Y2K trẻ trung, năng động"
            ],
        ),
        production=ProductVideoProduction(
            status=ProductStatus.CHUA_LAM,
            assigned_koc="@gobi.taurus",
            winning_format="Fast-Cut Beat Syncing (Cắt cảnh 1.5s theo nhịp nhạc)",
            vmax_panels=["Panel 01 (Toàn thân)", "Panel 22 (Ngang hông)", "Panel 36 (Xoay người)"],
            benchmark_video_url="https://www.tiktok.com/@lumystore6/video/7690007359501978900",
            benchmark_views=488900,
            published_video_url=None,
            published_at=None,
        ),
        seo=ProductSEOMetadata(
            primary_keywords=["quần short nữ", "quần short nắp túi", "quần short y2k"],
            secondary_keywords=["short nữ cạp trễ", "quần đùi nữ tôn dáng", "short kaki nữ"],
            search_intents=["quần short túi hộp nữ", "quần short hack chân dài", "short y2k phối đồ"],
            hashtags=["#quanshortnu", "#shorty2k", "#shortnaptui", "#outfitmuahe", "#gobitaurus"],
            caption_template="Chiếc quần short hack chân dài mà đùi to hay eo bánh mì diện vào cũng auto thon gọn! Mê style Y2K thì rinh ngay ở góc trái giỏ hàng nha!"
        ),
    ),
    ProductItem(
        product_code="SP-CD-005",
        product_name="Áo Khoác Cardigan Len Mỏng Dáng Rộng Nàng Thơ SuChang",
        category=ProductCategory.AO_KHOAC,
        pricing=ProductPricing(
            price_vnd=129000,
            original_price_vnd=199000,
            commission_rate_percent=20.0,
            commission_per_order_vnd=25800,
        ),
        specs=ProductSpecs(
            material="Len dệt kim mỏng nhẹ, mềm mại như mây, sợi bông tự nhiên không xơ cứng",
            colors=["Be sữa", "Nâu nhạt", "Hồng pastel", "Xanh bơ"],
            sizes=["Freesize (dưới 60kg)"],
            origin_shop="SuChang Studio",
            usp_features=[
                "Dệt lỏng tay tạo độ bay bổng nhu mì",
                "Cúc áo vỏ sò ánh xà cừ cổ điển",
                "Đa năng: khoác ngoài váy 2 dây hoặc cài cúc mặc đơn"
            ],
        ),
        production=ProductVideoProduction(
            status=ProductStatus.DANG_LAM,
            assigned_koc="@gobiboutique",
            winning_format="Daily Vlog KOC & ASMR Fabric (Âm thanh sột soạt, chạm thớ len)",
            vmax_panels=["Panel 03 (Cận mặt)", "Panel 25 (Thớ len)", "Panel 26 (Toàn thân)", "Panel 02 (Chỉ giỏ hàng)"],
            benchmark_video_url="https://www.tiktok.com/@suchangvn/video/7680123456789012345",
            benchmark_views=368674,
            published_video_url=None,
            published_at=None,
        ),
        seo=ProductSEOMetadata(
            primary_keywords=["áo cardigan len mỏng", "áo khoác len nàng thơ", "cardigan dáng rộng"],
            secondary_keywords=["áo khoác đi học nhẹ nhàng", "cardigan hàn quốc", "phối cardigan với váy 2 dây"],
            search_intents=["áo cardigan len mỏng mặc mùa thu", "áo cardigan phong cách nàng thơ", "cardigan hàn quốc giá học sinh"],
            hashtags=["#cardigannangtho", "#aokhoaclen", "#cardiganhanquoc", "#gobiboutique", "#thoitrangnangtho"],
            caption_template="Gợi ý chiếc cardigan len mỏng chuẩn vibe nàng thơ đi cafe cuối tuần 🌷 Tone be sữa nhẹ tênh, chất len êm ru không ngứa. Nhấp giỏ hàng săn deal nhé!"
        ),
    ),
    ProductItem(
        product_code="SP-VB-006",
        product_name="Váy Body Tay Dài Cổ Vuông Tôn Dáng Phối Ren LAVENDER",
        category=ProductCategory.VAY_DAM,
        pricing=ProductPricing(
            price_vnd=249000,
            original_price_vnd=380000,
            commission_rate_percent=18.0,
            commission_per_order_vnd=44820,
        ),
        specs=ProductSpecs(
            material="Thun tăm gân cao cấp co giãn 4 chiều, viền ren mi mềm mại",
            colors=["Đen quyến rũ", "Trắng tiểu thư", "Đỏ rượu vang"],
            sizes=["S (40-47kg)", "M (48-54kg)"],
            origin_shop="LAVENDER Official Store",
            usp_features=[
                "Cổ vuông sâu khoe trọn xương quai xanh thanh tú",
                "Thiết kế rúm nhẹ 2 bên hông giấu bụng cực khéo",
                "Chất vải đầm tay, dày dặn, không lộ viền nội y"
            ],
        ),
        production=ProductVideoProduction(
            status=ProductStatus.CHUA_LAM,
            assigned_koc="@thienthoaireview",
            winning_format="POV (Point of View: Con trai chấm điểm đồ bạn gái mặc đi date)",
            vmax_panels=["Panel 01 (Toàn thân)", "Panel 03 (Cận mặt)", "Panel 36 (Xoay dáng)"],
            benchmark_video_url=None,
            benchmark_views=None,
            published_video_url=None,
            published_at=None,
        ),
        seo=ProductSEOMetadata(
            primary_keywords=["váy body tay dài", "đầm ôm cổ vuông", "váy body tôn dáng"],
            secondary_keywords=["váy đi date sang chảnh", "đầm body phối ren", "váy ôm body hack eo"],
            search_intents=["váy body cổ vuông tay dài", "đầm ôm đi tiệc tôn dáng", "váy body đẹp giá rẻ"],
            hashtags=["#vaybody", "#damomcovuong", "#outfitdidate", "#thienthoaireview", "#tiktokshopaffiliate"],
            caption_template="Con trai chấm điểm chiếc đầm cháy hàng nhất TikTok Shop tuần qua! Form ôm tôn dáng 10 điểm đi date chàng nào cũng mê. Xem chi tiết ở góc trái nha!"
        ),
    ),
    ProductItem(
        product_code="SP-TX-007",
        product_name="Túi Xách Nữ Kẹp Nách Da Mềm Đính Dây Xích Bạc MOLLIX",
        category=ProductCategory.TUI_XACH,
        pricing=ProductPricing(
            price_vnd=189000,
            original_price_vnd=299000,
            commission_rate_percent=20.0,
            commission_per_order_vnd=37800,
        ),
        specs=ProductSpecs(
            material="Da PU cao cấp chống xước, bề mặt lì mềm mịn, xích bạc mạ tĩnh điện chống gỉ",
            colors=["Đen sang trọng", "Trắng kem", "Bạc ánh kim metallic"],
            sizes=["24cm x 14cm x 7cm (vừa iPhone Pro Max + đồ skincare/son phấn)"],
            origin_shop="MOLLIX Studio",
            usp_features=[
                "Thiết kế 2 quai tháo rời: vừa kẹp nách sang chảnh vừa đeo chéo cá tính",
                "Ngăn khóa zip an toàn bên trong kèm lót vải nhung êm ái",
                "Phụ kiện xích bạc tạo điểm nhấn bắt mắt khi chụp ảnh dạo phố"
            ],
        ),
        production=ProductVideoProduction(
            status=ProductStatus.CHUA_LAM,
            assigned_koc="@thienthoaireview",
            winning_format="Unboxing & What's In My Bag (Đựng cả thế giới)",
            vmax_panels=["Panel 22 (Cận tay cầm túi)", "Panel 25 (Chất da & xích)", "Panel 01 (Lên đồ dạo phố)"],
            benchmark_video_url=None,
            benchmark_views=None,
            published_video_url=None,
            published_at=None,
        ),
        seo=ProductSEOMetadata(
            primary_keywords=["túi kẹp nách nữ", "túi xách nữ da mềm", "túi xách dây xích"],
            secondary_keywords=["túi xách nữ đi tiệc", "túi kẹp nách sang chảnh", "túi xách nữ giá học sinh"],
            search_intents=["túi kẹp nách nữ da mềm giá rẻ", "túi xách nữ đựng vừa điện thoại", "túi xách phối đồ nàng thơ"],
            hashtags=["#tuikepnach", "#tuixachnu", "#tuixachdamem", "#phukienthoitrang", "#thienthoaireview"],
            caption_template="Chiếc túi giá chưa bằng 3 ly trà sữa mà đựng được cả thế giới của con gái! Da mềm êm ru, xích bạc sáng bóng. Rinh ngay tại giỏ hàng TikTok Shop nha!"
        ),
    ),
]

for p in products:
    folder = manager.save_product(p)
    print(f"[+] Saved {p.product_code}: {p.product_name} -> {folder}")

    # Copy cover for SP-BJ-001 if available
    if p.product_code == "SP-BJ-001" and os.path.exists("shots/beenalth_cover.jpg"):
        target_cover = folder.parent / "assets" / "cover.jpg"
        shutil.copy("shots/beenalth_cover.jpg", target_cover)
        print(f"  -> Copied cover image to {target_cover}")

    # Write detailed koc_script.md for each product
    script_file = folder.parent / "koc_script.md"
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(f"""# KỊCH BẢN KOC AI: {p.product_name} ({p.product_code})
* **KOC Phụ Trách:** {p.production.assigned_koc}
* **Trạng Thái:** {p.production.status.value.upper()}
* **Giá Niêm Yết:** {p.pricing.price_vnd:,}đ | **Hoa Hồng:** {p.pricing.commission_rate_percent}% ({p.pricing.commission_per_order_vnd:,}đ/đơn)
* **Định Dạng:** {p.production.winning_format}

---

## 1. HOOK 3 GIÂY ĐẦU (00:00 - 00:03)
* **Góc máy:** {p.production.vmax_panels[0] if p.production.vmax_panels else "Panel 03"}
* **Text Hook Safe Zone:** "{p.seo.primary_keywords[0].upper()} - XEM NGAY KẺO HỐ!"
* **Lời thoại:** "{p.seo.caption_template.split('!')[0]}!"

## 2. SOI CHI TIẾT & CHẤT LIỆU (00:03 - 00:15)
* **Chất liệu:** {p.specs.material}
* **USP 1:** {p.specs.usp_features[0] if p.specs.usp_features else ""}
* **USP 2:** {p.specs.usp_features[1] if len(p.specs.usp_features) > 1 else ""}

## 3. LÊN DÁNG & MIX MATCH (00:15 - 00:27)
* **Bảng màu:** {', '.join(p.specs.colors)}
* **Kích cỡ:** {', '.join(p.specs.sizes)}
* **Phối đồ:** {p.seo.secondary_keywords[0]}

## 4. KÊU GỌI HÀNH ĐỘNG (00:27 - 00:35)
* **CTA:** Nhấp vào giỏ hàng góc trái màn hình để săn deal hời!
""")

    # Write seo_metadata.json
    seo_file = folder.parent / "seo_metadata.json"
    with open(seo_file, "w", encoding="utf-8") as f:
        json.dump(p.seo.model_dump(), f, ensure_ascii=False, indent=2)

manifest = manager.rebuild_warehouse_index()
print(f"\n[OK] Warehouse Index Rebuilt Successfully!")
print(f"Total Products: {manifest.total_products}")
print(f"Status Summary: {manifest.status_summary}")
print(f"KOC Assignments: {manifest.koc_assignments_summary}")
