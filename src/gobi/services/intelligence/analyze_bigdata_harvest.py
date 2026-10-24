import json
import re
from collections import Counter

def analyze_harvest(json_path="configs/koc_fashion_bigdata_harvest.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        videos = json.load(f)

    total_videos = len(videos)
    if total_videos == 0:
        print("No videos found.")
        return

    # Sort by views
    sorted_videos = sorted(videos, key=lambda x: x.get("views", 0), reverse=True)

    views = [v.get("views", 0) for v in videos]
    likes = [v.get("likes", 0) for v in videos]
    shares = [v.get("shares", 0) for v in videos]
    saves = [v.get("saves", 0) for v in videos]
    comments = [v.get("comments", 0) for v in videos]

    total_views = sum(views)
    avg_views = total_views // total_videos
    max_views = max(views)

    # Engagement Rate: (Likes + Comments + Shares + Saves) / Views * 100
    engagement_rates = []
    for v in videos:
        view_cnt = v.get("views", 0)
        if view_cnt > 0:
            eng = (v.get("likes", 0) + v.get("comments", 0) + v.get("shares", 0) + v.get("saves", 0)) / view_cnt * 100
            engagement_rates.append(eng)

    avg_engagement = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0

    # Top Hashtags
    hashtag_counter = Counter()
    for v in videos:
        desc = v.get("desc", "")
        tags = re.findall(r"#\w+", desc.lower())
        hashtag_counter.update(tags)

    # Top Words in Titles/Descriptions
    word_counter = Counter()
    stopwords = {"và", "là", "cho", "của", "có", "trong", "được", "với", "các", "này", "khi", "để", "thì", "mà", "ở", "em", "nè", "nha", "ạ", "luôn", "quá", "ơi", "video", "tiktok", "fyp", "xuhuong"}
    for v in videos:
        desc = v.get("desc", "")
        # Remove hashtags and links
        cleaned_text = re.sub(r"#\w+", "", desc)
        cleaned_text = re.sub(r"https?://\S+", "", cleaned_text)
        words = re.findall(r"\b\w{2,}\b", cleaned_text.lower())
        for w in words:
            if w not in stopwords and not w.isdigit():
                word_counter[w] += 1

    # Product category extraction
    category_counts = {
        "Váy / Đầm (Dress)": 0,
        "Áo Cardigan / Dệt kim (Knitwear)": 0,
        "Quần suông / Quần hack dáng (Pants/Jeans)": 0,
        "Chân váy (Skirts)": 0,
        "Set đồ phối sẵn (Coordinate Set)": 0,
        "Áo thun / Áo baby tee / Body": 0
    }

    for v in videos:
        desc = v.get("desc", "").lower()
        if any(k in desc for k in ["đầm", "váy hoa", "váy suông", "dress"]):
            category_counts["Váy / Đầm (Dress)"] += 1
        if any(k in desc for k in ["len", "cardigan", "dệt kim", "áo khoác"]):
            category_counts["Áo Cardigan / Dệt kim (Knitwear)"] += 1
        if any(k in desc for k in ["quần ống suông", "quần tây", "quần jean", "quần suông", "hack dáng", "cạp cao", "quần short"]):
            category_counts["Quần suông / Quần hack dáng (Pants/Jeans)"] += 1
        if any(k in desc for k in ["chân váy", "chân váy chữ a", "chân váy xếp ly"]):
            category_counts["Chân váy (Skirts)"] += 1
        if any(k in desc for k in ["set", "phối đồ", "outfit", "set đồ"]):
            category_counts["Set đồ phối sẵn (Coordinate Set)"] += 1
        if any(k in desc for k in ["áo thun", "baby tee", "ôm body", "áo croptop", "áo kiểu"]):
            category_counts["Áo thun / Áo baby tee / Body"] += 1

    # Top 10 viral videos
    top_10 = sorted_videos[:10]

    report = {
        "total_analyzed": total_videos,
        "total_views": total_views,
        "avg_views": avg_views,
        "max_views": max_views,
        "avg_engagement_rate": round(avg_engagement, 2),
        "top_hashtags": hashtag_counter.most_common(15),
        "top_keywords": word_counter.most_common(20),
        "category_distribution": category_counts,
        "top_10_videos": [
            {
                "rank": i + 1,
                "id": v.get("id"),
                "author": v.get("author"),
                "views": v.get("views"),
                "likes": v.get("likes"),
                "shares": v.get("shares"),
                "saves": v.get("saves"),
                "comments": v.get("comments"),
                "engagement_rate": round(((v.get("likes", 0) + v.get("comments", 0) + v.get("shares", 0) + v.get("saves", 0)) / max(v.get("views", 1), 1)) * 100, 2),
                "desc": v.get("desc"),
                "music": v.get("music"),
                "url": v.get("video_url")
            }
            for i, v in enumerate(top_10)
        ]
    }

    output_path = "configs/koc_fashion_bigdata_analytics.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Analysis saved to {output_path}")
    print(f"Total Views: {total_views:,} | Avg Views: {avg_views:,} | Max Views: {max_views:,}")
    print("\n--- TOP 10 VIRAL VIDEOS ---")
    for item in report["top_10_videos"]:
        print(f"#{item['rank']} | {item['views']:,} views | {item['likes']:,} likes | Eng: {item['engagement_rate']}% | @{item['author']} | {item['desc'][:70]}...")

    print("\n--- TOP 10 HASHTAGS ---")
    for tag, cnt in report["top_hashtags"][:10]:
        print(f"{tag}: {cnt} videos")

    print("\n--- CATEGORY DISTRIBUTION ---")
    for cat, cnt in category_counts.items():
        print(f"{cat}: {cnt} videos")

if __name__ == "__main__":
    analyze_harvest()
