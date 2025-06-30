import json
import spacy
from tqdm import tqdm

# Loading spacy model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 15_000_000

# Setting file path
file_path = "/Users/lijiachen/Desktop/硕士/25 Spring/7.1 Text Analytics in the Digital Humanities/biden.jsonl"

all_text = ""
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        record = json.loads(line)
        all_text += " " + record['Text']

def split_text(text, max_len=900_000):
    for i in range(0, len(text), max_len):
        yield text[i:i + max_len]

total_words = 0
total_sentences = 0

print("Processing text in chunks...")
for chunk in tqdm(split_text(all_text), desc="Chunks processed"):
    doc = nlp(chunk)
    total_words += sum(1 for token in doc if token.is_alpha)
    total_sentences += sum(1 for sent in doc.sents)

asl = total_words / total_sentences if total_sentences > 0 else 0.0
print(f"Average Sentence Length (ASL)：{asl:.2f} words/sentence")
