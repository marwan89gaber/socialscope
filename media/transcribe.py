import whisper
import torch

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