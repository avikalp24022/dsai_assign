from graph.state import AgentState
from tools.llm_inference import inference
import json

INTENT_DETECTION_PROMPT = """
You are an intent detection system. Analyze the user's query and extracted content.

User Query: {query}
Extracted Content: {content}
Input Type: {input_type}

Available intents:
1. "extract_text" - User wants text extraction only
2. "summarize" - User wants a summary
3. "sentiment" - User wants sentiment analysis
4. "code_explain" - User wants code explanation
5. "conversational" - General question/conversation
6. "youtube_transcript" - User wants YouTube transcript
7. "transcribe" - User wants to transcribe the audio
8. "ambiguous" - Intent is unclear

Rules:
- If confidence < 0.7, mark as "ambiguous"
- If multiple intents are plausible, mark as "ambiguous"
- If user query is vague ("What should I do with this?"), mark as "ambiguous"

Return JSON:
{{
    "intent": "summarize",
    "confidence": 0.9,
    "reasoning": "User explicitly asked for summary",
    "needs_clarification": false,
    "clarification_question": null
}}

> **Return ONLY valid JSON.  
> Do not include explanations, markdown, or text outside JSON.**

If needs_clarification = true, provide a short, clear question.
"""


def process(state: AgentState) -> AgentState:    
    print("\n[INTENT DETECTOR] Analyzing intent...")
    
    if state.get("user_clarification"):
        print("[INTENT DETECTOR] Using user clarification")
        prompt = state["user_clarification"]
    else:
        prompt = state["user_prompt"]
    
    detection_prompt = INTENT_DETECTION_PROMPT.format(
        query=prompt,
        content=state.get("extracted_content", "")[:500],
        input_type=state.get("input_type", "text")
    )
    
    try:
        raw = inference(user_prompt=detection_prompt)
        import re
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in model output")
        json_str = match.group()
        result = json.loads(json_str)
        # result = json.loads(match)
        
        state["detected_intent"] = result["intent"]
        state["intent_confidence"] = result["confidence"]
        state["needs_clarification"] = result["needs_clarification"]
        state["clarification_question"] = result.get("clarification_question")
        
        print(f"[INTENT DETECTOR] Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        print(f"[INTENT DETECTOR] Needs clarification: {result['needs_clarification']}")
        
        state["logs"].append(f"Detected intent: {result['intent']} ({result['confidence']:.2f})")
        
        if result["needs_clarification"]:
            print(f"[INTENT DETECTOR] Question: {result['clarification_question']}")
            state["logs"].append(f"Asking: {result['clarification_question']}")
    
    except Exception as e:
        print(f"[INTENT DETECTOR] Error: {str(e)}")
        state["needs_clarification"] = True
        state["clarification_question"] = "What would you like me to do with this content?"
    
    return state