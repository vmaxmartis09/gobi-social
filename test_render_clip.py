import os
import sys
import json
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# Font configurations
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REGULAR = "C:/Windows/Fonts/arial.ttf"

font_badge = ImageFont.truetype(FONT_BOLD, 36)
font_title = ImageFont.truetype(FONT_BOLD, 68)
font_sub = ImageFont.truetype(FONT_BOLD, 46)

def create_rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)

def render_scene_clip(scene, out_path, fps=30):
    duration = scene['duration']
    total_frames = int(duration * fps)
    w, h = 1080, 1920
    
    # Load and prepare base image
    img = Image.open(scene['image']).convert('RGB')
    
    # Target aspect ratio 9:16
    img_w, img_h = img.size
    target_ratio = w / h
    img_ratio = img_w / img_h
    
    if img_ratio > target_ratio:
        # Image is wider -> crop sides
        new_w = int(img_h * target_ratio)
        offset = (img_w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, img_h))
    else:
        # Image is taller -> crop top/bottom
        new_h = int(img_w / target_ratio)
        offset = (img_h - new_h) // 2
        img = img.crop((0, offset, img_w, offset + new_h))
        
    img = img.resize((w, h), Image.Resampling.LANCZOS)
    
    # Start ffmpeg process for streaming raw video frames
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{w}x{h}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", f"assets/audio/{scene['id']}.mp3",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_path
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    # Pre-render static overlay elements to speed up rendering
    badge_text = scene.get('badge', '🔥 HOT')
    title_text = scene.get('hook_title', '')
    sub1 = scene.get('subtitle_1', '')
    sub2 = scene.get('subtitle_2', '')
    
    # Animation loop
    for i in range(total_frames):
        progress = i / total_frames
        
        # Ken Burns effect: Zoom in slightly from 1.0 to 1.12
        scale = 1.0 + 0.12 * progress
        scaled_w = int(w * scale)
        scaled_h = int(h * scale)
        
        # Crop centered
        scaled_img = img.resize((scaled_w, scaled_h), Image.Resampling.BILINEAR)
        crop_x = (scaled_w - w) // 2
        crop_y = (scaled_h - h) // 2
        frame = scaled_img.crop((crop_x, crop_y, crop_x + w, crop_y + h))
        
        # Draw darkened vignettes and UI overlays
        draw = ImageDraw.Draw(frame, 'RGBA')
        
        # Top gradient shadow for badge & headline readability
        draw.rectangle([0, 0, w, 400], fill=(0, 0, 0, 140))
        # Bottom gradient shadow for subtitle readability
        draw.rectangle([0, h - 550, w, h], fill=(0, 0, 0, 160))
        
        # 1. Category Pill Badge at Top
        badge_bbox = font_badge.getbbox(badge_text)
        badge_w = badge_bbox[2] - badge_bbox[0] + 50
        badge_h = 60
        badge_x = (w - badge_w) // 2
        badge_y = 120
        create_rounded_rect(draw, [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], 30, (230, 30, 60, 230))
        draw.text((badge_x + 25, badge_y + 8), badge_text, font=font_badge, fill=(255, 255, 255, 255))
        
        # 2. Main Hook Headline
        title_bbox = font_title.getbbox(title_text)
        title_w = title_bbox[2] - title_bbox[0]
        title_x = (w - title_w) // 2
        title_y = 210
        # Shadow
        draw.text((title_x + 3, title_y + 3), title_text, font=font_title, fill=(0, 0, 0, 220))
        # Text
        draw.text((title_x, title_y), title_text, font=font_title, fill=(255, 220, 0, 255)) # Vibrant Gold
        
        # 3. Dynamic Subtitles at Bottom
        current_sub = sub1 if progress < 0.52 else sub2
        sub_bbox = font_sub.getbbox(current_sub)
        sub_w = sub_bbox[2] - sub_bbox[0] + 60
        sub_h = 90
        sub_x = (w - sub_w) // 2
        sub_y = h - 350
        
        # Subtitle box backdrop (dark rounded pill with neon border)
        create_rounded_rect(draw, [sub_x, sub_y, sub_x + sub_w, sub_y + sub_h], 24, (15, 23, 42, 235))
        # Neon highlight stroke
        draw.rounded_rectangle([sub_x, sub_y, sub_x + sub_w, sub_y + sub_h], radius=24, outline=(255, 215, 0, 220), width=3)
        
        # Subtitle text
        text_inner_x = sub_x + 30
        text_inner_y = sub_y + 18
        draw.text((text_inner_x, text_inner_y), current_sub, font=font_sub, fill=(255, 255, 255, 255))
        
        # 4. Animated Progress Line at the very bottom
        line_w = int(w * progress)
        draw.rectangle([0, h - 16, line_w, h], fill=(255, 50, 100, 255))
        
        # Convert to bytes and pipe to ffmpeg
        proc.stdin.write(frame.tobytes())
        
        if (i + 1) % 50 == 0 or i == total_frames - 1:
            print(f"Rendered frame {i+1}/{total_frames} ({int((i+1)/total_frames*100)}%)")
            
    proc.stdin.close()
    proc.wait()
    print(f"Clip saved: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == '__main__':
    with open('scenes_config.json', 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    os.makedirs('temp_clips', exist_ok=True)
    print("Testing rendering clip 1...")
    render_scene_clip(scenes[0], 'temp_clips/scene1.mp4')
