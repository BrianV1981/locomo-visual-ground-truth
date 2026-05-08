#!/usr/bin/env python3
"""
Generate an OCR description cache for locomo-visual-ground-truth
using any Ollama vision model.

Usage:
    python generate_ocr_cache.py <ollama_model_name>

Example:
    python generate_ocr_cache.py qwen2.5vl:3b
    python generate_ocr_cache.py moondream:latest

Output:
    ../caches/<model_sanitized>_cache.json    e.g. ../caches/qwen25vl_3b_cache.json
"""
import argparse
import base64
import hashlib
import json
import os
import sys
import time

import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(REPO_ROOT, "images")
CACHES_DIR = os.path.join(REPO_ROOT, "caches")
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

PROMPT = (
    "Describe this image in detail, including any visible text, signage, "
    "objects, people, and setting."
)


def find_baseline_urls():
    """Pick the largest existing cache (by URL count) as the URL master list."""
    best_path, best_count = None, 0
    for fname in os.listdir(CACHES_DIR):
        if fname.endswith("_cache.json"):
            fpath = os.path.join(CACHES_DIR, fname)
            try:
                with open(fpath) as f:
                    urls = list(json.load(f).keys())
                if len(urls) > best_count:
                    best_path, best_count = fpath, len(urls)
            except Exception:
                continue
    if best_path is None:
        sys.exit("No existing cache found in caches/ — need at least one to source URLs.")
    with open(best_path) as f:
        return list(json.load(f).keys())


def build_url_to_path(urls):
    """Map each URL to its local image file via MD5(filename).jpg."""
    mapping = {}
    missing = 0
    for url in urls:
        fname = hashlib.md5(url.encode()).hexdigest() + ".jpg"
        fpath = os.path.join(IMAGES_DIR, fname)
        if os.path.exists(fpath):
            mapping[url] = fpath
        else:
            missing += 1
    print(f"Resolved {len(mapping)} images, {missing} missing")
    return mapping


def describe(model, image_path):
    b64 = base64.b64encode(open(image_path, "rb").read()).decode()
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": PROMPT,
            "images": [b64],
            "stream": False,
            "options": {"temperature": 0.1},
        },
        timeout=180,
    )
    return resp.json().get("response", "").strip()


def output_name(model):
    safe = model.replace(":", "_").replace("/", "_").replace(".", "")
    return f"{safe}_cache.json"


def main():
    parser = argparse.ArgumentParser(description="Generate OCR cache for any Ollama vision model")
    parser.add_argument("model", help="Ollama model name, e.g. qwen2.5vl:3b")
    parser.add_argument("--prompt", help="Custom prompt", default=None)
    parser.add_argument("--sleep", type=float, default=0.3, help="Pacing delay between images (default 0.3s)")
    parser.add_argument("--save-interval", type=int, default=50, help="Incremental save every N images")
    args = parser.parse_args()

    global PROMPT
    if args.prompt:
        PROMPT = args.prompt

    model = args.model
    out = output_name(model)
    out_path = os.path.join(CACHES_DIR, out)

    print(f"Model:  {model}")
    print(f"Output: {out_path}")

    urls = find_baseline_urls()
    url_map = build_url_to_path(urls)

    cache = {}
    if os.path.exists(out_path):
        with open(out_path) as f:
            cache = json.load(f)
        existing = sum(1 for v in cache.values() if v)
        print(f"Resuming: {existing} descriptions already cached, {len(cache)} total entries")

    pending = {}
    for url, fpath in url_map.items():
        if url in cache and cache[url]:
            continue
        pending[url] = fpath

    if not pending:
        print("All images already cached. Nothing to do.")
        return

    print(f"Processing {len(pending)} images...")
    total = len(pending)

    for i, (url, fpath) in enumerate(pending.items(), 1):
        print(f"[{i}/{total}] {os.path.basename(fpath)}", end=" ", flush=True)
        try:
            desc = describe(model, fpath)
            cache[url] = desc
            print(f"-> {desc[:80]}...")
        except Exception as e:
            print(f"-> ERROR: {e}")
            cache[url] = ""

        if i % args.save_interval == 0:
            with open(out_path, "w") as f:
                json.dump(cache, f, indent=2)
            print(f"  [saved {i}/{total}]")

        time.sleep(args.sleep)

    with open(out_path, "w") as f:
        json.dump(cache, f, indent=2)

    non_empty = sum(1 for v in cache.values() if v)
    print(f"\nDone. {non_empty}/{len(cache)} descriptions saved to {out_path}")


if __name__ == "__main__":
    main()
