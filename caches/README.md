# Caches Directory

This directory acts as the central hub for LoCoMo visual translations, allowing pure-text LLMs to evaluate the multimodal benchmark without requiring a vision encoder.

### Contents
*   **`llava_7b_cache.json`**: A comprehensive OCR and visual description mapping for all 821 active images in the dataset, generated using LLaVA-7B. 

*Developers can inject these descriptions into their text pipelines to completely bypass broken internet links and achieve true multimodal evaluation for $0 in API costs.*
