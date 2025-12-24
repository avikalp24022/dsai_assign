# from tools.llm_inference import inference_gemini

# # def transcribe(audio_path: str) -> dict:
# #     """
# #     Transcribe audio to text using Whisper
# #     Lazy import to avoid crash when ASR not used
# #     """
# #     try:
# #         import whisper
# #     except Exception as e:
# #         raise RuntimeError(
# #             "Whisper is not available in this environment. "
# #             "Install Python 3.10/3.11 or disable ASR."
# #         ) from e

# #     model = whisper.load_model("base")

# #     result = model.transcribe(audio_path)

# #     return {
# #         "text": result["text"],
# #         "duration": result.get("duration", 0),
# #         "language": result.get("language", "unknown")
# #     }

# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# USER_AUDIO_PROMPT="""
# I've attached the audio file data, perform {user_query} for this audio {audio_data}
# """

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def transcribe(audio_path: str, user_prompt: str) -> dict:
#     """
#     Transcribe audio to text using OpenAI Whisper API
#     """

#     if not os.path.exists(audio_path):
#         raise FileNotFoundError(f"Audio file not found: {audio_path}")

#     with open(audio_path, "rb") as audio_file:
#         # response = client.audio.transcriptions.create(
#         #     file=audio_file,
#         #     model="whisper-1",
#         #     response_format="verbose_json"
#         # )
#         audio_prompt = USER_AUDIO_PROMPT.format(
#         user_query=user_prompt,
#         audio_data=audio_file
# )
#         response = inference_gemini(user_prompt=audio_prompt)

#     return {
#         "text": response["text"],
#         "language": response.get("language", "unknown"),
#         "duration": response.get("duration", None),
#         "segments": response.get("segments", [])
#     }


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