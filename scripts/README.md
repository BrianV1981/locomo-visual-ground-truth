# Scripts Directory

This directory contains the Python toolkit used to build and maintain the visual ground truth repository.

### Contents
*   **`download_images.py`**: Sweeps the internet to download, downscale, and archive alive URLs while flagging 404s.
*   **`generate_matrix.py`**: Parses the conversation trees to map every image URL to its referencing question.
*   **`extract_llava_cache.py`**: The VLM prompt script used to iterate over the local image archive and extract rich OCR descriptions into the `caches/` directory.
