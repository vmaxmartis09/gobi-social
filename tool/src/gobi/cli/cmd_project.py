"""gobi project list | new <tên> | use <tên> | where — quản lý các project trong data source."""
from gobi import paths


def register_project_parser(subparsers):
    p = subparsers.add_parser("project", help="Quản lý các project dữ liệu (nhân vật, library, tài khoản, kết quả theo từng project)")
    sub = p.add_subparsers(dest="project_action", required=True)
    sub.add_parser("list", help="Liệt kê project và đánh dấu project đang dùng")
    sub.add_parser("where", help="In đường dẫn data source và project đang dùng")
    new_p = sub.add_parser("new", help="Tạo project mới từ khung chuẩn")
    new_p.add_argument("name")
    use_p = sub.add_parser("use", help="Chọn project mặc định")
    use_p.add_argument("name")
    return p


def handle_project_command(args) -> int:
    action = args.project_action
    if action == "list":
        active = paths.active_project()
        for name in paths.list_projects():
            print(("* " if name == active else "  ") + name)
        return 0
    if action == "where":
        print(f"data   : {paths.DATA_DIR}\nproject: {paths.project_dir()}")
        return 0
    name = args.name
    if not name.replace("-", "").replace("_", "").isalnum() or name.startswith("_"):
        print("[!] Tên project chỉ gồm chữ/số/-/_ và không bắt đầu bằng '_'.")
        return 1
    if action == "new":
        base = paths.scaffold_project(name)
        print(f"[+] Đã tạo project '{name}' tại {base}")
        return 0
    if action == "use":
        if name not in paths.list_projects():
            print(f"[!] Project '{name}' chưa tồn tại. Tạo bằng: python -m gobi project new {name}")
            return 1
        paths.set_active_project(name)
        print(f"[+] Project mặc định: {name}")
        return 0
    return 1
