"""Unit tests for SnapTik domain models, scraper adapter, and service."""

import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from gobi.adapters.scrapers.snaptik_scraper import SnaptikScraper
from gobi.domain.snaptik_models import (
    SnaptikAuthor,
    SnaptikMusic,
    SnaptikStats,
    SnaptikMedia,
    SnaptikVideoItem,
    SnaptikDownloadResult,
)
from gobi.services.media.snaptik_service import SnaptikService, sanitize_filename


class TestSnaptikModels(unittest.TestCase):
    def test_model_instantiation_and_serialization(self):
        author = SnaptikAuthor(id="123", unique_id="user_test", nickname="User Test", avatar="https://example.com/avatar.jpg")
        stats = SnaptikStats(plays=1000, likes=200, comments=50, shares=10)
        media = SnaptikMedia(
            video_url="https://example.com/clean.mp4",
            video_hd_url="https://example.com/hd.mp4",
            watermark_video_url="https://example.com/wm.mp4",
            audio_url="https://example.com/audio.mp3",
            cover_url="https://example.com/cover.jpg",
        )
        item = SnaptikVideoItem(
            id="7680784467144887573",
            original_url="https://www.tiktok.com/@user_test/video/7680784467144887573",
            title="Video Thử Nghiệm",
            duration=30,
            author=author,
            stats=stats,
            media=media,
        )

        data = item.model_dump()
        self.assertEqual(data["id"], "7680784467144887573")
        self.assertEqual(data["author"]["unique_id"], "user_test")
        self.assertEqual(data["stats"]["likes"], 200)
        self.assertEqual(data["media"]["video_url"], "https://example.com/clean.mp4")

    def test_sanitize_filename(self):
        # Vietnamese diacritics
        raw = "Áo Khoác Cardigan Len Kiểu Pháp Mới Nhất 2026!"
        clean = sanitize_filename(raw, max_length=50)
        self.assertTrue("Ao_Khoac_Cardigan" in clean)
        self.assertNotIn("!", clean)
        self.assertNotIn(" ", clean)

        # Truncation
        long_name = "a" * 100
        truncated = sanitize_filename(long_name, max_length=40)
        self.assertEqual(len(truncated), 40)

        # Empty fallback
        self.assertEqual(sanitize_filename(""), "tiktok_video")


class TestSnaptikScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = SnaptikScraper()

    def test_normalize_url(self):
        url = "https://www.tiktok.com/@test/video/12345?is_from_webapp=1&sender_device=pc"
        normalized = self.scraper.normalize_url(url)
        self.assertEqual(normalized, "https://www.tiktok.com/@test/video/12345")

        # Keep short link intact
        short_url = "https://vt.tiktok.com/ZS2xyz/?k=1"
        self.assertEqual(self.scraper.normalize_url(short_url), "https://vt.tiktok.com/ZS2xyz/?k=1")

    @patch("httpx.Client.get")
    def test_extract_via_tikwm_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 0,
            "msg": "success",
            "data": {
                "id": "7680784467144887573",
                "title": "Ao Khoac Dep",
                "duration": 15,
                "play": "https://cdn.example.com/video.mp4",
                "hdplay": "https://cdn.example.com/video_hd.mp4",
                "wmplay": "https://cdn.example.com/video_wm.mp4",
                "music": "https://cdn.example.com/music.mp3",
                "cover": "https://cdn.example.com/cover.jpg",
                "play_count": 50000,
                "digg_count": 2500,
                "comment_count": 80,
                "share_count": 35,
                "author": {
                    "id": "999",
                    "unique_id": "test_creator",
                    "nickname": "Creator Test",
                    "avatar": "https://cdn.example.com/avatar.jpg"
                }
            }
        }
        mock_get.return_value = mock_response

        item = self.scraper._extract_via_tikwm("https://www.tiktok.com/@test_creator/video/7680784467144887573")
        self.assertIsNotNone(item)
        self.assertEqual(item.id, "7680784467144887573")
        self.assertEqual(item.author.unique_id, "test_creator")
        self.assertEqual(item.media.video_url, "https://cdn.example.com/video.mp4")
        self.assertEqual(item.stats.plays, 50000)

    @patch.object(SnaptikScraper, "_extract_via_tikwm")
    @patch.object(SnaptikScraper, "_extract_via_ytdlp")
    def test_extract_fallback_loop(self, mock_ytdlp, mock_tikwm):
        # TikWM fails, yt-dlp succeeds
        mock_tikwm.side_effect = Exception("Rate limit on TikWM")

        mock_item = SnaptikVideoItem(
            id="7680784467144887573",
            original_url="https://www.tiktok.com/@test/video/7680784467144887573",
            title="Fallback Video",
            media=SnaptikMedia(video_url="https://cdn.ytdlp.com/video.mp4"),
            source_engine="ytdlp"
        )
        mock_ytdlp.return_value = mock_item

        result = self.scraper.extract("https://www.tiktok.com/@test/video/7680784467144887573")
        self.assertEqual(result.source_engine, "ytdlp")
        self.assertEqual(result.media.video_url, "https://cdn.ytdlp.com/video.mp4")


class TestSnaptikService(unittest.TestCase):
    def setUp(self):
        self.mock_scraper = MagicMock(spec=SnaptikScraper)
        self.service = SnaptikService(scraper=self.mock_scraper)

    def test_download_orchestration(self):
        mock_item = SnaptikVideoItem(
            id="998877",
            original_url="https://www.tiktok.com/@creator/video/998877",
            title="Cardigan Trend",
            author=SnaptikAuthor(unique_id="creator", nickname="Creator"),
            stats=SnaptikStats(plays=1000),
            media=SnaptikMedia(
                video_url="https://cdn.example.com/clean.mp4",
                audio_url="https://cdn.example.com/audio.mp3",
                cover_url="https://cdn.example.com/cover.jpg",
            )
        )
        self.mock_scraper.extract.return_value = mock_item

        def fake_download(url, dest, on_progress=None):
            Path(dest).parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                f.write(b"FAKE_DATA")
            return dest

        self.mock_scraper.download_stream.side_effect = fake_download

        res = self.service.download(
            url="https://www.tiktok.com/@creator/video/998877",
            output_dir="scratch/test_snaptik_output",
            download_audio=True,
            download_cover=True,
            save_metadata=True,
        )

        self.assertTrue(res.success)
        self.assertIsNotNone(res.video_path)
        self.assertTrue(Path(res.video_path).exists())
        self.assertTrue(Path(res.audio_path).exists())
        self.assertTrue(Path(res.cover_path).exists())
        self.assertTrue(Path(res.metadata_path).exists())

        # Check metadata json content
        with open(res.metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        self.assertEqual(meta["id"], "998877")
        self.assertEqual(meta["author"]["unique_id"], "creator")

        # Clean up test output
        import shutil
        shutil.rmtree("scratch/test_snaptik_output", ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
