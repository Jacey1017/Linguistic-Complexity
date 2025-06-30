import json
import textstat
from tqdm import tqdm

# Setting file path
file_path = "/Users/lijiachen/Desktop/硕士/25 Spring/7.1 Text Analytics in the Digital Humanities/trump_merged.jsonl"

# Reading texts
texts = []
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        record = json.loads(line)
        texts.append(record["Text"])

fkgl_scores = []
print("Calculating FKGL scores...")
for text in tqdm(texts):
    try:
        score = textstat.flesch_kincaid_grade(text)
        if 0 <= score <= 20:
            fkgl_scores.append(score)
    except:
        continue

# Results
if fkgl_scores:
    avg_fkgl = sum(fkgl_scores) / len(fkgl_scores)
    print(f"Average Flesch-Kincaid Grade Level (FKGL): {avg_fkgl:.2f}")
else:
    print("No valid FKGL scores could be computed.")
