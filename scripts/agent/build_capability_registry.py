"""Quét skill / rule / workflow / CLI của Gobi Social và sinh registry cho mọi AI tool.

Nguồn sự thật duy nhất: `.agents/` (`.agent/` và `.claude/skills` là symlink tới đây).
Output: `docs/AI_CAPABILITIES.md` + `.agents/registry.json`.

Usage: python scripts/agent/build_capability_registry.py [--check]
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
AGENTS = os.path.join(ROOT, ".agents")
CLI_DIR = os.path.join(ROOT, "src", "gobi", "cli")


def frontmatter(path):
    """Parse tối giản YAML frontmatter (name/description, hỗ trợ `>` và chuỗi nháy)."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not m:
        return {}, text
    data, key, buf = {}, None, []
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km and not line.startswith(" "):
            if key:
                data[key] = " ".join(buf).strip()
            key, val = km.group(1), km.group(2).strip()
            buf = [] if val in (">", "|", ">-", "|-") else [val]
        elif key:
            buf.append(line.strip())
    if key:
        data[key] = " ".join(buf).strip()
    for k, v in data.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            data[k] = v[1:-1].replace("''", "'")
    return data, text


def scan_skills():
    out = []
    base = os.path.join(AGENTS, "skills")
    for name in sorted(os.listdir(base)):
        p = os.path.join(base, name, "SKILL.md")
        if os.path.isfile(p):
            fm, _ = frontmatter(p)
            out.append({
                "name": fm.get("name", name),
                "path": os.path.relpath(p, ROOT),
                "description": fm.get("description", ""),
                "manual_only": fm.get("disable-model-invocation") == "true",
            })
    return out


def scan_docs(sub):
    out = []
    base = os.path.join(AGENTS, sub)
    if not os.path.isdir(base):
        return out
    for fn in sorted(os.listdir(base)):
        if fn.endswith(".md"):
            p = os.path.join(base, fn)
            fm, text = frontmatter(p)
            title = next((l.lstrip("# ").strip() for l in text.splitlines() if l.startswith("#")), fn)
            out.append({
                "name": fn[:-3],
                "path": os.path.relpath(p, ROOT),
                "always_on": fm.get("trigger") == "always_on",
                "summary": fm.get("description") or title,
            })
    return out


def scan_cli():
    cmds = {}
    for fn in sorted(os.listdir(CLI_DIR)):
        if fn.endswith(".py"):
            with open(os.path.join(CLI_DIR, fn), encoding="utf-8") as f:
                src = f.read()
            for mm in re.finditer(r'(\w+)\s*=\s*\w+\.add_parser\(\s*"([\w-]+)"(?:[^)]*?help="([^"]*)")?', src):
                if mm.group(1).endswith("_sub") or mm.group(1) in ("list_p", "get_p", "up_p", "assign_p"):
                    continue
                cmds.setdefault(mm.group(2), mm.group(3) or "")
    return [{"command": f"python -m gobi {k}", "help": v} for k, v in sorted(cmds.items())]


def render(reg):
    L = ["# AI CAPABILITIES — Skill, Rule, Workflow & CLI của Gobi Social",
         "",
         "> **Auto-generated** bởi `python scripts/agent/build_capability_registry.py` — KHÔNG sửa tay. "
         "Máy đọc: [`.agents/registry.json`](../.agents/registry.json).",
         "",
         "## Quy ước chung cho MỌI AI tool (Claude Code, Cursor, Gemini, Codex, Antigravity...)",
         "- **Nguồn sự thật duy nhất:** thư mục [`.agents/`](../.agents). `.agent/` và `.claude/skills` là symlink trỏ về đây — "
         "thêm/sửa skill CHỈ ở `.agents/skills/<tên>/SKILL.md`, rồi chạy lại script này.",
         "- **Cách dùng 1 skill:** mở `.agents/skills/<tên>/SKILL.md`, đọc đầy đủ rồi làm theo. Tool không có cơ chế skill native "
         "vẫn dùng được bằng cách đọc file đó trực tiếp.",
         "- **Video:** bắt đầu từ skill `hyperframes` (entry point bắt buộc), sau đó skill con phù hợp.",
         "- Luật dự án: [`AGENTS.md`](../AGENTS.md) · kiến trúc: [`ARCHITECTURE.md`](../ARCHITECTURE.md) · tiếp quản: [`CONTINUITY.md`](../CONTINUITY.md).",
         "",
         f"## 1. Skills ({len(reg['skills'])})",
         "",
         "| Skill | Mô tả | Ghi chú |", "|---|---|---|"]
    for s in reg["skills"]:
        d = s["description"].replace("|", "\\|")
        d = d if len(d) <= 220 else d[:217] + "..."
        note = "chỉ gọi thủ công" if s["manual_only"] else ""
        L.append(f"| [`{s['name']}`](../{s['path']}) | {d} | {note} |")
    L += ["", f"## 2. Rules ({len(reg['rules'])})", "", "| Rule | Always-on | Tóm tắt |", "|---|---|---|"]
    for r in reg["rules"]:
        L.append(f"| [`{r['name']}`](../{r['path']}) | {'yes' if r['always_on'] else ''} | {r['summary'][:140].replace('|', '/')} |")
    L += ["", f"## 3. Workflows ({len(reg['workflows'])})", "", "| Workflow | Tóm tắt |", "|---|---|"]
    for w in reg["workflows"]:
        L.append(f"| [`{w['name']}`](../{w['path']}) | {w['summary']} |")
    L += ["", f"## 4. Gobi CLI ({len(reg['cli'])})", "", "| Lệnh | Chức năng |", "|---|---|"]
    for c in reg["cli"]:
        L.append(f"| `{c['command']}` | {c['help']} |")
    L += ["", "## 5. Agent runtime trong code",
          "- `scripts/agent/run_agent.py` → `gobi.services.os_kernel.AgentOS` (Agent-Reach, browser-use, video/subtitle inspector).",
          "- `integrations/agent_reach/`, `integrations/hyperframes/` (có `AGENTS.md` riêng), `integrations/OmniVoice/`, `integrations/Wav2Lip/`.",
          "- Subagent: không có định nghĩa riêng trong repo; tool nào hỗ trợ subagent thì dùng built-in của tool đó và truyền kèm quy tắc `AGENTS.md`.",
          ""]
    return "\n".join(L)


def main():
    reg = {"skills": scan_skills(), "rules": scan_docs("rules"), "workflows": scan_docs("workflows"), "cli": scan_cli()}
    md, js = render(reg), json.dumps(reg, ensure_ascii=False, indent=2) + "\n"
    targets = {os.path.join(ROOT, "docs", "AI_CAPABILITIES.md"): md, os.path.join(AGENTS, "registry.json"): js}
    if "--check" in sys.argv:
        stale = [p for p, c in targets.items() if not os.path.isfile(p) or open(p, encoding="utf-8").read() != c]
        print("STALE: " + ", ".join(os.path.relpath(p, ROOT) for p in stale) if stale else "OK")
        sys.exit(1 if stale else 0)
    for p, c in targets.items():
        with open(p, "w", encoding="utf-8") as f:
            f.write(c)
        print("wrote", os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
