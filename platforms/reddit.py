import requests
from config import REDDIT_HEADERS


def fetch_reddit_post(url: str) -> dict:
    json_url = url.rstrip("/") + ".json"

    response = requests.get(json_url, headers=REDDIT_HEADERS, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Reddit returned status {response.status_code}")

    data = response.json()

    post_data = data[0]["data"]["children"][0]["data"]

    return {
        "title":      post_data.get("title", ""),
        "text":       post_data.get("selftext", ""),
        "author":     post_data.get("author", ""),
        "subreddit":  post_data.get("subreddit", ""),
        "url":        post_data.get("url", ""),
        "created_utc": post_data.get("created_utc", None),
        "score":      post_data.get("score", 0),
    }