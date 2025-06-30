import json
import re
import spacy
from tqdm import tqdm

# Loading spacy model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 10_000_000

# Setting file path
file_path = "/Users/lijiachen/Desktop/硕士/25 Spring/7.1 Text Analytics in the Digital Humanities/trump_merged.jsonl"

# Reading texts
all_text = ""
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        record = json.loads(line)
        all_text += " " + record['Text']

all_text = re.sub(r"[^\w\s]", "", all_text.lower())

# Splitting texts
def split_text(text, max_len=900_000):
    for i in range(0, len(text), max_len):
        yield text[i:i+max_len]

total_tokens = 0
content_words = 0
content_pos_tags = {'NOUN', 'VERB', 'ADJ', 'ADV'}

print("Processing text in chunks with progress bar...")
for chunk in tqdm(split_text(all_text), desc="Chunks processed"):
    doc = nlp(chunk)
    for token in doc:
        if token.is_alpha:
            total_tokens += 1
            if token.pos_ in content_pos_tags:
                content_words += 1

# Results
lexical_density = (content_words / total_tokens) * 100 if total_tokens > 0 else 0

print(f"Lexical Density：{lexical_density:.2f}%")
