import json
import os

def load_jsonl(path):
    """Read a jsonl file into a list"""
    data = []
    if not os.path.exists(path):
        return data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def save_jsonl(path, data):
    """Save data as a jsonl file"""
    with open(path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def merge_and_sort_president_files(president_name):
    base_path = r"D:\president\texts"
    original_path = os.path.join(base_path, f"{president_name}_texts.jsonl")
    filtered_path = os.path.join(base_path, f"{president_name}_texts_filtered.jsonl")
    speech_path = os.path.join(base_path, f"{president_name}_speech_only.jsonl")
    output_path = os.path.join(base_path, f"{president_name}_merged_sorted.jsonl")

    print(f"Processing {president_name}...")

    original = load_jsonl(original_path)
    filtered = load_jsonl(filtered_path)
    speech = load_jsonl(speech_path)

    def key_fn(item):
        return (item.get("Title", ""), item.get("Date", ""))

    filtered_set = set(key_fn(item) for item in filtered)

    remaining = [item for item in original if key_fn(item) not in filtered_set]

    combined = speech + remaining

    combined_sorted = sorted(combined, key=lambda x: x.get("Date", ""))

    save_jsonl(output_path, combined_sorted)
    print(f"Completed: {output_path}\n")

presidents = ["biden", "trump", "trump2", "obama", "bush", "clinton"]

for name in presidents:
    merge_and_sort_president_files(name)

