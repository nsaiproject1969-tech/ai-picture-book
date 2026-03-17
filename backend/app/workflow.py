from typing import TypedDict, List
from langgraph.graph import StateGraph

from app.agents.story_agent import generate_story
from app.agents.character_agent import generate_character
from app.agents.page_split_agent import split_pages
from app.agents.prompt_agent import create_image_prompt
from app.agents.midjourney_agent import build_midjourney_prompt
from app.agents.midjourney_executor import generate_midjourney_image
from app.services.discord_sender import generate_midjourney_image


class Page(TypedDict):
    page: int
    text: str
    image_prompt: str


class BookState(TypedDict, total=False):
    theme: str
    story: str
    character: dict
    pages: List[Page]


# ------------------------
# Agent Nodes
# ------------------------

def story_node(state: BookState):

    story = generate_story(state["theme"])

    return {"story": story}


def character_node(state: BookState):

    character = generate_character(state["theme"])

    return {"character": character}


def split_node(state: BookState):

    result = split_pages(state["story"])

    return {"pages": result["pages"]}


def prompt_node(state: BookState):

    pages_with_prompts = []

    for page in state["pages"]:

        scene_prompt = create_image_prompt(
            page["text"],
            state["character"]["description"]
        )

        mj_prompt = build_midjourney_prompt(
            scene_prompt,
            state["character"]["description"]
        )

        pages_with_prompts.append({
            "page": page["page"],
            "text": page["text"],
            "image_prompt": mj_prompt
        })

    return {"pages": pages_with_prompts}


def image_node(state):

    prompt = state["image_prompt"]

    generate_midjourney_image(prompt)

    return state


# ------------------------
# Graph Definition
# ------------------------

builder = StateGraph(BookState)

builder.add_node("story", story_node)
builder.add_node("character", character_node)
builder.add_node("split", split_node)
builder.add_node("prompt", prompt_node)
#builder.add_node("image", image_node)

builder.set_entry_point("story")

builder.add_edge("story", "character")
builder.add_edge("character", "split")
builder.add_edge("split", "prompt")
#builder.add_edge("prompt", "image")


workflow = builder.compile()