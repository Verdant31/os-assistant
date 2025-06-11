import io
import json
import argparse
import whisper
import numpy as np
import sys
import time

model = whisper.load_model("small")

sys.stdout = io.TextIOWrapper(
    sys.stdout.buffer,
    encoding='utf-8',
    line_buffering=True
)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def is_audio_silent(audio_array: np.ndarray, threshold: float = 0.020) -> bool:
    """Detects whether the audio signal is effectively silent."""
    print(f"Audio max value: {np.abs(audio_array).max()}")
    return np.abs(audio_array).max() < threshold


def speech_to_text(wav_path: str) -> dict:
    """
    Transcribe a WAV audio file to text using OpenAI's Whisper model.

    Parameters:
    - wav_path: Path to the .wav audio file.

    Returns:
    - Dictionary with transcribed text and transcription time.
    """
    audio = whisper.load_audio(wav_path)

    if is_audio_silent(audio):
        return {
            "text": "",
            "transcription_time_seconds": 0.0,
            "skipped": True,
            "reason": "Detected silence"
        }

    start_time = time.time()
    options = {"fp16": False, "task": "transcribe", 'no_speech_threshold': 0.1,
               "condition_on_previous_text": False, "logprob_threshold": -1.00, "without_timestamps": True}

    result = model.transcribe(wav_path,  **options)
    end_time = time.time()

    elapsed_time = end_time - start_time

    return {
        "text": result.get("text", ""),
        "transcription_time_seconds": round(elapsed_time, 2)
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe a WAV file to text using Whisper"
    )
    parser.add_argument(
        "--wav_path",
        default=r"C:\Users\verdant\AppData\Roaming\com.desktop-assistant.app\tauri-plugin-mic-recorder\20250506174355.wav",
        help="Path to the .wav audio file to transcribe"
    )

    args = parser.parse_args()
    try:
        result = speech_to_text(args.wav_path)
        result["text"] = result["text"].encode('utf-8').decode('utf-8')
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        err = {"Error -> speech2Text.py:": str(e)}
        print(json.dumps(err, ensure_ascii=False))
        sys.exit(1)
