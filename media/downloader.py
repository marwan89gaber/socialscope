import os
import yt_dlp
import requests
from config import INPUT_DIR, REDDIT_HEADERS
from .frames import extract_gif


def download_video(job_id: str, video_url: str) -> str:
    output_dir = os.path.join(INPUT_DIR, job_id)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "video.mp4")

    ydl_opts = {
        "outtmpl": output_path,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    if not os.path.exists(output_path):
        raise Exception(f"Download appeared to succeed but file not found at: {output_path}")

    return output_path


def download_image(job_id: str, image_url: str, filename: str = "image.jpg") -> str:
    output_dir = os.path.join(INPUT_DIR, job_id)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, filename)

    response = requests.get(image_url, headers=REDDIT_HEADERS, stream=True)

    if response.status_code != 200:
        raise Exception(f"Failed to download image: {response.status_code}")
    if "image" not in response.headers.get("Content-Type", ""):
        raise Exception(f"URL did not return an image content type: {response.headers.get('Content-Type')}")
    
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(1024):
            if chunk:  
                f.write(chunk)

    #size = os.path.getsize(output_path)
    #print("Saved file size:", size)

    return output_path


def download_gallery(job_id: str, image_urls: list[str]) -> list[dict]:
    
    saved_paths = []

    for idx, url in enumerate(image_urls, start=1):
        if ".gif" in url.lower():
            print(f"GIF detected in gallery ({idx})")

            gif_path = download_gif(job_id, url)
            frames_dir = extract_gif(gif_path)

            saved_paths.append({
                "type": "gif",
                "frames_dir": frames_dir
            })
        else:
            ext = ".jpg"
            if ".png" in url.lower():
                ext = ".png"
            elif ".webp" in url.lower():
                ext = ".webp"

            filename = f"image_{idx}{ext}"
            path = download_image(job_id, url, filename=filename)
            saved_paths.append({
                "type": "image",
                "path": path
            })

    return saved_paths

def download_gif(job_id: str, gif_url: str) -> str:
    output_dir = os.path.join(INPUT_DIR, job_id)
    os.makedirs(output_dir, exist_ok=True)

    gif_path = os.path.join(output_dir, "input.gif")

    response = requests.get(gif_url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download GIF: {response.status_code}")

    with open(gif_path, "wb") as f:
        for chunk in response.iter_content(1024):
            if chunk:
                f.write(chunk)

    return gif_path
