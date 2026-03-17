def build_midjourney_prompt(scene_prompt, character):

    mj_prompt = f"""
{scene_prompt}

Character description:
{character}

children's picture book illustration
soft pastel colors
storybook style

--ar 4:3
--v 6
--style raw
--cw 100
"""

    return mj_prompt.strip()