import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_story(theme):

    prompt = f"""
Write a short children's story in Japanese about a brave mouse exploring a magical forest.
    Use simple language for children.

Theme: {theme}

Length: 8 pages
Each page 1-2 sentences.
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res.choices[0].message.content