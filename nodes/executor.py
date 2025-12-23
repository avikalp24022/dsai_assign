from graph.state import AgentState
from tools import (
    asr, ocr_tool, pdf_parser, youtube_transcribe,
    summarization, sentiment_analysis, code_analysis, conversation
)

TASK_MAP = {
    "transcribe_audio": asr.transcribe,
    "ocr_image": ocr_tool.extract,
    "parse_pdf": pdf_parser.extract_pdf,
    "fetch_youtube": youtube_transcribe.get_transcript,
    "summarize": summarization.summarize,
    "sentiment_analysis": sentiment_analysis.analyze,
    "code_explanation": code_analysis.explain,
    "conversational_response": conversation.answer_question
}

def process(state: AgentState) -> AgentState:
    if state["current_step"] >= len(state["execution_plan"]):
        return state
    
    current_task = state["execution_plan"][state["current_step"]]
    print(f"\n[EXECUTOR] Running task: {current_task}")
    state["logs"].append(f"Executing: {current_task}")
    
    try:
        tool_func = TASK_MAP.get(current_task)
        
        if not tool_func:
            print(f"[EXECUTOR] Unknown task: {current_task}")
            state["step_results"][current_task] = {"error": f"Unknown task: {current_task}"}
            state["current_step"] += 1
            return state
        
        # Determine input for the tool
        if current_task in ["transcribe_audio", "ocr_image", "parse_pdf"]:
            input_data = state.get("input_data")
            result = tool_func(input_data)
            
            if "text" in result:
                state["extracted_content"] = result["text"]
        
        elif current_task == "fetch_youtube":
            result = tool_func(state["user_prompt"])
            if result.get("success"):
                state["extracted_content"] = result["transcript"]
        
        elif current_task == "code_explanation":
            content = state.get("extracted_content", "")
            query = state["user_prompt"]
            result = tool_func(content)

        elif current_task == "summarize":
            content = state.get("extracted_content", "")
            query = state["user_prompt"]
            result = tool_func(content)

        else:
            content = state.get("extracted_content", "")
            query = state["user_prompt"]
            result = tool_func(content, query)
        
        state["step_results"][current_task] = result
        print(f"[EXECUTOR] Task completed: {current_task}")
    
    except Exception as e:
        print(f"[EXECUTOR] Task failed: {str(e)}")
        state["step_results"][current_task] = {"error": str(e)}
        state["logs"].append(f"ERROR in {current_task}: {str(e)}")
    
    state["current_step"] += 1
    return state