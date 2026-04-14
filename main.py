import os
import json
from datetime import datetime

from config import OUTPUTS_DIR
from platforms import fetch_reddit_post
from storage import init_db, create_job, update_job_status, job_exists
from utils import detect_platform, is_valid_url, is_reachable
from media import download_video, download_image,  extract_frames, extract_audio, transcribe_audio


def process_link(url: str):

    print("--- Social Lens ---")

    # Step 1 — validate
    if not is_valid_url(url):
        print("Invalid URL. Please enter a proper link.")
        return

    # Step 2 — detect platform
    platform = detect_platform(url)
    if platform == "unsupported":
        print("This platform is not supported yet.")
        return

    print(f"Platform detected: {platform}")

    # Step 3 — reachability
    print("Checking if the post is reachable...")
    if not is_reachable(url):
        print("Could not reach this URL. It may be private or deleted.")
        return

    # Step 4 — deduplication and creating job
    existing_job_id = job_exists(url)
    if existing_job_id:
        print(f"This link was already submitted. Job ID: {existing_job_id}")
        job_id = existing_job_id
    
    else:
        job_id = create_job(url, platform)
        print(f"Job created. ID: {job_id}")

    # Step 5 — fetch post data
    update_job_status(job_id, "fetching")
    print("Fetching post data...")

    try:
        if platform == "reddit":
            post = fetch_reddit_post(url)
        else:
            raise Exception("No fetcher available for this platform")
    except Exception as e:
        update_job_status(job_id, "failed", error=str(e))
        print(f"Failed to fetch post: {e}")
        return

    # Step 6 — mark done and save output
    update_job_status(job_id, "fetched")

    """output = {
        "job_id":    job_id,
        "url":       url,
        "platform":  platform,
        "fetched_at": datetime.utcnow().isoformat(),
        "post":      post
    }

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUTS_DIR, f"{job_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Done. Output saved to: {output_path}")
    print(f"\nPost title: {post['title']}")
    print(f"Author:     {post['author']}")
    print(f"Subreddit:  r/{post['subreddit']}")
    print(f"Type:       {post['content_type']}")
    print(f"Score:      {post['score']}")"""

    media = {}

    if post["content_type"] == "video":
        print("Video post detected — starting media pipeline...")

        try:
            update_job_status(job_id, "downloading_video")
            video_path = download_video(job_id, post["url"])
            print(f"Video saved: {video_path}")

            update_job_status(job_id, "extracting_frames")
            frames_dir = extract_frames(job_id, video_path)

            update_job_status(job_id, "extracting_audio")
            audio_path = extract_audio(job_id, video_path)

            update_job_status(job_id, "transcribing")
            transcript = transcribe_audio(audio_path)
            print(f"Transcript: {transcript['text'][:120]}...")

            media = {
                "video_path":  video_path,
                "frames_dir":  frames_dir,
                "audio_path":  audio_path,
                "transcript":  transcript,
            }

        except Exception as e:
            update_job_status(job_id, "failed", error=str(e))
            print(f"Media pipeline failed: {e}")
            return
        
    elif post["content_type"] == "image":
        print("Image post detected — saving as image...")

        try:
            update_job_status(job_id, "downloading_image")
            frames_dir = download_image(job_id, post["url"])

            media = {
                "frames_dir": frames_dir,
            }

        except Exception as e:
            update_job_status(job_id, "failed", error=str(e))
            print(f"Image download failed: {e}")
            return

        

    # Final output with media info
    update_job_status(job_id, "done")

    output = {
        "job_id":     job_id,
        "url":        url,
        "platform":   platform,
        "fetched_at": datetime.utcnow().isoformat(),
        "post":       post,
        "media":      media,
    }

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUTS_DIR, f"{job_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Output saved to: {output_path}")
    print(f"Post title: {post['title']}")
    print(f"Author:     {post['author']}")
    print(f"Type:       {post['content_type']}")
    if media.get("transcript"):
        print(f"Transcript: {media['transcript']['text'][:100]}...")



if __name__ == "__main__":
    init_db()
    url = input("Paste a link: ").strip()
    process_link(url)