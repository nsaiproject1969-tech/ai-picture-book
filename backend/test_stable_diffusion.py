from diffusers import StableDiffusionPipeline
import torch

print("Loading model... (first time may take a few minutes)")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)

pipe = pipe.to("mps")  # for Mac GPU acceleration

prompt = "children book illustration of a brave mouse exploring a magical forest, watercolor style"

print("Generating image...")

image = pipe(prompt).images[0]

image.save("mouse_story.png")

print("Image saved as mouse_story.png")