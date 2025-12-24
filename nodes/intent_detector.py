from graph.state import AgentState
from tools.llm_inference import inference
import json

# INTENT_DETECTION_PROMPT = """
# You are an intent detection system. Analyze the user's query and few sample of extracted content.

# - If task is related to summarize or transcribe or analysis but enough data is not given like very 10 worded text or no code or no pdf or audio, then needs_clarification="true" and intent = ambiguous.

# User Query: {query}
# Extracted Content: {content}
# Input Type: {input_type}

# Available intents:
# 1. "extract_text" - User wants text extraction only
# 2. "summarize" - User wants a summary
# 3. "sentiment" - User wants sentiment analysis
# 4. "code_explain" - User wants code explanation
# 5. "conversational" - General question/conversation
# 6. "youtube_transcript" - User wants YouTube transcript
# 7. "transcribe" - User wants to transcribe the audio
# 8. "ambiguous" - Intent is unclear

# Rules:
# - If confidence < 0.7, mark as "ambiguous"
# - If multiple intents are plausible, mark as "ambiguous"
# - If user query is vague ("What should I do with this?"), mark as "ambiguous"

# Return JSON:
# {{
#     "intent": "summarize",
#     "confidence": 0.9,
#     "reasoning": "User explicitly asked for summary",
#     "needs_clarification": false,
#     "clarification_question": null
# }}

# If needs_clarification = true, provide a short, clear question.

# > **Return ONLY valid JSON.  
# > Do not include explanations, markdown, or text outside JSON.**


# """

# INTENT_DETECTION_PROMPT = """
# You are an intent detection system. Analyze the user's query together with a **partial preview** of extracted content.

# Important:
# - The extracted content may be **intentionally truncated** (e.g., only the first 500 tokens).
# - **Do NOT request clarification simply because the content is short or incomplete.**
# - Assume the provided content is sufficient for intent detection.

# Only set needs_clarification = true **if the user's request itself is unclear**, contradictory, or impossible to infer.

# User Query: {query
# Input Type: {input_type}

# Available intents:
# 1. "extract_text" - User wants text extraction only
# 2. "summarize" - User wants a summary
# 3. "sentiment" - User wants sentiment analysis
# 4. "code_explain" - User wants code explanation
# 5. "conversational" - General question/conversation
# 6. "youtube_transcript" - User wants YouTube transcript
# 7. "transcribe" - User wants to transcribe the audio
# 8. "ambiguous" - Intent is unclear

# Decision Rules:
# - If confidence < 0.7 → intent = "ambiguous"
# - If multiple intents are equally plausible → intent = "ambiguous"
# - If the user's query is vague or underspecified → intent = "ambiguous"
# - **Do NOT mark ambiguous due to short or truncated content alone.**

# Return JSON exactly in this format:
# {{
#     "intent": "...",
#     "confidence": 0.0,
#     "reasoning": "...",
#     "needs_clarification": false,
#     "clarification_question": null
# }}

# If needs_clarification = true, provide a short, specific clarification question.

# Return ONLY valid JSON.
# No extra text, no markdown, no explanation.
# """

INTENT_DETECTION_PROMPT = """
You are an intent detection system.

User Query: {query}
Input Type: {input_type}

Choose one intent:
- extract_text
- summarize
- sentiment
- code_explain
- conversational
- youtube_transcript
- transcribe
- ambiguous

Rules:
- If unclear, vague, or multiple intents → ambiguous
- If confidence < 0.7 → ambiguous
- Ask for clarification ONLY if the query itself is unclear

Return ONLY this JSON:
{{
  "intent": "...",
  "confidence": 0.0,
  "reasoning": "...",
  "needs_clarification": false,
  "clarification_question": null
}}
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
        # content=state.get("extracted_content", "")[:100],
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
        # print(detection_prompt)
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