"""
Test integration of OmniVoice within Gobi Social.
"""

import os
import unittest
from pathlib import Path

from gobi.adapters.integrations.omnivoice_adapter import OmniVoiceAdapter
from gobi.services.voice.voice_cloner import VoiceCloner


class TestOmniVoiceIntegration(unittest.TestCase):
    def test_omnivoice_adapter_initialization(self):
        adapter = OmniVoiceAdapter()
        self.assertTrue(adapter.python_exe.exists())
        self.assertIn("OmniVoice", str(adapter.python_exe))

    def test_voice_cloner_default_engine(self):
        vault_dir = Path("assets/voice_vault/voice-fm-lyly")
        self.assertTrue((vault_dir / "omnivoice_prompt.pt").exists())
        self.assertTrue((vault_dir / "reference_clean_slice.wav").exists())

    def test_omnivoice_synthesis_smoke(self):
        cloner = VoiceCloner()
        output_mp3 = Path("output/_test_omnivoice_smoke.mp3")
        if output_mp3.exists():
            output_mp3.unlink()

        res = cloner.speak(
            profile_id="voice-fm-lyly",
            new_script="Chào Gô bi nhé!",
            output_path=str(output_mp3),
            engine="omnivoice",
            master=True
        )
        self.assertTrue(Path(res).exists())
        self.assertGreater(Path(res).stat().st_size, 1000)

        # Cleanup
        if output_mp3.exists():
            output_mp3.unlink()


if __name__ == "__main__":
    unittest.main()
