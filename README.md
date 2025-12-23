# DSAI Agentic System

Multi-modal AI agent that processes text, images, PDFs, and audio files to perform tasks like summarization, sentiment analysis, code explanation, and more.

---

## Features

- 🎵 Audio transcription (Whisper)
- 📄 PDF text extraction
- 🖼️ Image OCR
- 📺 YouTube transcript fetching
- 📝 Summarization (1-line + bullets + detailed)
- 😊 Sentiment analysis
- 💻 Code explanation with bug detection
- 💬 Conversational Q&A
- ❓ **Smart clarification** - asks follow-up questions when intent is unclear

---

## How It Works

```
User Input (text/file) 
    ↓
Input Handler (extracts content)
    ↓
Intent Detector (what does user want?)
    ↓
[Needs clarification?] → YES → Ask user → Get response
    ↓ NO
Planner (creates task plan)
    ↓
Executor (runs tools)
    ↓
Output Formatter (formats result)
    ↓
Return to user
```

**Example Flow:**
1. User uploads `code_screenshot.png` + "Explain this code"
2. Agent extracts text via OCR → detects "code_explain" intent
3. Creates plan: `["ocr_image", "code_explanation"]`
4. Executes: Tesseract OCR (extracts code) → Code Analysis tool
5. Returns: Code explanation + bug detection + time/space complexity

---

## Installation

### Prerequisites
- Python 3.9+
- GEMINI API KEY and BUILD Nvidia API KEY
- Tesseract OCR

### Install Tesseract

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to `C:\Program Files\Tesseract-OCR`
3. Add to PATH or configure in code (see Troubleshooting)

### Setup

**Windows:**
```cmd
# 1. Clone repo
git clone <repo-url>
cd DSAI

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (use notepad)
echo OPENAI_API_KEY=sk-your-key-here > .env
```

---

## Running the App

### Option 1: Web Interface (Chat UI)
```bash
python main.py
```
Open: http://localhost:8000

### Option 2: CLI Testing
```bash
python test.py
```

### Option 3: Python Script
```python
from test import run_agent

# Simple question
run_agent("What is machine learning?")

# Process file
run_agent("Summarize this", input_data="lecture.mp3")
```

---

## Usage Examples

### 1. Conversational Query
```python
run_agent("What is natural language processing?")
# Returns: Full explanation in natural language
```

### 2. PDF Analysis + Summary
```python
run_agent("Summarize this lecture", input_data="lecture.pdf")
# Returns: 1-line + 3 bullets + 5-sentence summary with duration
```

### 3. Image Code Explanation
```python
run_agent("Explain this code", input_data="code_screenshot.png")
# Returns: What code does + bugs detected + time complexity
```
---

## Configuration

Create `.env` file:
```bash
NVIDIA_API_KEY=your-key-here
LLM_MODEL=model-input
TEMPERATURE=0.3
INTENT_CONFIDENCE_THRESHOLD=0.7
```
---

## Testing

Run all test cases:
```bash
python test.py
```

This runs:
- Audio transcription + summary
- PDF action items extraction
- Image OCR + code explanation
- YouTube transcript fetching
- Sentiment analysis
- Ambiguous query (clarification flow)

---

## Troubleshooting

**Tesseract not found (Windows):**
```python
# In tools/ocr_tool.py, add at the top:
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**Module not found errors:**
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📊 Supported Files

| Type | Formats | Max Size |
|------|---------|----------|
| Images | JPG, PNG | 10 MB |
| Audio | MP3, WAV, M4A, <P4> | 25 MB |
| Documents | PDF | 10 MB |

---


**Built with LangGraph, FastAPI, and Gemini and NIM API**