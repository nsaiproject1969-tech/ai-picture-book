from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


# LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# 1️⃣ STORY GENERATOR
story_prompt = PromptTemplate(
    input_variables=["idea"],
    template="""
Write a short children's story based on this idea.

Idea:
{idea}

Keep it simple and divide it into 4 scenes.
"""
)

#story_chain = LLMChain(llm=llm, prompt=story_prompt)
story_chain = story_prompt | llm

# 2️⃣ SCENE EXTRACTOR
scene_prompt = PromptTemplate(
    input_variables=["story"],
    template="""
Extract 4 visual scenes from this story.

Return format:

Scene 1:
Scene 2:
Scene 3:
Scene 4:

Story:
{story}
"""
)

scene_chain = scene_prompt | llm
#scene_chain = LLMChain(llm=llm, prompt=scene_prompt)

# 3️⃣ MIDJOURNEY PROMPT GENERATOR
image_prompt = PromptTemplate(
    input_variables=["scene"],
    template="""
Create a Midjourney prompt for a children's book illustration.

Scene:
{scene}

Style: children's book illustration, whimsical, soft lighting, storybook art
"""
)

#image_chain = LLMChain(llm=llm, prompt=image_prompt)

image_chain = image_prompt | llm
# TEST IDEA
idea = "A brave mouse exploring a magical forest"

# RUN PIPELINE
#story = story_chain.run(idea=idea)
story = story_chain.invoke({"idea": idea}).content
#scenes = scene_chain.run(story=story)
scenes = scene_chain.invoke({"story": story}).content

scene_list = scenes.split("\n")

prompts = []

for scene in scene_list:
    if scene.strip():
        prompt = image_chain.invoke({"scene": scene}).content
        prompts.append(prompt)

# PRINT PROMPTS
print("\n==============================")
print("MIDJOURNEY PROMPTS")
print("==============================")

for i, p in enumerate(prompts):
    print(f"\nScene {i+1}")
    print("/imagine prompt:", p)