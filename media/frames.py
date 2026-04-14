import os
import ffmpeg
from config import INPUT_DIR


def extract_frames(job_id: str, video_path: str, fps: float = 0.5) -> str:
    frames_dir = os.path.join(INPUT_DIR, job_id, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    output_pattern = os.path.join(frames_dir, "frame_%04d.jpg")

    try:
        (
            ffmpeg
            .input(video_path)
            .filter("fps", fps=fps)
            .output(output_pattern, qscale=2)
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        raise Exception(f"FFmpeg frame extraction failed: {e.stderr.decode()}")

    extracted = sorted(os.listdir(frames_dir))
    if len(extracted) == 0:
        raise Exception("Frame extraction produced no output files.")
    if len(extracted) < 3:
        print(f"Warning: Only {len(extracted)} frame(s) extracted - video may be very short.")

    print(f"Extracted {len(extracted)} frames to: {frames_dir}")
    return frames_dir
