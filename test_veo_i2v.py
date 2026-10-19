import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Use sample image
img_path = r"c:\Users\HAI\OneDrive\Tài liệu\vmax\affiliate_tiktok\sample_video\images\01_hook_model_cafe.jpg"
image_input = types.Image.from_file(location=img_path)

prompt = "A young beautiful Asian woman smiling warmly, gently moving her head and blinking naturally, smooth continuous motion, high quality, photorealistic."

print("Starting Veo 3.1 Fast Image-to-Video generation...")
try:
    operation = client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        prompt=prompt,
        image=image_input,
        config=types.GenerateVideosConfig(
            aspect_ratio="9:16",
            duration_seconds=4,
            person_generation="allow_adult"
        )
    )
    print("Operation started successfully! Name:", operation.name)
    
    poll_count = 0
    while not operation.done:
        poll_count += 1
        print(f"Waiting for Veo video... poll {poll_count} (sleeping 10s)")
        time.sleep(10)
        operation = client.operations.get(operation)
        
    print("Operation done!")
    if operation.error:
        print("Operation error:", operation.error)
    else:
        print("Generated videos count:", len(operation.result.generated_videos))
        video_obj = operation.result.generated_videos[0]
        out_file = "veo_generated_scene1.mp4"
        # Check how to get video bytes
        if hasattr(video_obj.video, "video_bytes") and video_obj.video.video_bytes:
            with open(out_file, "wb") as f:
                f.write(video_obj.video.video_bytes)
        elif hasattr(video_obj.video, "uri") and video_obj.video.uri:
            print("Video URI:", video_obj.video.uri)
            # download via client or urllib
            import urllib.request
            req = urllib.request.Request(video_obj.video.uri, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as r, open(out_file, "wb") as f:
                f.write(r.read())
        print(f"🎉 Saved {out_file} successfully! Size: {os.path.getsize(out_file)} bytes")

except Exception as e:
    print("Veo I2V Error:", type(e), e)
