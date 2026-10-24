"""
Gobi 36 Multi-Angle Dataset Visual Catalog & Verification Reporter
Generates an HTML contact sheet and JSON manifest of the generated profile images.
"""

import os
import json
from pathlib import Path
from PIL import Image

DATASET_DIR = Path("/Volumes/Data/gobi-social/assets/datasets/koc/gobi_profile_36")
CONFIG_PATH = Path("/Volumes/Data/gobi-social/configs/koc_gobi_36_poses.json")
OUTPUT_HTML = Path("/Volumes/Data/gobi-social/shots/gobi_36_contact_sheet.html")
OUTPUT_MANIFEST = DATASET_DIR / "manifest.json"

def build_catalog():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        poses = json.load(f)

    manifest_entries = []
    html_cards = []

    # Include master anchor first
    anchor_file = DATASET_DIR / "00_MASTER_DNA_ANCHOR.jpg"
    if anchor_file.exists():
        im = Image.open(anchor_file)
        w, h = im.size
        size_kb = anchor_file.stat().st_size / 1024
        manifest_entries.append({
            "id": 0,
            "code": "00_MASTER_DNA_ANCHOR",
            "title": "MASTER IDENTITY DNA ANCHOR",
            "filename": anchor_file.name,
            "width": w,
            "height": h,
            "size_kb": round(size_kb, 1),
            "status": "COMPLETED"
        })
        html_cards.append(f"""
        <div class="card anchor">
            <div class="badge anchor-badge">MASTER ANCHOR (ID 00)</div>
            <img src="{anchor_file.as_uri()}" alt="Master Anchor" loading="lazy">
            <div class="info">
                <h3>00. Master Identity DNA</h3>
                <p><strong>Dims:</strong> {w}x{h} ({round(size_kb, 1)} KB)</p>
                <p class="tag">Primary Reference</p>
            </div>
        </div>
        """)

    files_in_dir = list(DATASET_DIR.glob("*.jpg"))
    for p in poses:
        pid = p["id"]
        code = p["code"]
        title = p["title"]
        prefix = f"gobi_angle_{pid:02d}_"
        matches = [f for f in files_in_dir if f.name.startswith(prefix)]
        target = matches[0] if matches else (DATASET_DIR / f"{code}.jpg")
        
        if target.exists() and target.stat().st_size > 100000:
            im = Image.open(target)
            w, h = im.size
            size_kb = target.stat().st_size / 1024
            manifest_entries.append({
                "id": pid,
                "code": code,
                "title": title,
                "filename": target.name,
                "width": w,
                "height": h,
                "size_kb": round(size_kb, 1),
                "status": "COMPLETED"
            })
            html_cards.append(f"""
            <div class="card completed">
                <div class="badge done-badge">Pose #{pid:02d} - COMPLETED</div>
                <img src="{target.as_uri()}" alt="{title}" loading="lazy">
                <div class="info">
                    <h3>#{pid:02d}. {title}</h3>
                    <p><strong>Dims:</strong> {w}x{h} ({round(size_kb / 1024, 2)} MB)</p>
                    <p class="prompt-text"><em>"{p['prompt'][:80]}..."</em></p>
                </div>
            </div>
            """)
        else:
            manifest_entries.append({
                "id": pid,
                "code": code,
                "title": title,
                "status": "PENDING"
            })
            html_cards.append(f"""
            <div class="card pending">
                <div class="badge pending-badge">Pose #{pid:02d} - QUEUED</div>
                <div class="placeholder">
                    <span>Rendering / Queued</span>
                </div>
                <div class="info">
                    <h3>#{pid:02d}. {title}</h3>
                    <p class="prompt-text"><em>"{p['prompt'][:80]}..."</em></p>
                </div>
            </div>
            """)

    with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, indent=2, ensure_ascii=False)

    completed_count = sum(1 for m in manifest_entries if m["status"] == "COMPLETED")
    total_count = len(poses) + 1  # includes anchor

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Gobi KOC - 36-Pose Master Profile Visual Sheet</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #0f1117;
            color: #e5e7eb;
            margin: 0;
            padding: 24px;
        }}
        header {{
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #374151;
        }}
        h1 {{ margin: 0 0 8px 0; color: #f9fafb; font-size: 26px; }}
        .stats {{ color: #10b981; font-size: 16px; font-weight: 600; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }}
        .card {{
            background: #1e222d;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #374151;
            display: flex;
            flex-direction: column;
            position: relative;
        }}
        .card.anchor {{ border: 2px solid #ec4899; }}
        .card.completed {{ border: 1px solid #10b981; }}
        .card.pending {{ opacity: 0.5; border-style: dashed; }}
        .badge {{
            position: absolute;
            top: 10px;
            left: 10px;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .anchor-badge {{ background: #ec4899; color: white; }}
        .done-badge {{ background: #10b981; color: white; }}
        .pending-badge {{ background: #6b7280; color: white; }}
        img {{
            width: 100%;
            height: 380px;
            object-fit: cover;
            background: #111827;
        }}
        .placeholder {{
            width: 100%;
            height: 380px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #1f2937;
            color: #9ca3af;
            font-size: 14px;
        }}
        .info {{
            padding: 14px;
            flex: 1;
        }}
        h3 {{ margin: 0 0 6px 0; font-size: 15px; color: #f3f4f6; }}
        p {{ margin: 0 0 4px 0; font-size: 12px; color: #9ca3af; }}
        .prompt-text {{ color: #d1d5db; font-size: 11px; line-height: 1.4; }}
        .tag {{ display: inline-block; padding: 2px 6px; background: #be185d; color: white; border-radius: 4px; font-weight: 600; font-size: 10px; }}
    </style>
</head>
<body>
    <header>
        <h1>🌟 Gobi KOC Master Profile Dataset (36 Angles & Poses)</h1>
        <div class="stats">Progress: {completed_count} / {total_count} Profiles Captured ({round(completed_count / total_count * 100)}%)</div>
    </header>
    <div class="grid">
        {"".join(html_cards)}
    </div>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Catalog updated: {completed_count}/{total_count} completed.")
    print(f"HTML Sheet: {OUTPUT_HTML}")
    print(f"Manifest: {OUTPUT_MANIFEST}")

if __name__ == "__main__":
    build_catalog()
