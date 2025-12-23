from dotenv import load_dotenv, find_dotenv, get_key
from openai import OpenAI

# def inference_nvidia(system_prompt="""""", user_prompt="""""", json_req=False):
#     client = OpenAI(
#         base_url = "https://integrate.api.nvidia.com/v1",
#         api_key = get_key(find_dotenv(), "NVIDIA_API_KEY")
#     )

#     completion = client.chat.completions.create(
#         model="qwen/qwen3-next-80b-a3b-instruct",
#         messages=[{"role":"user","content":user_prompt}],
#         temperature=0.2,
#         top_p=0.7,
#         max_tokens=8192,
#         stream=False
#     )

#     response = completion.choices[0].message.content.strip('\n')

#     if json_req == True:
#         import re
#         match = re.search(r'\{.*\}', response, re.DOTALL)
#         if not match:
#             raise ValueError("No JSON found in model output")
#         json_str = match.group()
#         print(json_str)
#         return json_str

#     # for chunk in completion:
#     #     reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
#     #     if reasoning:
#     #         print(reasoning, end="")
#     #     if chunk.choices[0].delta.content is not None:
#     #         print(chunk.choices[0].delta.content, end="")

#     return response

from google import genai
from google.genai import types

client = genai.Client(api_key="")
def inference(system_prompt="""""", user_prompt="""""", json_req=False):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt),
        contents=user_prompt
    )

    if json_req == True:
        import re
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in model output")
        json_str = match.group()
        print(json_str)
        return json_str

    print(response.text)
    return response.text