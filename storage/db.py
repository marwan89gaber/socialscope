import os
import sqlite3
import uuid
from datetime import datetime
from config import DATABASE_PATH


def get_connection():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)



def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id      TEXT PRIMARY KEY,
            url         TEXT NOT NULL,
            platform    TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'queued',
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL,
            error       TEXT,
            result_id   TEXT
        )
    """)
    conn.commit()
    conn.close()


def create_job(url: str, platform: str) -> str:
    job_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO jobs (job_id, url, platform, status, created_at, updated_at)
        VALUES (?, ?, ?, 'queued', ?, ?)
    """, (job_id, url, platform, now, now))
    conn.commit()
    conn.close()
    return job_id


def update_job_status(job_id: str, status: str, error: str = None):
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE jobs SET status = ?, updated_at = ?, error = ?
        WHERE job_id = ?
    """, (status, now, error, job_id))
    conn.commit()
    conn.close()


def get_job(job_id: str) -> dict:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def job_exists(url: str) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT job_id FROM jobs WHERE url = ?", (url,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_status(job_id: str) -> str:
    job = get_job(job_id)
    return job["status"] if job else "not found"