

def transcribe(audio_path: str) -> dict:
    """
    Transcribe audio to text using Whisper
    Lazy import to avoid crash when ASR not used
    """
    try:
        import whisper
    except Exception as e:
        raise RuntimeError(
            "Whisper is not available in this environment. "
            "Install Python 3.10/3.11 or disable ASR."
        ) from e

    model = whisper.load_model("base")

    result = model.transcribe(audio_path)

    return {
        "text": result["text"],
        "duration": result.get("duration", 0),
        "language": result.get("language", "unknown")
    }