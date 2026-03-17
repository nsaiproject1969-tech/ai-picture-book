import json
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _build_character_prompt(theme: str) -> str:
    return f"""
You are creating a reusable character profile for a children's picture book.

Theme: {theme}

Return JSON only using this schema:
{{
  "name": "character name",
  "description": "2-4 sentence physical/personality description for children",
  "image_prompt": "midjourney portrait prompt",
  "visual_traits": ["trait 1", "trait 2", "trait 3", "trait 4"],
  "wardrobe": "default outfit and accessories",
  "palette": "3-5 color words"
}}

Rules:
- Keep visual traits concrete and easy to repeat across pages.
- Keep language child-friendly.
- Avoid style flags like --ar, --v, --style in image_prompt.
"""


def generate_character(theme: str) -> Dict[str, Any]:
    """Generate one canonical character definition used across every page."""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        temperature=0.4,
        messages=[{"role": "user", "content": _build_character_prompt(theme)}],
    )

    character = json.loads(res.choices[0].message.content)

    # Ensure expected keys are present for downstream prompt builders.
    character.setdefault("name", "Main Character")
    character.setdefault("description", "A kind and adventurous child-friendly character.")
    character.setdefault("image_prompt", character["description"])
    character.setdefault("visual_traits", [])
    character.setdefault("wardrobe", "simple storybook outfit")
    character.setdefault("palette", "soft pastel tones")

    return character


def character_reference(character: Dict[str, Any]) -> str:
    """Create a compact reusable character block for every page prompt."""

    traits: List[str] = character.get("visual_traits", []) or []
    traits_text = ", ".join(traits) if traits else character.get("description", "")

    return (
        f"Name: {character.get('name', 'Main Character')}\n"
        f"Core look: {traits_text}\n"
        f"Outfit: {character.get('wardrobe', 'simple storybook outfit')}\n"
        f"Color palette: {character.get('palette', 'soft pastel tones')}\n"
        "Consistency rule: Keep this character's face, proportions, and outfit recognizable in every page."
    )
