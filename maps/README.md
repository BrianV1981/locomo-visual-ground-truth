# Maps Directory

This directory contains the forensic mapping matrices and URL triage lists used to sever the dataset's reliance on the live internet.

### Contents
*   **`question_image_matrix.csv`**: A master matrix linking every QA pair to its precise visual dependency.
*   **`image_map.json`**: The canonical map linking the original internet URLs to our locally preserved, downscaled image filenames.
*   **`alive_urls.json` / `dead_urls.json`**: The triage results from the internet sweep.
*   **`unused_alive_urls.json`**: The pool of active images used by the V2 benchmark to replace the 82 dead questions with conversation-locked replacements.
