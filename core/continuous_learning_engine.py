"""
VMAX Continuous Learning & Experience Optimization Engine
Co che tu hoc, ghi nhan chi so video thuc te, rut kinh nghiem
va tu dong tinh chinh (Auto-Tune) cong thuc KOC AI de khong bao gio bi flop.
"""

import os
import sys
import json
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(PROJECT_ROOT, "configs", "koc_learning_memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def record_video_feedback(video_id: str, title: str, format_name: str, hook: str, views: int, completion_rate: float, orders: int, notes: str):
    """
    Ghi nhan chi so thuc te sau khi video duoc dang tai de he thong tu danh gia va hoc hoi.
    """
    mem = load_memory()
    is_win = (views >= 1000 and completion_rate >= 20.0) or (orders >= 5)
    status = "WINNING_BENCHMARK" if is_win else "NEEDS_OPTIMIZATION"
    
    new_log = {
        "video_id": video_id,
        "title": title,
        "format": format_name,
        "hook_type": hook,
        "metrics": {
            "views": views,
            "completion_rate": f"{completion_rate}%",
            "orders_generated": orders
        },
        "status": status,
        "extracted_takeaway": notes
    }
    
    mem.setdefault("video_performance_logs", []).append(new_log)
    
    # Neu la bai hoc moi, them vao historical_lessons
    lesson_id = f"LSN-{len(mem.get('historical_lessons', [])) + 1:03d}"
    new_lesson = {
        "lesson_id": lesson_id,
        "date": time.strftime("%Y-%m-%d"),
        "category": f"Dynamic Learning from {video_id}",
        "finding": f"Video '{title}' dat {views} views, {orders} don hang voi hook: '{hook}'.",
        "actionable_rule": notes
    }
    mem.setdefault("historical_lessons", []).append(new_lesson)
    
    save_memory(mem)
    print(f"[+] Da cap nhat bai hoc kinh nghiem: {lesson_id} - Trang thai: {status}")
    return new_log

def get_learning_summary():
    mem = load_memory()
    lessons = mem.get("historical_lessons", [])
    logs = mem.get("video_performance_logs", [])
    weights = mem.get("auto_tuned_prompt_weights", {})
    return {
        "total_lessons_learned": len(lessons),
        "total_experiments_recorded": len(logs),
        "preferred_hooks": weights.get("preferred_hooks", []),
        "latest_lessons": lessons[-3:] if lessons else []
    }

if __name__ == "__main__":
    print("======================================================================")
    print("       VMAX CONTINUOUS LEARNING & EXPERIENCE OPTIMIZATION ENGINE      ")
    print("======================================================================")
    summary = get_learning_summary()
    print(f"[*] Tong so bai hoc he thong da tich luy: {summary['total_lessons_learned']}")
    print(f"[*] Tong so video thi nghiem da ghi nhan: {summary['total_experiments_recorded']}")
    print("\n--- Cac Hook dang duoc uu tien cao nhat (Auto-Tuned) ---")
    for h in summary["preferred_hooks"]:
        print(f"  + {h}")
    print("\n--- 3 Bai hoc kinh nghiem gan nhat ---")
    for l in summary["latest_lessons"]:
        print(f"  [{l['lesson_id']}] {l['category']}:")
        print(f"     -> Quy tac: {l['actionable_rule']}")
    print("======================================================================")
