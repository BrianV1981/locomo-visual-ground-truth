# Scripts Directory

This directory contains the Python toolkit used to build and maintain the visual ground truth repository.

### Contents
*   **`download_images.py`**: Sweeps the internet to download, downscale, and archive alive URLs while flagging 404s.
*   **`generate_matrix.py`**: Parses the conversation trees to map every image URL to its referencing question.
*   **`extract_llava_cache.py`**: The VLM prompt script used to iterate over the local image archive and extract rich OCR descriptions into the `caches/` directory.
*   **`generate_ocr_cache.py`**: One-shot Ollama cache builder for any vision model. Run it with any Ollama model name to generate a cache file in `../caches/`.

### Quick Start — Contribute a Model Cache
```bash
# 1. Pull your model
ollama pull qwen2.5vl:3b

# 2. Generate the cache (expects Ollama running on localhost:11434)
python scripts/generate_ocr_cache.py qwen2.5vl:3b

# 3. The cache lands in caches/qwen25vl_3b_cache.json
```
