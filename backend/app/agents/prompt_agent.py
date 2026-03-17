import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def create_image_prompt(page_text, character):

    prompt = f"""
Create a Midjourney prompt for a children's picture book illustration.

Character:
{character}

Scene:
{page_text}

Style: colorful children's picture book
"""

    return prompt