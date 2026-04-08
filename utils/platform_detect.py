from urllib.parse import urlparse

PLATFORM_PATTERNS = {
    "reddit": ["reddit.com", "www.reddit.com", "old.reddit.com"],
}

def detect_platform(url: str) -> str:
    try:
        hostname = urlparse(url).netloc.lower()
        for platform, domains in PLATFORM_PATTERNS.items():
            if hostname in domains:
                return platform
        return "unsupported"
    except Exception:
        return "unsupported"