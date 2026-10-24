"""
GOBI VOICE ENGINE 2.0 - UNIFIED VOICE CLONER
============================================
Động cơ nhân bản giọng nói Tiếng Việt thuần Việt đa tầng:
- Tự động hóa từ video/mp3 đầu vào -> Hồ sơ âm thanh (Sound Profile).
- Hỗ trợ đa mô hình: VieNeu-TTS v3 Turbo, Seed-VC, F5-TTS và Edge-TTS.
- Tự động hóa toàn bộ chuỗi: Tách âm -> VAD cắt lát -> Whisper STT -> Clone -> Mastering -14 LUFS.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import imageio_ffmpeg
from gradio_client import Client, handle_file

from gobi.services.voice.audio_preprocessor import AudioPreprocessor
from gobi.services.voice.audio_mastering import AudioMastering

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
DEFAULT_PROFILES_DIR = os.path.join(PROJECT_ROOT, "assets", "voice_vault")
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# Câu nói mặc định bắt buộc cho mọi giọng đọc clone trong hệ thống Gobi
DEFAULT_CLONED_GREETING = "Hello gô bi thúi của em , em là Gô bi của anh đây nè !"

class VoiceCloner:
    def __init__(self, profiles_dir: str = DEFAULT_PROFILES_DIR, whisper_model: str = "base"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.preprocessor = AudioPreprocessor(whisper_model=whisper_model)
        self.mastering = AudioMastering()
        self._local_vieneu = None

    def _get_local_vieneu(self):
        if self._local_vieneu is None:
            from vieneu import Vieneu
            onnx_dir = os.path.join(PROJECT_ROOT, "models", "vieneu_v3_turbo", "onnx_update")
            codec_dir = os.path.join(PROJECT_ROOT, "models", "moss_audio_tokenizer")
            if os.path.exists(onnx_dir) and os.path.exists(codec_dir):
                self._local_vieneu = Vieneu(onnx_dir=onnx_dir, codec_dir=codec_dir)
            else:
                self._local_vieneu = Vieneu()
        return self._local_vieneu

    def create_profile(
        self,
        media_path: str,
        profile_id: str,
        speaker_name: Optional[str] = None,
        dialect: str = "north",
        style: str = "tiktok_action_review",
        custom_transcript: Optional[str] = None,
        target_duration: float = 4.5
    ) -> Dict[str, Any]:
        """
        Tạo hồ sơ giọng nói độc lập (Sound Profile) từ bất kỳ Video hoặc MP3 nào:
        1. Làm sạch audio, tách tạp âm
        2. Tự động cắt lát vàng 4.5s
        3. Tự động chép lời đối chiếu (hoặc dùng text người dùng cung cấp)
        4. Tự động xuất 1 file source gốc giọng đọc (source_original_preview.mp3)
        5. Tự động xuất 1 file giọng clone đọc câu chào mặc định:
           'Hello gô bi thúi của em , em là Gô bi của anh đây nè !' (cloned_default_sample.mp3)
        6. Lưu trữ vào assets/voice_vault/<profile_id>/ và copy sang output/
        """
        profile_folder = self.profiles_dir / profile_id
        profile_folder.mkdir(parents=True, exist_ok=True)

        print(f"\n=======================================================")
        print(f"📦 KHỞI TẠO SOUND PROFILE: {profile_id}")
        print(f"-> Nguồn dữ liệu: {media_path}")
        print(f"=======================================================")

        prep_data = self.preprocessor.process_media(
            input_media_path=media_path,
            output_dir=str(profile_folder),
            target_duration=target_duration
        )

        transcript = custom_transcript.strip() if custom_transcript else prep_data["transcript"]
        transcript_file = profile_folder / "reference_transcript.txt"
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(transcript)

        # 1. TẠO FILE SOURCE GỐC GIỌNG ĐỌC (source_original_preview.mp3)
        source_preview_mp3 = profile_folder / "source_original_preview.mp3"
        print(f"\n[Preview] Đang xuất file source gốc giọng đọc: {source_preview_mp3.name}...")
        self.mastering.master_tiktok_koc(
            input_audio_path=str(prep_data["ref_slice_wav"]),
            output_audio_path=str(source_preview_mp3),
            target_lufs=-14.0,
            presence_boost_db=2.5,
            tempo_factor=1.00
        )

        meta = {
            "profile_id": profile_id,
            "speaker_name": speaker_name or profile_id,
            "dialect": dialect,
            "style": style,
            "source_media": os.path.abspath(media_path),
            "source_preview_mp3": str(source_preview_mp3.resolve()),
            "ref_slice_wav": os.path.abspath(prep_data["ref_slice_wav"]),
            "full_wav": os.path.abspath(prep_data["full_wav"]),
            "duration": prep_data["duration"],
            "rms": prep_data["rms"],
            "transcript": transcript,
            "default_greeting": DEFAULT_CLONED_GREETING,
            "created_at": str(Path(media_path).stat().st_mtime)
        }

        # 1. Trích xuất & Lưu OmniVoice Prompt (.pt) chuẩn hóa
        try:
            from gobi.adapters.integrations.omnivoice_adapter import OmniVoiceAdapter
            adapter = OmniVoiceAdapter()
            prompt_pt = adapter.create_prompt(
                profile_dir=str(profile_folder),
                ref_slice=str(prep_data["ref_slice_wav"]),
                ref_text=transcript
            )
            meta["engine"] = "omnivoice"
            meta["omnivoice_prompt"] = prompt_pt
            print(f"[VoiceCloner] Đã trích xuất & lưu OmniVoice Prompt -> {prompt_pt}")
        except Exception as e_omni:
            print(f"[!] Không thể trích xuất OmniVoice Prompt: {e_omni}")

        # Trích xuất Speaker Embedding độ nét cao từ toàn bộ audio vocal gốc (full_wav)
        try:
            import soundfile as sf
            import numpy as np
            local_tts = self._get_local_vieneu()
            full_data, full_sr = sf.read(prep_data["full_wav"])
            speaker_emb = local_tts.engine._ensure_speaker_encoder().embed(full_data, full_sr)
            emb_file = profile_folder / "speaker_emb.npy"
            np.save(emb_file, speaker_emb)
            print(f"[VoiceCloner] Đã trích xuất & lưu Speaker Embedding ({len(full_data)/full_sr:.1f}s) -> {emb_file.name}")
        except Exception as e_emb:
            print(f"[!] Không thể trích xuất speaker_emb tự động: {e_emb}")

        # Lưu sơ bộ để speak() có thể đọc profile
        profile_json = profile_folder / "profile.json"
        with open(profile_json, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        # 2. TẠO FILE GIỌNG ĐÃ ĐƯỢC CLONE ĐỌC CÂU CHÀO MẶC ĐỊNH (cloned_default_sample.mp3)
        cloned_default_mp3 = profile_folder / "cloned_default_sample.mp3"
        print(f"\n[Preview] Đang sinh giọng clone đọc câu chào mặc định: \"{DEFAULT_CLONED_GREETING}\"...")
        try:
            self.speak(
                profile_id=profile_id,
                new_script=DEFAULT_CLONED_GREETING,
                output_path=str(cloned_default_mp3),
                engine="omnivoice",
                master=True
            )
            meta["cloned_default_mp3"] = str(cloned_default_mp3.resolve())
        except Exception as e:
            print(f"[!] Không thể tự động tạo cloned_default_sample qua OmniVoice ({e}), fallback sang VieNeu...")
            try:
                self.speak(
                    profile_id=profile_id,
                    new_script=DEFAULT_CLONED_GREETING,
                    output_path=str(cloned_default_mp3),
                    engine="vieneu",
                    master=True
                )
                meta["cloned_default_mp3"] = str(cloned_default_mp3.resolve())
            except Exception as e2:
                print(f"[!] Không thể tạo cloned_default_sample: {e2}")

        # Đồng bộ sang output/ cho người dùng nghe ngay
        out_dir = Path(PROJECT_ROOT) / "output"
        out_dir.mkdir(parents=True, exist_ok=True)
        if source_preview_mp3.exists():
            shutil.copy2(source_preview_mp3, out_dir / f"{profile_id}_source_original_preview.mp3")
        if cloned_default_mp3.exists():
            shutil.copy2(cloned_default_mp3, out_dir / f"{profile_id}_cloned_default_sample.mp3")

        with open(profile_json, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        print(f"\n[+] ĐÃ LƯU PROFILE VÀ BỘ ĐÔI PREVIEW HOÀN TẤT: {profile_json}")
        print(f" • File Source Gốc : {source_preview_mp3}")
        print(f" • File Clone Mẫu : {cloned_default_mp3}")
        return meta

    def get_profile(self, profile_id: str) -> Dict[str, Any]:
        """Tải thông tin profile từ Kho Giọng (Voice Vault)."""
        profile_json = self.profiles_dir / profile_id / "profile.json"
        if not profile_json.exists():
            raise FileNotFoundError(f"Không tìm thấy Sound Profile '{profile_id}' trong Kho Giọng tại: {profile_json}")
        with open(profile_json, "r", encoding="utf-8") as f:
            return json.load(f)

    def speak(
        self,
        profile_id: str,
        new_script: str,
        output_path: str,
        engine: str = "omnivoice",
        master: bool = True,
        tempo_factor: float = 1.10
    ) -> str:
        """
        Sinh giọng nói đọc kịch bản mới bằng Sound Profile đã lưu.
        engine:
          - 'omnivoice': OmniVoice SOTA Zero-Shot Voice Cloner (Mặc định số 1, chạy MPS offline, độ giống cực cao).
          - 'vieneu': VieNeu-TTS v3 Turbo (chuyên tiếng Việt, tự nhiên, tròn thanh điệu).
          - 'seed_vc': Voice Conversion (đắp thanh quản thật lên giọng đọc cảm xúc).
          - 'f5_tts': F5-TTS Neural Diffusion Transformer.
          - 'edge_tts': Fallback giọng Hoài My nếu không có mạng.
        """
        meta = self.get_profile(profile_id)
        ref_audio = meta["ref_slice_wav"]
        ref_text = meta["transcript"]

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        temp_raw_wav = os.path.join(os.path.dirname(os.path.abspath(output_path)), f"_temp_raw_{profile_id}.wav")

        print(f"\n[VoiceCloner] Đang sinh giọng với Động cơ: {engine.upper()} (Tempo: {tempo_factor}x)...")
        print(f"-> Profile: {profile_id} ({meta.get('speaker_name', '')})")
        print(f"-> Mẫu âm thanh: {ref_audio}")
        print(f"-> Kịch bản mới: \"{new_script[:60]}...\"")

        success = False
        last_error = None

        # 0. THỬ NGHIỆM ĐỘNG CƠ OMNIVOICE (K2-FSA SOTA ZERO-SHOT CLONER)
        if engine == "omnivoice":
            try:
                from gobi.adapters.integrations.omnivoice_adapter import OmniVoiceAdapter
                adapter = OmniVoiceAdapter()
                profile_dir = self.profiles_dir / profile_id
                print(f"[OmniVoice] Đang sinh giọng clone qua OmniVoice SOTA Engine với profile: {profile_id}...")
                adapter.synthesize_from_profile(
                    profile_dir=str(profile_dir),
                    text=new_script,
                    output_wav=temp_raw_wav,
                    speed=1.0,
                    num_step=32,
                    denoise=True
                )
                success = True
                print(f"[+] Đã sinh âm thanh clone chuẩn xác qua OmniVoice Engine!")
            except Exception as e_omni:
                print(f"[!] OmniVoice gặp sự cố ({e_omni}), chuyển sang VieNeu...")
                last_error = e_omni
                engine = "vieneu"

        # 1. THỬ NGHIỆM ĐỘNG CƠ VIENEU-TTS V3 TURBO (MẶC ĐỊNH SỐ 1 CHO TIẾNG VIỆT)
        if engine == "vieneu":
            # 1.1 Thử nghiệm mô hình VieNeu-TTS Offline cục bộ (ONNX Lite CPU)
            try:
                import soundfile as sf
                import numpy as np
                local_tts = self._get_local_vieneu()

                emb_file = self.profiles_dir / profile_id / "speaker_emb.npy"
                if emb_file.exists():
                    print(f"[VieNeu-TTS] Sử dụng Speaker Embedding 30s độ nét cao: {emb_file.name}...")
                    speaker_emb = np.load(emb_file)
                    ref_audio_data, sr_ref = sf.read(ref_audio)
                    ref_codes = local_tts.engine._encode_ref_wav(ref_audio_data, sr_ref)
                    voice_dict = {
                        "speaker_emb": speaker_emb,
                        "codes": ref_codes
                    }
                    wav = local_tts.infer(
                        text=new_script,
                        voice=voice_dict,
                        temperature=0.6,
                        top_k=20,
                        top_p=0.9,
                        repetition_penalty=1.2,
                        silence_p=0.06,
                        max_chars=256
                    )
                else:
                    print(f"[VieNeu-TTS] Đang sinh giọng trực tiếp qua VieNeu Offline ONNX với mẫu tham chiếu: {ref_audio}...")
                    wav = local_tts.infer(
                        text=new_script,
                        ref_audio=ref_audio,
                        temperature=0.6,
                        top_k=20,
                        top_p=0.9,
                        repetition_penalty=1.2,
                        silence_p=0.06,
                        max_chars=256
                    )
                sf.write(temp_raw_wav, wav, local_tts.sample_rate)
                success = True
                print(f"[+] Đã sinh âm thanh clone chuẩn xác qua VieNeu-TTS v3 Turbo Offline!")
            except Exception as e_local:
                print(f"[!] VieNeu Offline gặp sự cố ({e_local}), chuyển sang kết nối Hugging Face...")
                try:
                    client = Client("pnnbao-ump/VieNeu-TTS-v3-Turbo", token=hf_token)
                    dialect_str = str(meta.get("dialect", "")).lower()
                    voice_name = "Thùy Dung" if "north" in dialect_str or "bắc" in dialect_str else "Trúc Ly"
                    res = client.predict(
                        text=new_script,
                        voice=voice_name,
                        ref_audio=handle_file(ref_audio),
                        temperature=0.75,
                        top_k=25,
                        top_p=0.95,
                        repetition_penalty=1.2,
                        max_new_frames=500,
                        max_chars=350,
                        api_name="/synthesize"
                    )
                    src = res[0] if isinstance(res, (list, tuple)) else res
                    shutil.copy2(src, temp_raw_wav)
                    success = True
                except Exception as e:
                    print(f"[!] VieNeu-TTS gặp sự cố: {e}. Đang tự động chuyển sang Seed-VC...")
                    last_error = e
                    engine = "seed_vc"

        # 2. THỬ NGHIỆM ĐỘNG CƠ SEED-VC (VOICE CONVERSION TRÁO THANH QUẢN)
        if engine == "seed_vc" and not success:
            try:
                # Bước 2.1: Sinh giọng phát âm chuẩn tiếng Việt từ Edge-TTS làm bệ đỡ
                import asyncio
                import edge_tts
                base_wav = os.path.join(os.path.dirname(os.path.abspath(output_path)), f"_temp_base_edge_{profile_id}.wav")
                tts_voice = "vi-VN-HoaiMyNeural" if meta.get("dialect") == "north" else "vi-VN-NamMinhNeural"
                
                async def _gen_base():
                    comm = edge_tts.Communicate(new_script, voice=tts_voice, rate="+5%")
                    await comm.save(base_wav)
                asyncio.run(_gen_base())

                # Bước 2.2: Dùng Seed-VC đổi timbre sang người thật
                client_vc = Client("Plachta/Seed-VC", token=hf_token)
                res_vc = client_vc.predict(
                    source_audio_path=handle_file(base_wav),
                    target_audio_path=handle_file(ref_audio),
                    diffusion_steps=30,
                    length_adjust=0.97,
                    inference_cfg_rate=0.75,
                    f0_condition=False,
                    auto_f0_adjust=True,
                    pitch_shift=0,
                    api_name="/predict_1"
                )
                src_vc = res_vc[1] if isinstance(res_vc, (list, tuple)) and len(res_vc) > 1 else res_vc[0]
                shutil.copy2(src_vc, temp_raw_wav)
                if os.path.exists(base_wav):
                    os.remove(base_wav)
                success = True
            except Exception as e:
                print(f"[!] Seed-VC gặp sự cố: {e}. Đang tự động chuyển sang F5-TTS...")
                last_error = e
                engine = "f5_tts"

        # 3. THỬ NGHIỆM ĐỘNG CƠ F5-TTS
        if engine == "f5_tts" and not success:
            try:
                client_f5 = Client("mrfakename/E2-F5-TTS", token=hf_token)
                res_f5 = client_f5.predict(
                    ref_audio=handle_file(ref_audio),
                    ref_text=ref_text,
                    gen_text=new_script,
                    remove_silence=True,
                    api_name="/predict"
                )
                src_f5 = res_f5[0] if isinstance(res_f5, (list, tuple)) else res_f5
                shutil.copy2(src_f5, temp_raw_wav)
                success = True
            except Exception as e:
                print(f"[!] F5-TTS gặp sự cố: {e}. Kích hoạt chế độ cứu cánh Edge-TTS Neural...")
                last_error = e
                engine = "edge_tts"

        # 4. CỨU CÁNH CUỐI CÙNG: EDGE-TTS NEURAL LOCAL
        if not success:
            import asyncio
            import edge_tts
            tts_voice = "vi-VN-HoaiMyNeural" if meta.get("dialect") == "north" else "vi-VN-NamMinhNeural"
            async def _gen_fallback():
                comm = edge_tts.Communicate(new_script, voice=tts_voice, rate="+6%", pitch="+2Hz")
                await comm.save(temp_raw_wav)
            asyncio.run(_gen_fallback())
            print(f"[+] Đã sinh âm thanh dự phòng chất lượng cao qua Edge-TTS Hoài My!")

        # 5. CHẠY MASTERING HẬU KỲ CHUẨN TIKTOK KOC (-14 LUFS)
        if master:
            print("[Mastering] Đang chạy chuỗi Mastering TikTok KOC Action (-14 LUFS, Presence EQ, De-Esser)...")
            self.mastering.master_tiktok_koc(
                input_audio_path=temp_raw_wav,
                output_audio_path=output_path,
                target_lufs=-14.0,
                presence_boost_db=1.2,
                tempo_factor=tempo_factor
            )
        else:
            shutil.copy2(temp_raw_wav, output_path)

        if os.path.exists(temp_raw_wav):
            os.remove(temp_raw_wav)

        print(f"\n[THÀNH CÔNG] File âm thanh Clone đã sẵn sàng tại:")
        print(f"-> {os.path.abspath(output_path)} ({os.path.getsize(output_path):,} bytes)")
        return os.path.abspath(output_path)

    def clone_and_speak(
        self,
        media_path: str,
        new_script: str,
        output_path: str,
        profile_id: Optional[str] = None,
        dialect: str = "north",
        engine: str = "omnivoice"
    ) -> str:
        """
        Quy trình 1 chạm từ A-Z:
        Input video/mp3 -> Tạo profile -> Sinh kịch bản mới -> Master chuẩn TikTok.
        """
        if not profile_id:
            profile_id = Path(media_path).stem.replace(" ", "_").lower()
            
        self.create_profile(media_path=media_path, profile_id=profile_id, dialect=dialect)
        return self.speak(profile_id=profile_id, new_script=new_script, output_path=output_path, engine=engine)
