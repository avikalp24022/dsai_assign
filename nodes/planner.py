from graph.state import AgentState
from tools.llm_inference import inference

PLANNING_PROMPT = """
You are a task planner. Create an execution plan based on the user's intent.

Intent: {intent}
User Query: {query}
Input Type: {input_type}
Has Extracted Content: {has_content}

Available tasks:
- "transcribe_audio": Convert audio to text (only if input_type is audio and not already transcribed)
- "ocr_image": Extract text from image (only if input_type is image and not already extracted)
- "parse_pdf": Extract text from PDF (only if input_type is pdf and not already extracted)
- "fetch_youtube": Get YouTube transcript (only if youtube URL detected)
- "summarize": Create 1-line + 3 bullets + 5-sentence summary
- "sentiment_analysis": Analyze sentiment with label + confidence + justification
- "code_explanation": Explain code + detect bugs + time complexity
- "conversational_response": Answer general questions

Rules:
1. If content is NOT extracted yet, start with extraction task
2. Then add the main task based on intent
3. Keep plan minimal (1-3 steps usually)
4. For "summarize" intent on audio: ["transcribe_audio", "summarize"]
5. For "sentiment" on PDF: ["parse_pdf", "sentiment_analysis"]
6. For "code_explain" on image: ["ocr_image", "code_explanation"]

Return JSON array: ["task1", "task2"]
> **Return ONLY valid JSON.  
> Do not include explanations, markdown, or text outside JSON.**
"""

def process(state: AgentState) -> AgentState:
    """
    Create execution plan based on intent.
    """
    
    print("\n[PLANNER] Creating execution plan...")
    
    has_content = bool(state.get("extracted_content"))
    
    planning_prompt = PLANNING_PROMPT.format(
        intent=state["detected_intent"],
        query=state["user_prompt"],
        input_type=state.get("input_type", "text"),
        has_content=has_content
    )
    
    try:
        plan = inference(user_prompt=planning_prompt, json_req=True)
       
        
        # Ensure it's a list
        if isinstance(plan, dict) and "plan" in plan:
            plan = plan["plan"]
        elif not isinstance(plan, list):
            plan = [plan]
        
        state["execution_plan"] = plan
        state["current_step"] = 0
        
        print(f"[PLANNER] Plan: {' → '.join(plan)}")
        state["logs"].append(f"Execution plan: {' → '.join(plan)}")
    
    except Exception as e:
        print(f"[PLANNER] Planning failed: {str(e)}")
        intent = state["detected_intent"]
        if intent == "summarize":
            state["execution_plan"] = ["summarize"]
        elif intent == "sentiment":
            state["execution_plan"] = ["sentiment_analysis"]
        elif intent == "code_explain":
            state["execution_plan"] = ["code_explanation"]
        else:
            state["execution_plan"] = ["conversational_response"]
        
        state["current_step"] = 0
    
    return state