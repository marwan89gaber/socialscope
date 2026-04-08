import os
import json
from datetime import datetime

from config import OUTPUTS_DIR
from platforms import fetch_reddit_post
from storage import init_db, create_job, update_job_status, job_exists
from utils import detect_platform, is_valid_url, is_reachable


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

    # Step 4 — deduplication
    existing_job_id = job_exists(url)
    if existing_job_id:
        print(f"This link was already submitted. Job ID: {existing_job_id}")
        return

    # Step 5 — create job
    job_id = create_job(url, platform)
    print(f"Job created. ID: {job_id}")

    # Step 6 — fetch post data
    update_job_status(job_id, "downloading")
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

    # Step 7 — mark done and save output
    update_job_status(job_id, "done")

    output = {
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


if __name__ == "__main__":
    init_db()
    url = input("Paste a link: ").strip()
    process_link(url)

#if __name__ == "__main__":
#    URL1 = "https://reddit.com/r/learnprogramming/comments/14abcde/sample_post/"
#    URL2 = "https://www.reddit.com/r/Python/comments/15m8z9/example_post_title/"
#    URL3 = "https://www.reddit.com/r/Python/comments/invalid123456789/"
#    URL4 = "http://www.reddit.com/r/Python/comments/15m8z9/example_post_title/"
#    URL5 = "https://twitter.com/somepost"
#    URL6 = "https://m.reddit.com/r/Python/comments/15m8z9/example_post_title/"   
#    print("reading URL4")
#    print(is_valid_url(URL4))
#    print(is_reachable(URL4))
#    print(detect_platform(URL4))#