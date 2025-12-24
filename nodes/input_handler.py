import os
from graph.state import AgentState
from tools import ocr_tool, pdf_parser, asr

from typing import TypedDict, Optional, List, Dict, Any


def detect_input_type(user_prompt: str, input_data: Optional[str]) -> str:
    # Check if it's a file
    if input_data and os.path.isfile(input_data):
        ext = os.path.splitext(input_data)[1].lower()
        
        if ext in ['.jpg', '.jpeg', '.png']:
            return "image"
        elif ext == '.pdf':
            return "pdf"
        elif ext in ['.mp3', '.wav', '.m4a', '.mp4']:
            return "audio"
    
    # Check for YouTube URL
    if "youtube.com" in user_prompt or "youtu.be" in user_prompt:
        return "youtube"
    
    # Check if text contains a file path
    if input_data and not os.path.isfile(input_data):
        return "text"  # It's raw text content
    
    # Default to text query
    return "text"


def extract_content(input_type: str, input_data: str) -> Dict[str, Any]:
    """Extract content based on input type"""
    
    if input_type == "image":
        result = ocr_tool.extract(input_data)
        return {
            "content": result["text"] or "",
            "metadata": {"ocr_confidence": result["confidence"]}
        }
    
    elif input_type == "pdf":
        result = pdf_parser.extract_pdf(input_data)
        return {
            "content": result["text"] or "",
            "metadata": {"confidence": result["confidence"], "pages": result["pages"]}
        }
    
    elif input_type == "audio":
        result = asr.transcribe(input_data, "Transcribe this audio")
        return {
            "content": result["text"] or "",
            "metadata": {"duration": result["duration"]}
        }
    
    elif input_type == "youtube":
        from tools.youtube_transcribe import get_transcript
        print(f"YT Link is in this format: {input_data}")
        result = get_transcript(input_data)
        return {
            "content": result["transcript"] if result["success"] else "",
            "metadata": {"video_id": result.get("video_id")}
        }
    
    elif input_type == "text":
        return {
            "content": input_data or "",
            "metadata": {}
        }


def process(state: AgentState) -> AgentState:
    print("\n[INPUT HANDLER] Processing input...")
    
    # Step 1: Detect input type
    input_type = detect_input_type(state["user_prompt"], state.get("input_data"))
    state["input_type"] = input_type
    
    print(f"[INPUT HANDLER] Detected input type: {input_type}")
    state["logs"].append(f"Input type: {input_type}")
    
    # Step 2: Extract content
    try:
        if input_type == "youtube":
            import re
            match = re.search(
                r"(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?[^\s]+|youtu\.be\/[^\s]+))",
                state["user_prompt"]
            )
            state["input_data"] = match.group(1)
            result = extract_content(input_type, state.get("input_data", state["user_prompt"]))

        result = extract_content(input_type, state.get("input_data", state["user_prompt"]))
        state["extracted_content"] = result["content"]
        state["extraction_metadata"] = result["metadata"]
        
        print(f"[INPUT HANDLER] Extracted {len(result['content'])} characters")
        state["logs"].append(f"Extracted content: {len(result['content'])} chars")
        
        if result["metadata"]:
            print(f"[INPUT HANDLER] Metadata: {result['metadata']}")
            state["logs"].append(f"Metadata: {result['metadata']}")
    
    except Exception as e:
        print(f"[INPUT HANDLER] Extraction failed: {str(e)}")
        state["logs"].append(f"ERROR: {str(e)}")
        state["extracted_content"] = state["user_prompt"]
    
    return state