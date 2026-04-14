import os
import yt_dlp
import requests
from config import INPUT_DIR, REDDIT_HEADERS


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


def download_image(job_id: str, image_url: str) -> str:
    output_dir = os.path.join(INPUT_DIR, job_id)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "image.jpg")

    response = requests.get(image_url, headers=REDDIT_HEADERS, stream=True)

    #print("Status:", response.status_code)
    #print("Content-Type:", response.headers.get("Content-Type"))

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

    if not image_url.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")):
        raise Exception(f"URL does not appear to be an image: {image_url}")

    return output_path


def download_gallery(job_id: str, image_urls: list[str]) -> list:
    output_dir = os.path.join(INPUT_DIR, job_id, "gallery")
    os.makedirs(output_dir, exist_ok=True)

    saved_paths = []

    for idx, url in enumerate(image_urls, start=1):
        ext = ".jpg"
        if ".png" in url.lower():
            ext = ".png"
        elif ".webp" in url.lower():
            ext = ".webp"
        elif ".gif" in url.lower():
            ext = ".gif"

        filename = f"image_{idx}{ext}"
        saved_path = download_image(job_id, url, filename=filename)
        saved_paths.append(saved_path)

    return output_dir