"""
Multi-Platform Media & Content Inspector Tool
Wraps Agent-Reach capabilities: YouTube metadata/subtitles, Bilibili info, Web reader (Jina Reader), and RSS feeds.
"""

import os
import json
import subprocess
import urllib.request
import feedparser

class MediaReachTool:
    def __init__(self, venv_scripts_dir: str = None):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        if not venv_scripts_dir:
            bin_dir = os.path.join(project_root, ".venv", "bin")
            scripts_dir = os.path.join(project_root, ".venv", "Scripts")
            self.venv_scripts_dir = bin_dir if os.path.exists(bin_dir) else scripts_dir
        else:
            self.venv_scripts_dir = venv_scripts_dir

        bin_exe = os.path.join(self.venv_scripts_dir, "yt-dlp")
        win_exe = os.path.join(self.venv_scripts_dir, "yt-dlp.exe")
        self.yt_dlp_path = win_exe if os.path.exists(win_exe) else (bin_exe if os.path.exists(bin_exe) else "yt-dlp")


    def inspect_youtube(self, url: str) -> dict:
        """Lay metadata va thong tin video YouTube qua yt-dlp."""
        cmd = [self.yt_dlp_path, "--dump-json", url]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8")
            data = json.loads(result.stdout)
            return {
                "platform": "YouTube",
                "title": data.get("title"),
                "uploader": data.get("uploader"),
                "duration": data.get("duration_string"),
                "views": data.get("view_count"),
                "description": data.get("description", "")[:500] + "...",
                "tags": data.get("tags", []),
                "webpage_url": data.get("webpage_url")
            }
        except Exception as e:
            return {"error": f"Failed to inspect YouTube: {str(e)}"}

    def get_youtube_subtitles(self, url: str, output_dir: str = "temp_subs", lang: str = "vi,en") -> dict:
        """Tai phu de / transcript cua video YouTube."""
        os.makedirs(output_dir, exist_ok=True)
        cmd = [
            self.yt_dlp_path,
            "--write-sub",
            "--write-auto-sub",
            "--sub-lang", lang,
            "--skip-download",
            "-o", f"{output_dir}/%(id)s",
            url
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {"status": "success", "output_dir": output_dir, "logs": res.stdout}
        except Exception as e:
            return {"error": f"Failed to get subtitles: {str(e)}"}

    def read_web_content(self, url: str) -> str:
        """Doc noi dung trang web duoi dang Markdown sach qua Jina Reader."""
        jina_url = f"https://r.jina.ai/{url}"
        req = urllib.request.Request(jina_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8")
        except Exception as e:
            return f"Failed to read web via Jina Reader: {str(e)}"

    def parse_rss_feed(self, feed_url: str) -> list:
        """Doc ban tin / RSS feed tu bat ky website nao."""
        feed = feedparser.parse(feed_url)
        items = []
        for entry in feed.entries[:10]:
            items.append({
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": entry.get("published", entry.get("updated", "")),
                "summary": entry.get("summary", "")[:250]
            })
        return items
