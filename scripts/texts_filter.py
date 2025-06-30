import os
import json

save_dir = "D://president"
input_files = [
    "obama_texts.jsonl"
]

keywords = ["interview", "news conference", "debate"]

def filter_jsonl(input_path, output_path, keywords):
    count = 0
    with open(input_path, mode="r", encoding="utf-8") as infile, \
         open(output_path, mode="w", encoding="utf-8") as outfile:
        for line in infile:
            try:
                data = json.loads(line)
                title = data.get("Title", "").lower()
                if any(kw in title for kw in keywords):
                    outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
                    count += 1
            except json.JSONDecodeError:
                continue
    print(f"Filtering complete: {os.path.basename(input_path)} → retained {count} records")

for filename in input_files:
    input_path = os.path.join(save_dir, filename)
    output_filename = filename.replace(".jsonl", "_filtered.jsonl")
    output_path = os.path.join(save_dir, output_filename)
    filter_jsonl(input_path, output_path, keywords)

