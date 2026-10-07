import os
from typing import Any, Dict, List, Optional

import whisper
import torch

from config import OUTPUTS_DIR

_model_cache = {}


def transcribe_audio(audio_path: str, model_size: str = "base") -> dict:
    if model_size not in _model_cache:
        print(f"Loading Whisper model: {model_size}")
        _model_cache[model_size] = whisper.load_model(model_size)

    model = _model_cache[model_size]

    print("Transcribing audio...")
    fp16 = torch.cuda.is_available()
    result = model.transcribe(audio_path, fp16=fp16)

    return {
        "text":     result["text"].strip(),
        "language": result.get("language", "unknown"),
        "segments": [
            {
                "start": round(seg["start"], 2),
                "end":   round(seg["end"],   2),
                "text":  seg["text"].strip(),
            }
            for seg in result.get("segments", [])
        ],
    }


def _format_segments_as_captions(segments: List[Dict[str, Any]]) -> str:
    lines = []

    for segment in segments:
        start = segment.get("start", 0.0)
        end = segment.get("end", 0.0)
        text = segment.get("text", "").strip()
        lines.append(f"[{start:0>8.2f} --> {end:0>8.2f}] {text}")

    return "\n".join(lines).strip() + ("\n" if lines else "")


def transcribe_video_to_txt(video_path: str, model_size: str = "base", output_txt_path: Optional[str] = None) -> str:
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    transcript = transcribe_audio(video_path, model_size=model_size)

    if output_txt_path is None:
        os.makedirs(OUTPUTS_DIR, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_txt_path = os.path.join(OUTPUTS_DIR, f"{base_name}_cc.txt")

    with open(output_txt_path, "w", encoding="utf-8") as file:
        file.write(f"Source: {video_path}\n")
        file.write(f"Language: {transcript['language']}\n\n")
        file.write(_format_segments_as_captions(transcript["segments"]))

    return output_txt_path