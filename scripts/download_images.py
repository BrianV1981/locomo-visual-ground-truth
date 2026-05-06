import os
import json
import time
import requests
import io
import hashlib
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_filename_from_url(url):
    """Generate a unique filename for an image URL using MD5."""
    hash_obj = hashlib.md5(url.encode('utf-8'))
    return f"{hash_obj.hexdigest()}.jpg"

def process_image(url, output_dir):
    """Download, resize (max 1920x1080), strip alpha, and save as JPEG."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()

        img = Image.open(io.BytesIO(resp.content))
        
        # Resize preserving aspect ratio
        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        
        # Convert to RGB (removes alpha channel if PNG)
        img = img.convert("RGB")
        
        filename = get_filename_from_url(url)
        filepath = os.path.join(output_dir, filename)
        
        img.save(filepath, format="JPEG", quality=90)
        return url, filename, True, None
    except Exception as e:
        return url, None, False, str(e)

def main():
    print("🚀 Starting LoCoMo Image Preservation Download")
    
    with open('../maps/alive_urls.json', 'r', encoding='utf-8') as f:
        alive_urls = json.load(f)
        
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loaded {len(alive_urls)} URLs to download and process.")
    
    image_map = {}
    failed_urls = {}
    
    completed = 0
    total = len(alive_urls)
    
    # Check for existing images to support resuming
    existing_files = set(os.listdir(output_dir))
    urls_to_process = []
    
    for url in alive_urls:
        expected_filename = get_filename_from_url(url)
        if expected_filename in existing_files:
            image_map[url] = expected_filename
            completed += 1
        else:
            urls_to_process.append(url)
            
    print(f"Found {completed} already downloaded. {len(urls_to_process)} remaining.")
    
    if urls_to_process:
        print("Starting threaded download...")
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(process_image, url, output_dir): url for url in urls_to_process}
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                url, filename, success, error = future.result()
                
                completed += 1
                if success:
                    image_map[url] = filename
                else:
                    failed_urls[url] = error
                    
                print(f"Progress: {completed}/{total} | Success: {len(image_map)} | Failed: {len(failed_urls)}", end="\r", flush=True)
                
                # Periodically save mapping
                if completed % 50 == 0:
                    with open('../maps/image_map.json', 'w', encoding='utf-8') as f:
                        json.dump(image_map, f, indent=4)
                        
        print("\nDownload complete!")
        
    # Final save
    with open('../maps/image_map.json', 'w', encoding='utf-8') as f:
        json.dump(image_map, f, indent=4)
        
    if failed_urls:
        with open('../maps/failed_downloads.json', 'w', encoding='utf-8') as f:
            json.dump(failed_urls, f, indent=4)
        print(f"⚠️ {len(failed_urls)} images failed to download (saved to failed_downloads.json)")
        
    print(f"✅ Successfully mapped and saved {len(image_map)} images.")

if __name__ == "__main__":
    main()
