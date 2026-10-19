"""
VMAX KOC AI Production Engine
Tich hop tri thuc tu Tuong Vi (W5G Martech) va he thong ma tran 36 goc may cua VMAX.
"""

import os
import sys
import json

# Dam bao UTF-8 console tren Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUB_FILE = os.path.join(PROJECT_ROOT, "configs", "koc_ai_knowledge_hub.json")
PANEL_MANIFEST = os.path.join(PROJECT_ROOT, "affiliate_tiktok", "sample_video", "koc_matrix_panels", "manifest.json")

def load_hub_data():
    if os.path.exists(HUB_FILE):
        with open(HUB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_panels_manifest():
    if os.path.exists(PANEL_MANIFEST):
        with open(PANEL_MANIFEST, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_recommended_model_for_task(task_type: str):
    hub = load_hub_data()
    matrix = hub.get("ai_model_matrix", {})
    mapping = {
        "image": "Nano_Banana_Flux",
        "key_visual": "Nano_Banana_Flux",
        "motion": "Kling_3_0",
        "camera": "Kling_3_0",
        "storytelling": "Seedance",
        "lipsync": "Seedance",
        "realism": "Sora_2_Pro_Veo_3_1",
        "flagship": "Sora_2_Pro_Veo_3_1",
        "fast_test": "Grok_Aurora",
        "pipeline": "Wan"
    }
    key = mapping.get(task_type.lower(), "Nano_Banana_Flux")
    return {key: matrix.get(key, {})}

def get_vmax_system_overview():
    hub = load_hub_data()
    panels = load_panels_manifest()
    growth = hub.get("channel_growth_protocol_2000_followers", {})
    return {
        "system_name": hub.get("system_name"),
        "version": hub.get("version"),
        "total_consistency_panels": len(panels),
        "models_integrated": list(hub.get("ai_model_matrix", {}).keys()),
        "workflow_steps": len(hub.get("production_workflow_5_steps", [])),
        "target_growth": growth.get("target"),
        "content_ratio": growth.get("content_ratio")
    }

if __name__ == "__main__":
    overview = get_vmax_system_overview()
    print("======================================================================")
    print("           VMAX KOC AI PRODUCTION ENGINE - OVERVIEW                   ")
    print("======================================================================")
    print(f"[*] He thong: {overview['system_name']} v{overview['version']}")
    print(f"[*] Ma tran goc may hien tai: {overview['total_consistency_panels']} panels da co san")
    print(f"[*] Cac Model AI trong ma tran: {', '.join(overview['models_integrated'])}")
    print(f"[*] Quy trinh san xuat tieu chuan: {overview['workflow_steps']} buoc khep kin")
    print(f"[*] Muc tieu tang truong kenh: {overview['target_growth']}")
    print(f"[*] Ty le vang noi dung: {overview['content_ratio']}")
    print("======================================================================")
