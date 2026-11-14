"""
GOBI SOCIAL - SETUP 30 BATCH ACCOUNTS MATRIX
============================================
Tạo và quản lý danh sách 30 tài khoản email (Catch-All Routing)
để phục vụ phân bổ vòng lặp sinh 42 góc ảnh KOC AI.
"""

import json
from pathlib import Path

CONFIG_PATH = Path("configs/koc_30_batch_accounts.json")
CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Tên miền catch-all mặc định (hoặc subdomain anonaddy)
BASE_DOMAIN = "gobikoc.anonaddy.com"

ACCOUNTS = []
for i in range(1, 31):
    acc_id = f"gobi_koc_worker_{i:02d}"
    email = f"koc.worker.{i:02d}@{BASE_DOMAIN}"
    ACCOUNTS.append({
        "index": i,
        "account_id": acc_id,
        "email": email,
        "status": "READY",
        "assigned_angles": [],
        "completed_angles": [],
        "quota_per_day": 2,
        "notes": f"Tài khoản worker {i} nhận OTP tự động qua catch-all"
    })

# Phân bổ 42 góc chụp vào 30 tài khoản (mỗi tài khoản gánh 1-2 góc để hoàn toàn không bị dính rate limit!)
for idx in range(1, 43):
    worker_idx = (idx - 1) % 30
    ACCOUNTS[worker_idx]["assigned_angles"].append(idx)

data = {
    "system": "Gobi 30 Batch Accounts Dispatcher",
    "total_accounts": 30,
    "total_angles": 42,
    "destination_forwarding_inbox": "dinhthienthoai@gmail.com",
    "accounts": ACCOUNTS
}

CONFIG_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[+] Đã tạo ma trận 30 tài khoản tại: {CONFIG_PATH}")
print(f" • 30 tài khoản chia sẻ tải 42 góc chụp (tối đa 1-2 góc/tài khoản)")
print(f" • Hộp thư gom OTP tự động: dinhthienthoai@gmail.com")
