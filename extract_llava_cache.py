import json
import os
import re

def main():
    print("🚀 Extracting LLaVA transcriptions from generated flight recorders...")
    
    with open('locomo10.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    md_dir = '../benchmarks/locomo/data/flight_recorders'
    
    llava_cache = {}
    missing_count = 0
    
    for row in dataset:
        dialogue_id = row['sample_id']
        md_path = os.path.join(md_dir, f"{dialogue_id}.md")
        
        if not os.path.exists(md_path):
            print(f"  [!] Skipping {dialogue_id}, markdown not found (Wait for locomo_eval to finish).")
            continue
            
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        # The visual description format in the markdown is:
        # [2023-05-18 14:00:00] *[Visual Description of image shared by Caroline: A painting of a sunrise over a calm ocean...]*
        # We use a regex to capture everything after "shared by {speaker}: " up to the closing "]*"
        
        # Note: speaker names might contain spaces.
        pattern = r"\*\[Visual Description of image shared by [^:]+: (.*?)]\*"
        matches = re.findall(pattern, md_content, flags=re.DOTALL)
        
        # Extract all image URLs in order from the dataset
        img_urls_in_order = []
        conversation = row.get('conversation', {})
        for i in range(1, 100):
            session_key = f'session_{i}'
            if session_key not in conversation:
                break
            for turn in conversation[session_key]:
                img_urls = turn.get('img_url', [])
                if img_urls and isinstance(img_urls, list) and img_urls[0]:
                    img_urls_in_order.append(img_urls[0])
                    
        # Check if lengths match
        if len(matches) != len(img_urls_in_order):
            print(f"  [!] Warning: length mismatch in {dialogue_id}: {len(matches)} descriptions vs {len(img_urls_in_order)} URLs")
            
        # Map them back
        for url, desc in zip(img_urls_in_order, matches):
            if url not in llava_cache:
                llava_cache[url] = desc.strip()
            elif llava_cache[url] != desc.strip():
                # If the same image URL has different descriptions, we just keep the first one
                pass

    if llava_cache:
        out_path = 'llava_7b_cache.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(llava_cache, f, indent=4, ensure_ascii=False)
        print(f"✅ Successfully extracted and saved {len(llava_cache)} image descriptions to {out_path}.")
    else:
        print("⚠️ No descriptions extracted. Please ensure locomo_eval has finished generating the markdown files.")

if __name__ == '__main__':
    main()
