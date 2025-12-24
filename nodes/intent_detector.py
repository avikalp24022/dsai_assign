from graph.state import AgentState
from tools.llm_inference import inference
import json

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