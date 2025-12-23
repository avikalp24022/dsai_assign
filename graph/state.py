from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    # Input
    user_prompt: str                          # "Summarize this audio"
    input_type: str                           # "audio", "image", "pdf", "text", "youtube"
    input_data: Optional[str]                 # File path or text content
    
    # Extracted Content
    extracted_content: Optional[str]          # Transcribed/OCR'd/parsed text
    extraction_metadata: Optional[Dict]       # {confidence, duration, pages, etc}
    
    # Intent & Clarity
    detected_intent: Optional[str]            # "summarize", "sentiment", etc.
    intent_confidence: float                  # 0.0 - 1.0
    needs_clarification: bool                 # True if ambiguous
    clarification_question: Optional[str]     # Question to ask user
    user_clarification: Optional[str]         # User's clarification response
    
    # Planning & Execution
    execution_plan: List[str]                 # ["transcribe", "summarize"]
    current_step: int                         # Current step in plan
    step_results: Dict[str, Any]              # Results from each step
    
    # Output
    final_output: str                         # Final formatted result
    logs: List[str]                           # Execution logs