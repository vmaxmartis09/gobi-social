#!/usr/bin/env python3
"""
scripts/clean_workspace.py
Dọn dẹp cache, temporary media rác, screenshot debug và file rác macOS theo chuẩn ARCHITECTURE.md.

Sử dụng:
    python scripts/clean_workspace.py           # Dọn dẹp an toàn
    python scripts/clean_workspace.py --dry-run # Xem trước các file sẽ bị xoá
"""

import os
import shutil
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def clean_workspace(dry_run: bool = False):
    total_freed = 0
    removed_items = []

    def remove_file(p: Path):
        nonlocal total_freed
        if p.exists():
            size = p.stat().st_size
            total_freed += size
            removed_items.append(f"FILE: {p.relative_to(PROJECT_ROOT)} ({size / 1024:.1f} KB)")
            if not dry_run:
                try:
                    p.unlink()
                except Exception as e:
                    print(f"Lỗi khi xoá file {p}: {e}")

    def remove_dir(p: Path):
        nonlocal total_freed
        if p.exists() and p.is_dir():
            size = sum(f.stat().st_size for f in p.glob('**/*') if f.is_file())
            total_freed += size
            removed_items.append(f"DIR:  {p.relative_to(PROJECT_ROOT)} ({size / 1024:.1f} KB)")
            if not dry_run:
                try:
                    shutil.rmtree(p)
                except Exception as e:
                    print(f"Lỗi khi xoá thư mục {p}: {e}")

    print(f"[*] Bắt đầu quét và dọn dẹp rác tại: {PROJECT_ROOT}")
    if dry_run:
        print("[!] Chế độ DRY-RUN (chỉ kiểm tra, không xoá)")

    # 1. Dọn shots/ (chỉ giữ thư mục, xoá hết screenshots/frames tạm)
    shots_dir = PROJECT_ROOT / "shots"
    if shots_dir.exists():
        for item in shots_dir.iterdir():
            if item.name.startswith("."):
                continue
            if item.is_file():
                remove_file(item)
            elif item.is_dir():
                remove_dir(item)

    # 2. Dọn scratch media & archives
    scratch_dir = PROJECT_ROOT / "scratch"
    if scratch_dir.exists():
        for ext in ["*.wav", "*.mp3", "*.mp4", "*.tgz", "*.jpg", "*.png"]:
            for item in scratch_dir.glob(ext):
                remove_file(item)
        for item in scratch_dir.glob("restructure/*.tgz"):
            remove_file(item)
        if (scratch_dir / "frames").exists():
            remove_dir(scratch_dir / "frames")
        test_hf = scratch_dir / "test_hyperframes" / "demo"
        if test_hf.exists():
            remove_file(test_hf / "out.mp4")
            remove_dir(test_hf / ".thumbnails")
            remove_dir(test_hf / ".hyperframes")

    # 3. Dọn output/ temp caches và files rác nằm sai chỗ
    output_dir = PROJECT_ROOT / "output"
    if output_dir.exists():
        for temp_dir in output_dir.glob("temp_*"):
            if temp_dir.is_dir():
                remove_dir(temp_dir)
        for loose_audio in output_dir.glob("*.wav"):
            remove_file(loose_audio)
        for test_file in output_dir.glob("test_*"):
            if test_file.is_file():
                remove_file(test_file)

    # 4. Dọn file rác macOS (.DS_Store, __MACOSX)
    for ds in PROJECT_ROOT.glob("**/.DS_Store"):
        remove_file(ds)
    for macosx in PROJECT_ROOT.glob("**/__MACOSX"):
        if macosx.is_dir():
            remove_dir(macosx)

    # 5. Dọn __pycache__ & *.pyc bên ngoài .venv
    for pyc in PROJECT_ROOT.glob("**/*.pyc"):
        if ".venv" not in pyc.parts:
            remove_file(pyc)
    for pycache in PROJECT_ROOT.glob("**/__pycache__"):
        if ".venv" not in pycache.parts and pycache.is_dir():
            remove_dir(pycache)

    # Báo cáo kết quả
    print("\n" + "=" * 60)
    print(f"TỔNG KẾT DỌN DẸP ({'DRY-RUN' if dry_run else 'HOÀN TẤT'}):")
    print(f"- Số mục xử lý: {len(removed_items)}")
    for item in removed_items:
        print(f"  * {item}")
    print(f"- Dung lượng giải phóng: {total_freed / (1024 * 1024):.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean temporary & junk files in workspace.")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ liệt kê không xoá")
    args = parser.parse_args()
    clean_workspace(dry_run=args.dry_run)
