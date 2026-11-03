"""Điểm duy nhất phân giải đường dẫn repo / data source / project của Gobi Social.

Quy ước:
- REPO_ROOT:  thư mục gốc repo (env GOBI_ROOT, mặc định tự dò từ vị trí file này).
- DATA_DIR:   data source (env GOBI_DATA_DIR, mặc định REPO_ROOT/data) — có thể nằm ngoài repo.
- Project:    mỗi project có data riêng tại DATA_DIR/projects/<tên>.
              Chọn project theo thứ tự: tham số name > env GOBI_PROJECT > file DATA_DIR/projects/.active > "gobi".
- Dữ liệu dùng chung nhiều project (model, giọng, template) nằm ở DATA_DIR/_shared.
"""
import json
import os
from pathlib import Path
from typing import Optional

DEFAULT_PROJECT = "gobi"

# Cấu trúc chuẩn của một project: đường dẫn tương đối -> mô tả (dùng sinh README).
PROJECT_LAYOUT = {
    "characters/profiles": "Hồ sơ nhân vật (profile.json: persona, giọng, phong cách).",
    "characters/dna": "Ảnh neo gốc & ma trận góc quay giữ nhân vật nhất quán.",
    "characters/datasets": "Dữ liệu ảnh cắt lát phục vụ Face-ID / LoRA.",
    "library/videos": "Video gốc của người dùng.",
    "library/images": "Ảnh gốc của người dùng.",
    "library/audio": "Audio / nhạc nền của người dùng.",
    "library/samples": "Video/ảnh tham khảo cần phân tích hoặc mimic.",
    "library/texts": "Kịch bản, ghi chú dạng văn bản.",
    "products/catalog": "Kho sản phẩm (mỗi sản phẩm một thư mục).",
    "products/config": "Cấu hình danh mục sản phẩm.",
    "accounts": "Tài khoản mạng xã hội của project (không commit secret).",
    "social/tiktok": "Session, lịch đăng, số liệu TikTok.",
    "social/youtube": "Session, lịch đăng, số liệu YouTube.",
    "social/instagram": "Session, lịch đăng, số liệu Instagram.",
    "social/x": "Session, lịch đăng, số liệu X (Twitter).",
    "knowledge": "Tri thức niche: policy, từ điển cấm, big data xu hướng, trí nhớ tự học.",
    "analytics": "Báo cáo phân tích sau xử lý.",
    "raw": "Dữ liệu cào thô.",
    "configs/prompts": "Prompt template của project.",
    "configs/workflows": "Cấu hình workflow của project.",
    "output": "Sản phẩm render (video, audio, log).",
    "shots": "Ảnh chụp màn hình làm bằng chứng.",
}


def _find_repo_root() -> Path:
    env = os.environ.get("GOBI_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    for parent in Path(__file__).resolve().parents:
        if (parent / "ai" / "AGENTS.md").exists():
            return parent
    raise RuntimeError("Không tìm thấy gốc repo Gobi; hãy đặt biến môi trường GOBI_ROOT.")


REPO_ROOT = _find_repo_root()
DATA_DIR = Path(os.environ.get("GOBI_DATA_DIR") or REPO_ROOT / "data").expanduser().resolve()
PROJECTS_DIR = DATA_DIR / "projects"
SHARED_DIR = DATA_DIR / "_shared"


def active_project() -> str:
    env = os.environ.get("GOBI_PROJECT")
    if env:
        return env
    marker = PROJECTS_DIR / ".active"
    if marker.is_file():
        name = marker.read_text(encoding="utf-8").strip()
        if name:
            return name
    return DEFAULT_PROJECT


def set_active_project(name: str) -> None:
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    (PROJECTS_DIR / ".active").write_text(name + "\n", encoding="utf-8")


def list_projects() -> list:
    if not PROJECTS_DIR.is_dir():
        return []
    return sorted(p.name for p in PROJECTS_DIR.iterdir() if p.is_dir() and not p.name.startswith(("_", ".")))


def project_dir(name: Optional[str] = None) -> Path:
    return PROJECTS_DIR / (name or active_project())


def project_path(*parts: str, project: Optional[str] = None) -> Path:
    return project_dir(project).joinpath(*parts)


def shared_path(*parts: str) -> Path:
    return SHARED_DIR.joinpath(*parts)


def _readme(title: str, body: str) -> str:
    return f"# {title}\n\n{body}\n\n> Nội dung thật của thư mục này được gitignore; chỉ README này nằm trong git.\n"


def scaffold_project(name: str, root: Optional[Path] = None) -> Path:
    """Tạo khung thư mục + README + project.json cho một project (không ghi đè file có sẵn)."""
    base = (root or PROJECTS_DIR) / name
    base.mkdir(parents=True, exist_ok=True)
    meta = base / "project.json"
    if not meta.exists():
        meta.write_text(json.dumps({"name": name, "description": "", "platforms": ["tiktok", "youtube", "instagram", "x"]},
                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    top = {}
    for rel, desc in PROJECT_LAYOUT.items():
        d = base / rel
        d.mkdir(parents=True, exist_ok=True)
        top.setdefault(rel.split("/")[0], []).append((rel, desc))
        readme = d / "README.md"
        if not readme.exists():
            readme.write_text(_readme(rel, desc), encoding="utf-8")
    body = "Cấu trúc project:\n\n" + "\n".join(f"- `{rel}/` — {desc}" for items in top.values() for rel, desc in items)
    readme = base / "README.md"
    if not readme.exists():
        readme.write_text(_readme(f"Project `{name}`", body), encoding="utf-8")
    return base


def scaffold_shared(root: Optional[Path] = None) -> Path:
    base = root or SHARED_DIR
    items = {"models": "Trọng số model AI cục bộ (tải lại theo docs).",
             "voices/vault": "Kho giọng mẫu đã lọc tạp âm, dùng chung các project (cloned/ và profiles/ là alias symlink).",
             "voices/samples": "Giọng mẫu thô.", "templates": "Intro/outro, font, nhạc nền, template dùng chung."}
    for rel, desc in items.items():
        d = base / rel
        d.mkdir(parents=True, exist_ok=True)
        if not (d / "README.md").exists():
            (d / "README.md").write_text(_readme(f"_shared/{rel}", desc), encoding="utf-8")
    return base
