import os
import ffmpeg
from config import INPUT_DIR


def extract_audio(job_id: str, video_path: str) -> str:
    output_dir = os.path.join(INPUT_DIR, job_id)
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, "audio.wav")

    try:
        (
            ffmpeg
            .input(video_path)
            .output(
                audio_path,
                map="0:a",         # audio stream only
                acodec="pcm_s16le", # uncompressed WAV — safest for Whisper
                ar=16000,           # 16kHz sample rate — what Whisper expects
                ac=1,               # mono
            )
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        raise Exception(f"FFmpeg audio extraction failed: {e.stderr.decode()}")

    if not os.path.exists(audio_path):
        raise Exception("Audio extraction produced no output file.")

    return audio_path