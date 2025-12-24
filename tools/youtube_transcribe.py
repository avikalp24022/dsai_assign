import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(text: str) -> str | None:
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return None


def get_transcript(text: str) -> dict:
    video_id = extract_video_id(text)

    if not video_id:
        return {
            "success": False,
            "error": "No YouTube URL found"
        }

    try:
        ytt_api = YouTubeTranscriptApi()
        
        transcript_list = ytt_api.fetch(video_id)
        full_text = " ".join(
            snippet.text for snippet in transcript_list.snippets
        )

        return {
            "success": True,
            "video_id": video_id,
            "transcript": full_text
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    print(
        get_transcript(
            "https://www.youtube.com/watch?v=USW8yf4L-R4"
        )
        # get_transcript(
        #     "https://www.youtube.com/watch?v=ry9SYnV3svc"
        # )
        # get_transcript(
        #     "https://www.youtube.com/watch?v=8rWtLqyQm6E"
        # )
    )
