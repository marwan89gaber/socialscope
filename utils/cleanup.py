import os
import shutil

from config import INPUT_DIR, OUTPUTS_DIR, DATABASE_PATH


def cleanup_inputs():
    """Delete all downloaded media in inputs/ but keep the folder."""
    if os.path.exists(INPUT_DIR):
        for item in os.listdir(INPUT_DIR):
            item_path = os.path.join(INPUT_DIR, item)
            if item == ".gitkeep":
                continue
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        print("Inputs cleared.")
    else:
        print("Inputs folder not found — nothing to clear.")


def cleanup_outputs():
    """Delete all JSON output files in outputs/ but keep the folder."""
    if os.path.exists(OUTPUTS_DIR):
        for item in os.listdir(OUTPUTS_DIR):
            if item == ".gitkeep":
                continue
            item_path = os.path.join(OUTPUTS_DIR, item)
            os.remove(item_path)
        print("Outputs cleared.")
    else:
        print("Outputs folder not found — nothing to clear.")


def cleanup_database():
    """Delete the SQLite database file entirely."""
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print("Database deleted.")
    else:
        print("Database not found — nothing to delete.")


def cleanup_pycache(root: str = None):
    """
    Recursively delete all __pycache__ folders under the project root.
    Defaults to the directory containing this file's parent (i.e. the project root).
    """
    if root is None:
        # this file lives at utils/cleanup.py, so go one level up
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 
    deleted = 0
    for dirpath, dirnames, _ in os.walk(root):
        if "__pycache__" in dirnames:
            cache_path = os.path.join(dirpath, "__pycache__")
            shutil.rmtree(cache_path)
            deleted += 1
            dirnames.remove("__pycache__")  # prevent os.walk from trying to recurse into it
 
    if deleted:
        print(f"Cleared {deleted} __pycache__ folder(s).")
    else:
        print("No __pycache__ folders found.")



def cleanup_all(include_whisper_cache: bool = False):
    """
    Full reset: inputs, outputs, database, and optionally the Whisper model cache.
    The Whisper cache is excluded by default because re-downloading the model
    takes time and bandwidth — only pass True if you explicitly want that.
    """
    print("--- Starting full cleanup ---")
    cleanup_inputs()
    cleanup_outputs()
    cleanup_database()
    cleanup_pycache()
    print("--- Cleanup complete ---")


if __name__ == "__main__":
    cleanup_all()