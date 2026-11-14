"""Integration tests for SnapTik Web API endpoints."""

import unittest
from unittest.mock import MagicMock, patch
from starlette.testclient import TestClient

from gobi.domain.snaptik_models import (
    SnaptikAuthor,
    SnaptikStats,
    SnaptikMedia,
    SnaptikVideoItem,
    SnaptikDownloadResult,
)
from gobi.services.media.snaptik_web import app


class TestSnaptikWebApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("SnapTik Gobi", response.text)
        self.assertIn("Kho Sản Phẩm", response.text)

    @patch("gobi.services.media.snaptik_web.ingest_tiktok_product")
    def test_post_ingest_product_endpoint(self, mock_ingest):
        mock_ingest.return_value = {
            "success": True,
            "total_ingested": 1,
            "catalog_file": "data/products/catalog.json",
            "products": [{
                "product_id": "123",
                "title": "Quần short",
                "folder": "data/products/123_quan_short",
                "metadata_file": "data/products/123_quan_short/product.json"
            }]
        }
        resp = self.client.post("/api/ingest-product", json={
            "url": "https://www.tiktok.com/@test/video/123456",
            "download_video": True
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["products"][0]["product_id"], "123")

    @patch("gobi.services.media.snaptik_web.service.get_info")
    def test_post_extract_success(self, mock_get_info):
        mock_get_info.return_value = SnaptikVideoItem(
            id="123456",
            original_url="https://www.tiktok.com/@test/video/123456",
            title="Video Test",
            author=SnaptikAuthor(unique_id="test", nickname="Test User"),
            stats=SnaptikStats(plays=5000, likes=100),
            media=SnaptikMedia(
                video_url="https://cdn.example.com/clean.mp4",
                audio_url="https://cdn.example.com/audio.mp3",
                cover_url="https://cdn.example.com/cover.jpg",
            )
        )

        resp = self.client.post("/api/extract", json={"url": "https://www.tiktok.com/@test/video/123456"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["id"], "123456")
        self.assertEqual(data["data"]["media"]["video_url"], "https://cdn.example.com/clean.mp4")

    @patch("gobi.services.media.snaptik_web.service.download")
    def test_post_download_success(self, mock_download):
        mock_download.return_value = SnaptikDownloadResult(
            success=True,
            video_path="output/videos/test.mp4",
            audio_path="output/audio/test_audio.mp3",
            metadata_path="output/videos/test.json",
        )

        resp = self.client.post("/api/download", json={
            "url": "https://www.tiktok.com/@test/video/123456",
            "download_audio": True,
            "hd": True
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["video_path"], "output/videos/test.mp4")


if __name__ == "__main__":
    unittest.main()
