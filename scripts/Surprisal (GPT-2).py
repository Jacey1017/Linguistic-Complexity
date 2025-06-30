import jsonlines
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from tqdm import tqdm

# Loading GPT-2 and tokenizer
print("Loading GPT-2 model...")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def calculate_surprisal(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
    input_ids = inputs["input_ids"].to(device)

    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        log_likelihood = outputs.loss.item() * input_ids.size(1)

    surprisal = log_likelihood / input_ids.size(1)
    return surprisal, input_ids.size(1)

# Reading texts
input_path = "/Users/lijiachen/Desktop/硕士/25 Spring/7.1 Text Analytics in the Digital Humanities/obama.jsonl"
all_texts = []

with jsonlines.open(input_path) as reader:
    for obj in tqdm(reader):
        if "Text" in obj:
            text = obj["Text"].strip()
            if text:
                all_texts.append(text)

full_corpus = "\n".join(all_texts)

# Splitting texts
print("Splitting corpus into manageable chunks...")
tokens = tokenizer(full_corpus, return_tensors="pt")["input_ids"][0]
chunk_size = 1024
num_chunks = (len(tokens) + chunk_size - 1) // chunk_size

total_log_likelihood = 0.0
total_tokens = 0

print("Calculating surprisal across the full corpus...")
for i in tqdm(range(num_chunks)):
    chunk = tokens[i * chunk_size: (i + 1) * chunk_size].unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(chunk, labels=chunk)
        log_likelihood = outputs.loss.item() * chunk.size(1)
        total_log_likelihood += log_likelihood
        total_tokens += chunk.size(1)

# Results
average_surprisal = total_log_likelihood / total_tokens
print(f"Average Surprisal: {average_surprisal:.4f}")
