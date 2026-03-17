
from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)

pipe = pipe.to("mps")  # Mac GPU


def generate_image(prompt, filename):

    image = pipe(prompt).images[0]

    image.save(filename)