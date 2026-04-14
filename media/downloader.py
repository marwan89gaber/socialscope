import os
import yt_dlp
from config import INPUT_DIR


def download_video(job_id: str, video_url: str) -> str:
    output_dir = os.path.join(INPUT_DIR, job_id)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "video.mp4")

    ydl_opts = {
        "outtmpl": output_path,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "quiet": False,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    if not os.path.exists(output_path):
        raise Exception(f"Download appeared to succeed but file not found at: {output_path}")

    return output_path