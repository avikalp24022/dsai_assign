import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(text: str) -> str:
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
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_list])
        
        return {
            "success": True,
            "transcript": transcript,
            "video_id": video_id
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
