# Data Directory

This directory contains the original LoCoMo V1 dataset (`locomo10.json`), forensically partitioned by its multimodal dependency to prevent link-rot vulnerabilities.

### Contents
*   **`locomo10.json`**: The original, unpartitioned Snap Research dataset.
*   **`locomo_pure_text.json`**: (1,251 questions) Guaranteed to have no images in their evidence chain.
*   **`locomo_verifiable_image.json`**: (653 questions) Evidence relies *only* on the 775 surviving, live image URLs.
*   **`locomo_dead_image.json`**: (82 questions) Evidence relies on permanently dead links. These questions are flagged for replacement in the V2 benchmark.
