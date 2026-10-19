import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Test prompt
prompt = "A beautiful young Vietnamese woman standing in a cozy cafe, smiling warmly, holding a stylish knit cardigan and showing it to the camera. Smooth natural movements, blinking, gentle breathing, photorealistic, cinematic lighting."

print("Initiating Veo video generation test...")
try:
    operation = client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            aspect_ratio="9:16",
            duration_seconds=5,
            person_generation="allow_adult"
        )
    )
    print("Operation started:", operation.name)
    
    # Poll operation until done
    while not operation.done:
        print("Waiting for Veo video generation... (sleeping 10s)")
        time.sleep(10)
        operation = client.operations.get(operation)
        
    print("Operation completed!")
    if operation.error:
        print("Error from operation:", operation.error)
    else:
        print("Result:", operation.result)
        # Download generated video
        video = operation.result.generated_videos[0]
        with open("veo_test_output.mp4", "wb") as f:
            f.write(video.video.video_bytes)
        print("Saved veo_test_output.mp4 successfully!")

except Exception as e:
    print("Veo generation call error:", type(e), e)
