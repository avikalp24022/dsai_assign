# ============================================================================
# api/main.py - FastAPI Application Entry Point
# ============================================================================

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
from typing import Optional
from datetime import datetime
import uuid

from graph.workflow import app as workflow_app
from graph.state import AgentState

# Initialize FastAPI
app = FastAPI(
    title="DSAI Agentic System",
    description="Multi-modal AI agent for text, audio, PDF, and image processing",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Session storage (in-memory for now)
sessions = {}


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main chat interface"""
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/chat")
async def chat(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Form(None),
    clarification: Optional[str] = Form(None)
):
    """
    Main chat endpoint - handles text messages and file uploads
    
    Args:
        message: User's text message
        file: Optional uploaded file (image/pdf/audio)
        session_id: Session ID for conversation continuity
        clarification: Optional clarification response
    
    Returns:
        JSON with agent response and metadata
    """
    
    try:
        # Generate or retrieve session
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Initialize session if new
        if session_id not in sessions:
            sessions[session_id] = {
                "history": [],
                "pending_clarification": None
            }
        
        session = sessions[session_id]
        
        # Handle file upload
        file_path = None
        if file:
            # Save uploaded file
            file_extension = os.path.splitext(file.filename)[1]
            file_path = f"uploads/{uuid.uuid4()}{file_extension}"
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            print(f"[API] File uploaded: {file_path}")
        
        # Prepare agent state
        initial_state = AgentState(
            user_prompt=message,
            input_data=file_path,
            input_type="",
            extracted_content=None,
            extraction_metadata=None,
            detected_intent=None,
            intent_confidence=0.0,
            needs_clarification=False,
            clarification_question=None,
            user_clarification=clarification,
            execution_plan=[],
            current_step=0,
            step_results={},
            final_output="",
            logs=[]
        )
        
        # Run the agent workflow
        print(f"[API] Processing message: {message}")
        final_state = workflow_app.invoke(initial_state)
        
        # Check if clarification is needed
        if final_state["needs_clarification"] and not clarification:
            session["pending_clarification"] = {
                "question": final_state["clarification_question"],
                "state": final_state
            }
            
            response = {
                "type": "clarification",
                "message": final_state["clarification_question"],
                "session_id": session_id
            }
        else:
            # Add to conversation history
            session["history"].append({
                "role": "user",
                "message": message,
                "file": file.filename if file else None,
                "timestamp": datetime.now().isoformat()
            })
            
            session["history"].append({
                "role": "assistant",
                "message": final_state["final_output"],
                "logs": final_state["logs"],
                "timestamp": datetime.now().isoformat()
            })
            
            session["pending_clarification"] = None
            
            response = {
                "type": "response",
                "message": final_state["final_output"],
                "metadata": {
                    "extracted_content": final_state.get("extracted_content", "")[:500],
                    "extraction_metadata": final_state.get("extraction_metadata", {}),
                    "detected_intent": final_state.get("detected_intent"),
                    "execution_plan": final_state.get("execution_plan", []),
                },
                "logs": final_state["logs"],
                "session_id": session_id
            }
        
        # Cleanup uploaded file
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        
        return JSONResponse(content=response)
    
    except Exception as e:
        print(f"[API] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": "processing_error"
            }
        )


@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    """Get conversation history for a session"""
    
    if session_id not in sessions:
        return {"history": []}
    
    return {"history": sessions[session_id]["history"]}


@app.delete("/api/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a conversation session"""
    
    if session_id in sessions:
        del sessions[session_id]
    
    return {"status": "cleared"}


# ============================================================================
# Mount static files
# ============================================================================

app.mount("/static", StaticFiles(directory="static"), name="static")


# ============================================================================
# Run server
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 Starting DSAI Agent Server")
    print("=" * 80)
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("=" * 80)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


# ============================================================================
# static/index.html - Chat Interface
# ============================================================================

# HTML_CONTENT = """

# """

# # Save HTML file
# with open("static/index.html", "w") as f:
#     f.write(HTML_CONTENT)