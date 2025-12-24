from graph.state import AgentState

def process(state: AgentState) -> AgentState:    
    print("\n[OUTPUT FORMATTER] Formatting results...")
    
    output_parts = []
    
    # Header
    output_parts.append("=" * 80)
    output_parts.append("AGENT EXECUTION RESULTS")
    output_parts.append("=" * 80)
    output_parts.append("")
    
    # Show extraction metadata if exists
    if state.get("extraction_metadata"):
        output_parts.append("EXTRACTION METADATA:")
        for key, value in state["extraction_metadata"].items():
            output_parts.append(f"  • {key}: {value}")
        output_parts.append("")
    
    # Show extracted content (truncated)
    if state.get("extracted_content"):
        content = state["extracted_content"]
        if len(content) > 300:
            content = content[:300] + "..."
        output_parts.append("EXTRACTED CONTENT:")
        output_parts.append(content)
        output_parts.append("")
    
    # Show results from each task
    output_parts.append("TASK RESULTS:")
    output_parts.append("")
    
    # for task, result in state["step_results"].items():
    #     output_parts.append(f"{task.upper().replace('_', ' ')}")
    #     output_parts.append("-" * 80)
        
    #     if isinstance(result, dict):
    #         if "error" in result:
    #             output_parts.append(f"Error: {result['error']}")
    #         else:
    #             for key, value in result.items():
    #                 if key != "text":  # Don't repeat full text
    #                     output_parts.append(f"  {key}: {value}")
    #     else:
    #         output_parts.append(str(result))
        
    #     output_parts.append("")

    # for result in state["step_results"]:
    result = state["step_results"]
    output_parts.append(f"Task Output")
    output_parts.append("-" * 80)
    
    if isinstance(result, dict):
        if "error" in result:
            output_parts.append(f"Error: {result['error']}")
        else:
            for key, value in result.items():
                if key != "text":  # Don't repeat full text
                    output_parts.append(f"  {key}: {value}")
    else:
        output_parts.append(str(result))
    
    output_parts.append("")
        
    
    state["final_output"] = "\n".join(output_parts)
    state["logs"].append("Output formatted successfully")
    
    return state
