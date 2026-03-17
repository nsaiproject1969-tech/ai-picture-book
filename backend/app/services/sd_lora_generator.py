from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class SDLoRAConfig:
    model_id: str = "runwayml/stable-diffusion-v1-5"
    lora_weights_path: Optional[str] = None
    device: str = "cuda"
    dtype: str = "float16"


class StableDiffusionLoRAGenerator:
    """Lazy-loaded Stable Diffusion + LoRA helper.

    Notes:
    - Designed so importing this module does not require diffusers/torch until runtime.
    - Use `generate_character_base` once, then `generate_page_from_reference` for each page.
    """

    def __init__(self, config: SDLoRAConfig):
        self.config = config
        self._txt2img = None
        self._img2img = None

    def _get_torch_dtype(self):
        import torch

        if self.config.dtype == "float16":
            return torch.float16
        if self.config.dtype == "bfloat16":
            return torch.bfloat16
        return torch.float32

    def _init_pipelines(self):
        if self._txt2img is not None and self._img2img is not None:
            return

        from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

        torch_dtype = self._get_torch_dtype()

        self._txt2img = StableDiffusionPipeline.from_pretrained(
            self.config.model_id,
            torch_dtype=torch_dtype,
        ).to(self.config.device)

        self._img2img = StableDiffusionImg2ImgPipeline.from_pretrained(
            self.config.model_id,
            torch_dtype=torch_dtype,
        ).to(self.config.device)

        if self.config.lora_weights_path:
            self._txt2img.load_lora_weights(self.config.lora_weights_path)
            self._img2img.load_lora_weights(self.config.lora_weights_path)

    def generate_character_base(
        self,
        prompt: str,
        output_path: str,
        negative_prompt: Optional[str] = None,
        steps: int = 30,
        guidance_scale: float = 7.0,
        seed: int = 42,
    ) -> str:
        import torch

        self._init_pipelines()
        generator = torch.Generator(device=self.config.device).manual_seed(seed)
        image = self._txt2img(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images[0]

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        return output_path

    def generate_page_from_reference(
        self,
        prompt: str,
        reference_image_path: str,
        output_path: str,
        negative_prompt: Optional[str] = None,
        steps: int = 30,
        guidance_scale: float = 7.0,
        strength: float = 0.45,
        seed: int = 42,
    ) -> str:
        import torch
        from PIL import Image

        self._init_pipelines()
        generator = torch.Generator(device=self.config.device).manual_seed(seed)
        reference = Image.open(reference_image_path).convert("RGB")

        image = self._img2img(
            prompt=prompt,
            image=reference,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            strength=strength,
            generator=generator,
        ).images[0]

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        return output_path
