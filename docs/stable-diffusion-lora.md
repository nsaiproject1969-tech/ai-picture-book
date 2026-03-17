# Stable Diffusion + LoRA integration notes

## Is it free?

- **Model usage**: Stable Diffusion base models and many LoRAs are open-source and can be used for free.
- **Compute is not free**: you still pay for GPU/CPU time (local machine, cloud VM, or managed inference API).
- **LoRA licenses vary**: always check each LoRA's license for commercial usage rights.

## Can we integrate it in this project?

Yes. This project can support a Stable Diffusion + LoRA pipeline in parallel to Midjourney.

Suggested flow:

1. Generate the **first image** (character base portrait).
2. Use that image as **reference input** for each page.
3. Keep the same LoRA + seed + guidance settings for consistency.

## Recommended generation flow

### 1) Character base image

- Run txt2img with a character-focused prompt.
- Save output as `assets/character_base.png`.
- Persist generation metadata (`seed`, `model_id`, `lora_path`, `strength`, `guidance_scale`).

### 2) Per-page images with reference

- Use img2img with `character_base.png` as the reference image.
- Use page-specific scene prompt + shared character descriptor.
- Keep denoise strength moderate (for example `0.35-0.55`) to preserve appearance.

### 3) Consistency tips

- Reuse the same LoRA checkpoint for all pages.
- Lock a style suffix (for example watercolor children's book style).
- Keep negative prompt stable across all pages.

## Cost expectations

- **Local**: no API fee, but requires compatible GPU and enough VRAM.
- **Cloud**: pay by GPU runtime.
- **Hosted APIs**: easy setup, usually pay per image/request.
