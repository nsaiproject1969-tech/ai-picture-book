import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def split_pages(story):

    prompt = f"""
Split this children's story into exactly 8 pages.

Return JSON like:

{{
 "pages":[
   {{"page":1,"text":"..."}},
   {{"page":2,"text":"..."}}
 ]
}}

Story:
{story}
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    data = res.choices[0].message.content

    import json
    return json.loads(data)