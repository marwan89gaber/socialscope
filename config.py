import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
INPUT_DIR = os.path.join(BASE_DIR, "inputs")

DATABASE_PATH = os.path.join(DATA_DIR, "social_lens.db")

SUPPORTED_PLATFORMS = ["reddit"]

REDDIT_CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME      = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD      = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT    = os.getenv("REDDIT_USER_AGENT", "social-lens/0.1 by Few-Yam-3637")

REDDIT_HEADERS = {
    "User-Agent": REDDIT_USER_AGENT
}