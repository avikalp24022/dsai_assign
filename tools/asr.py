from openai import OpenAI
import os

client = OpenAI()

def transcribe_audio(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="text"   # ensures plain text output
        )

    return transcription


if __name__ == "__main__":
    transcribe_audio("WhatsApp Audio 2025-12-23 at 1.31.22 PM.mp4")