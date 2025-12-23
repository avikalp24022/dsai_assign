from tools.llm_inference import inference

SENTIMENT_PROMPT = """
Analyze the sentiment of this text.

Text: {text}

Return ONLY valid JSON with this exact structure:
{{
    "label": "positive" or "negative" or "neutral",
    "confidence": 0.85,
    "justification": "Brief one-line explanation why"
}}
"""

def analyze(user_text:str):
    prompt = SENTIMENT_PROMPT.format(text=user_text)
    analysis = inference(user_prompt=prompt, json_req=True)
    
    return analysis