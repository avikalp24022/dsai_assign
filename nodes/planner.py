from graph.state import AgentState
from tools.llm_inference import inference

def process(state: AgentState) -> AgentState:
    print("\n[PLANNER] Creating execution plan...")

    intent=state["detected_intent"]
    
    try:
        plan = intent
       
        print(plan)
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