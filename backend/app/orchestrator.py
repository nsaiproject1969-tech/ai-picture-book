from app.agents.story_agent import generate_story
from app.agents.page_split_agent import split_pages
from app.agents.prompt_agent import create_image_prompt
from app.agents.character_agent import generate_character, character_reference

def generate_book(theme):

    story = generate_story(theme)

    character = generate_character(theme)

    pages_data = split_pages(story)

    prompts = []

    for page in pages_data["pages"]:

        prompt = create_image_prompt(
            page["text"],
            character_reference(character)
        )

        prompts.append({
            "page": page["page"],
            "text": page["text"],
            "image_prompt": prompt
        })

    return {
        "story": story,
        "character": character,
        "pages": prompts
    }