import json
import csv
import os

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_turn_map(conversation):
    turn_map = {}
    for i in range(1, 100):
        session_key = f'session_{i}'
        if session_key not in conversation:
            break
        for turn in conversation[session_key]:
            if 'dia_id' in turn:
                turn_map[turn['dia_id']] = turn
    return turn_map

def main():
    alive_urls = set(load_json('../maps/alive_urls.json'))
    dead_urls = set(load_json('../maps/dead_urls.json'))
    locomo_data = load_json('../data/locomo10.json')
    
    rows = []
    
    for d in locomo_data:
        dialogue_id = d.get('sample_id', 'unknown')
        conv = d.get('conversation', {})
        turn_map = build_turn_map(conv)
        
        for qa in d.get('qa', []):
            question = qa.get('question', '')
            if isinstance(question, dict):
                question = question.get('text', str(question))
            category = qa.get('category', '')
            evidence_list = qa.get('evidence', [])
            
            qa_images = []
            
            for ev in evidence_list:
                turn = turn_map.get(ev)
                if not turn: continue
                urls = turn.get('img_url', [])
                if urls and isinstance(urls, list) and urls[0]:
                    url = urls[0]
                    is_dead = url in dead_urls or url not in alive_urls
                    qa_images.append({
                        'url': url,
                        'evidence_id': ev,
                        'status': 'Dead' if is_dead else 'Alive'
                    })
            
            if not qa_images:
                rows.append([dialogue_id, question, category, ", ".join(evidence_list), "None", "Text-Only"])
            else:
                for img in qa_images:
                    rows.append([dialogue_id, question, category, img['evidence_id'], img['url'], img['status']])
                    
    matrix_path = '../maps/question_image_matrix.csv'
    with open(matrix_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Dialogue ID', 'Question', 'Category', 'Evidence ID', 'Image URL', 'Status'])
        writer.writerows(rows)
        
    print(f"Generated {matrix_path} with {len(rows)} rows.")
    
    # Also, let's find the unused alive images!
    # All alive images:
    used_alive_urls = set(row[4] for row in rows if row[5] == 'Alive')
    unused_alive_urls = alive_urls - used_alive_urls
    
    print(f"Total Alive URLs: {len(alive_urls)}")
    print(f"Used Alive URLs (in questions): {len(used_alive_urls)}")
    print(f"Unused Alive URLs (available for new questions): {len(unused_alive_urls)}")
    
    # Write unused alive URLs to a file to help with generating new questions
    unused_list = list(unused_alive_urls)
    with open('../maps/unused_alive_urls.json', 'w') as f:
        json.dump(unused_list, f, indent=4)
        
    print(f"Saved {len(unused_list)} unused alive URLs to unused_alive_urls.json")

if __name__ == '__main__':
    main()