import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

DATABASE_PATH = os.path.join(DATA_DIR, "social_lens.db")

SUPPORTED_PLATFORMS = ["reddit"]

REDDIT_HEADERS = {
    "User-Agent": "social-lens/0.1"
}