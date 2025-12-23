# test.py

from graph.workflow import app
from graph.state import AgentState

def run_test(user_prompt: str, input_data: str = None):
    """
    Test the agent pipeline
    """
    
    print("=" * 80)
    print("DSAI AGENT - TEST RUN")
    print("=" * 80)
    print(f"User Prompt: {user_prompt}")
    if input_data:
        print(f"Input Data: {input_data}")
    print("=" * 80)
    
    # Initialize state
    initial_state = AgentState(
        user_prompt=user_prompt,
        input_data=input_data,
        input_type="",
        extracted_content=None,
        extraction_metadata=None,
        detected_intent=None,
        intent_confidence=0.0,
        needs_clarification=False,
        clarification_question=None,
        user_clarification=None,
        execution_plan=[],
        current_step=0,
        step_results={},
        final_output="",
        logs=[]
    )
    
    # Run workflow
    try:
        final_state = app.invoke(initial_state)
        
        # Check if clarification needed
        if final_state["needs_clarification"]:
            print("\n" + "=" * 80)
            print("CLARIFICATION NEEDED")
            print("=" * 80)
            print(f"Question: {final_state['clarification_question']}")
            print("\nPlease provide clarification and run again with:")
            print(f'state["user_clarification"] = "your answer"')
            return final_state
        
        # Display results
        print("\n" + "=" * 80)
        print("FINAL OUTPUT")
        print("=" * 80)
        print(final_state["final_output"])
        
        print("\n" + "=" * 80)
        print("EXECUTION LOGS")
        print("=" * 80)
        for log in final_state["logs"]:
            print(f"  • {log}")
        
        return final_state
    
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # TEST CASE 1: Audio + Summary
    # print("\n🎵 TEST 1: Audio Transcription + Summary\n")
    # run_test(
    #     user_prompt="Summarize this audio lecture",
    #     input_data="lecture.mp3"
    # )
    
    # TEST CASE 2: PDF + Action Items
    # print("\n📄 TEST 2: PDF Extraction + Action Items\n")
    # run_test(
    #     user_prompt="What are the action items from this meeting?",
    #     input_data="Assignment DSAI.pdf"
    # )
    
    # TEST CASE 3: Image + Code Explanation
    # print("\n TEST 3: Image OCR + Code Explanation\n")
    # run_test(
    #     user_prompt="Explain this code",
    #     input_data="code_screenshot.png"
    # )
    
    # TEST CASE 4: Ambiguous Query (should ask follow-up)
    # print("\n❓ TEST 4: Ambiguous Query\n")
    # run_test(
    #     user_prompt="What can you tell me about this?",
    #     input_data="document.pdf"
    # )
    # TEST CASE 5: Conversational (should ask follow-up)
    print("\n❓ TEST 5: Ambiguous Query\n")
    run_test(
        user_prompt="Hey, whats up",
        # input_data="document.pdf"
    )