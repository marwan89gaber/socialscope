import os
import ffmpeg
import requests
from datetime import datetime
from PIL import Image
from config import INPUT_DIR


def extract_frames(job_id: str, video_path: str, fps: float = 1.0) -> str:
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


def extract_gif(gif_path: str, fps: float = 1.0) -> str:
    output_dir = os.path.dirname(gif_path)
    frame_interval_ms = 1000 // fps

    with Image.open(gif_path) as im:
        frame_index = 0
        saved_index = 0
        accumulated_time = 0

        try:
            while True:
                duration = im.info.get("duration", 100)
                accumulated_time += duration

                if accumulated_time >= frame_interval_ms:
                    frame = im.convert("RGB")
                    frame_path = os.path.join(output_dir, f"frame_{saved_index:03d}.jpg")
                    frame.save(frame_path, "JPEG")

                    saved_index += 1
                    accumulated_time = 0

                frame_index += 1
                im.seek(frame_index)

        except EOFError:
            pass

    return output_dir

#def ask_for_fps() -> float:
    while True:
        try:
            fps_input = input("Enter desired FPS for extraction (default is 1): ").strip()
            if fps_input == "":
                return 1.0
            fps = float(fps_input)
            if fps <= 0:
                print("FPS must be a positive number. Please try again.")
                continue
            return fps
        except ValueError:
            print("Invalid input. Please enter a numeric value for FPS.")