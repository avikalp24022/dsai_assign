# import os
# from openai import OpenAI

# # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def answer_question(prompt: str, json_mode: bool = False) -> str:
#     """
#     Get completion from OpenAI
#     """
    
#     messages = [{"role": "user", "content": prompt}]
    
#     kwargs = {
#         "model": "gpt-4.1-nano-2025-04-14",
#         "messages": messages,
#         "temperature": 0.3
#     }
    
#     if json_mode:
#         kwargs["response_format"] = {"type": "json_object"}
    
#     response = client.chat.completions.create(**kwargs)
#     return response.choices[0].message.content


from tools.llm_inference import inference

def answer_question(prompt: str, json_mode: bool = False) -> str:
    inference(user_prompt=prompt)