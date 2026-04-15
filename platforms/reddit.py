import requests
from urllib.parse import urlparse, urlunparse
from config import REDDIT_HEADERS

def resolve_reddit_url(url: str) -> str | None:
    if "/s/" in url:
        try:
            response = requests.head(
                url,
                headers=REDDIT_HEADERS,
                allow_redirects=True,
                timeout=10,
            )
            if response.status_code != 200:
                print(f"Short link resolved with status {response.status_code}")
                return None
            url = response.url
        except requests.RequestException as e:
            print(f"Failed to resolve short link: {e}")
            return None

    parsed = urlparse(url)
    clean_path = parsed.path.rstrip("/") + "/.json"

    clean_url = urlunparse((
        "https",
        "old.reddit.com",
        clean_path,
        "",
        "",
        "",
    ))

    return clean_url

def extract_gallery_urls(post_data: dict) -> list[str]:
    image_urls = []

    gallery_data = post_data.get("gallery_data", {})
    media_metadata = post_data.get("media_metadata", {})

    for item in gallery_data.get("items", []):
        media_id = item.get("media_id")
        media = media_metadata.get(media_id, {})

        if media.get("e") == "Image":
            url = media.get("s", {}).get("u")
            if url:
                url = url.replace("&amp;", "&")
                image_urls.append(url)

    return image_urls

def fetch_reddit_post(url: str) -> dict:
    json_url = resolve_reddit_url(url)

    if json_url is None:
        raise Exception("Could not build a valid JSON endpoint from this URL.")

    print(f"Fetching: {json_url}")

    try:
        response = requests.get(json_url, headers=REDDIT_HEADERS, timeout=10)
    except requests.RequestException as e:
        raise Exception(f"Network error: {e}")

    if response.status_code != 200:
        raise Exception(f"Reddit returned status {response.status_code}")

    content_type = response.headers.get("Content-Type", "")
    if "application/json" not in content_type:
        raise Exception(f"Expected JSON but got {content_type}. Post may be deleted or private.")

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"Failed to parse response as JSON: {e}")

    post_data = data[0]["data"]["children"][0]["data"]

    is_video = post_data.get("is_video", False)
    is_gallery = post_data.get("is_gallery", False)
    has_gallery_data = "gallery_data" in post_data

    url_value = post_data.get("url", "")

    if is_video:
        content_type = "video"
    elif is_gallery or (has_gallery_data and url_value.endswith("/gallery/")):
        content_type = "gallery"
    elif url_value.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
        content_type = "image"
    elif post_data.get("selftext", "").strip():
        content_type = "text"
    else:
        content_type = "link"

    gallery_urls = extract_gallery_urls(post_data) if is_gallery else []

    return {
        "title":        post_data.get("title", ""),
        "text":         post_data.get("selftext", ""),
        "author":       post_data.get("author", ""),
        "subreddit":    post_data.get("subreddit", ""),
        "url":          url_value,
        "created_utc":  post_data.get("created_utc", None),
        "score":        post_data.get("score", 0),
        "content_type": content_type,
        "is_video":     is_video,
        "is_gallery":   is_gallery,
        "gallery_urls": gallery_urls,
    }
