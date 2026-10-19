import os
import sys
import shutil
from gradio_client import Client, handle_file

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ref_audio = os.path.abspath("assets/cloned_voices/koc_neil_girl/reference_voice.wav")
ref_text = "Còn một em áo thun vừa thời trang lại vừa rất là nhiều công năng cho mấy bà luôn nha. Chất thì rất là co giãn đàn hồi, mặc nó thoải mái lắm luôn ý."
gen_text = "Mấy bà ơi, hôm nay em lên tiếp một mã áo thun chống nắng siêu đỉnh cho mùa hè này nhé! Nhanh tay bấm giỏ hàng kẻo hết size nha!"

print("Connecting to Neural F5-TTS Zero-Shot Voice Clone Server...")
client = Client("mrfakename/E2-F5-TTS")

print("Sending reference voice from mau-voice.mp4 to clone...")
print(f"Ref Audio: {ref_audio}")
print(f"Gen Text: {gen_text}")

try:
    result = client.predict(
        ref_audio=handle_file(ref_audio),
        ref_text=ref_text,
        gen_text=gen_text,
        remove_silence=True,
        api_name="/predict"
    )
    print("Voice Clone Inference Result:", result)
    
    # Copy result to output
    out_dest = os.path.abspath("output/true_neural_cloned_voice.wav")
    if isinstance(result, tuple) or isinstance(result, list):
        src_path = result[0]
    else:
        src_path = result
        
    shutil.copy2(src_path, out_dest)
    print(f"SUCCESS! True neural cloned voice saved to: {out_dest}")
    print(f"File size: {os.path.getsize(out_dest):,} bytes")
    
except Exception as e:
    print("Error during inference:", e)
