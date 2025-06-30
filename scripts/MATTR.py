import json
import re

# Setting file path
file_path = "/Users/lijiachen/Desktop/硕士/25 Spring/7.1 Text Analytics in the Digital Humanities/trump_merged.jsonl"

# Reading texts
all_text = ""
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        record = json.loads(line)
        all_text += " " + record['Text']

# Preprocessing texts
all_text = re.sub(r'[^\w\s]', '', all_text.lower())
tokens = all_text.split()

def compute_mattr(tokens, window_size=50):
    if len(tokens) < window_size:
        return len(set(tokens)) / len(tokens) if tokens else 0.0

    ttr_list = []
    for i in range(len(tokens) - window_size + 1):
        window = tokens[i:i + window_size]
        types = set(window)
        ttr = len(types) / window_size
        ttr_list.append(ttr)

    return sum(ttr_list) / len(ttr_list)

window_size = 50
mattr_score = compute_mattr(tokens, window_size)

# Results
print(f"MATTR（window size = {window_size}）：{mattr_score:.4f}")
