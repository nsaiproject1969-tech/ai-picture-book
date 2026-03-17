import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_character(theme):

    prompt = f"""
Create the main character for a children's picture book.

Theme: {theme}

Return JSON:

{{
 "name": "...",
 "description": "...",
 "image_prompt": "midjourney prompt for character portrait"
}}
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type":"json_object"},
        messages=[{"role":"user","content":prompt}]
    )

    import json
    return json.loads(res.choices[0].message.content)