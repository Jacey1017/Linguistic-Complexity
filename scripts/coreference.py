import re
import jsonlines
import time
from allennlp.predictors.predictor import Predictor
import allennlp_models.coref
from tqdm import tqdm
import os

PRONOUNS = {
    "i", "me", "you", "he", "she", "it", "we", "they",
    "him", "her", "us", "them", "his", "hers", "its", "ours", "theirs",
    "my", "your", "our", "their", "mine", "yours"
}


def split_text_to_paragraphs(text, max_tokens=500, tokenizer=None):
    sentences = re.split(r'(?<=[.!?]) +', text)
    paragraphs = []
    current_paragraph = []
    current_len = 0

    for sent in sentences:
        token_len = len(tokenizer.tokenize(sent)) if tokenizer else len(sent.split())
        if current_len + token_len > max_tokens and current_paragraph:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = [sent]
            current_len = token_len
        else:
            current_paragraph.append(sent)
            current_len += token_len

    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))
    return paragraphs


def analyze_text_in_chunks(text, predictor, tokenizer=None):
    paragraphs = split_text_to_paragraphs(text, max_tokens=500, tokenizer=tokenizer)

    total_mentions = 0
    total_tokens = 0
    total_chains = 0
    pronoun_chains = 0
    all_chain_lengths = []

    backward_distances = []

    for p in tqdm(paragraphs, desc="Analysis progress"):
        results = predictor.predict(document=p)
        clusters = results.get("clusters", [])
        doc_tokens = results.get("document", [])

        total_tokens += len(doc_tokens)
        total_chains += len(clusters)
        all_chain_lengths.extend([len(c) for c in clusters])
        total_mentions += sum(len(c) for c in clusters)

        for cluster in clusters:
            if any(
                    any(token.lower() in PRONOUNS for token in results["document"][start:end + 1])
                    for start, end in cluster
            ):
                pronoun_chains += 1

            for i in range(1, len(cluster)):
                curr_start = cluster[i][0]
                prev_start = cluster[i - 1][0]
                dist = curr_start - prev_start
                if dist > 0:
                    backward_distances.append(dist)

    avg_chain_length = (sum(all_chain_lengths) / total_chains) if total_chains > 0 else 0
    mention_coverage = (total_mentions / total_tokens) if total_tokens > 0 else 0
    pronoun_ratio = (pronoun_chains / total_chains) if total_chains > 0 else 0
    avg_backward_distance = (sum(backward_distances) / len(backward_distances)) if backward_distances else 0

    return {
        "num_chains": total_chains,
        "avg_chain_length": avg_chain_length,
        "mention_coverage": mention_coverage,
        "pronoun_ratio": pronoun_ratio,
        "avg_backward_distance": avg_backward_distance,
    }


def process_file(file_path, predictor):
    print(f"\n>>> Starting to process file: {file_path}")
    all_texts = []
    with jsonlines.open(file_path) as reader:
        for obj in tqdm(reader, desc="Reading text progress"):
            text = obj.get("Text", "").strip()
            if text:
                all_texts.append(text)
    full_text = "\n".join(all_texts)

    print("Starting coreference chain analysis...")
    metrics = analyze_text_in_chunks(full_text, predictor)

    print(f"\nAnalysis complete: {os.path.basename(file_path)}")
    print(f"Number of coreference chains: {metrics['num_chains']}")
    print(f"Average chain length: {metrics['avg_chain_length']:.2f}")
    print(f"Mention coverage: {metrics['mention_coverage']:.2%}")
    print(f"Ratio of chains with pronouns: {metrics['pronoun_ratio']:.2%}")
    print(f"Average backward distance: {metrics['avg_backward_distance']:.2f} tokens")
    return metrics


def main():
    print("Loading coreference model (CPU only)...")
    predictor = Predictor.from_path(
        "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz",
        cuda_device=-1
    )

    files = [
        r"D:\president\texts\clinton_merged_sorted.jsonl"
    ]

    all_results = {}
    for f in files:
        try:
            metrics = process_file(f, predictor)
            all_results[os.path.basename(f)] = metrics
        except Exception as e:
            print(f"❌ Error processing file: {f}")
            print(e)
        print("Waiting 10 seconds before processing the next file...\n")
        time.sleep(10)

    print("\n📊 All files processed, results:")
    for filename, metrics in all_results.items():
        print(f"\n{filename}:")
        print(f"  Number of coreference chains: {metrics['num_chains']}")
        print(f"  Average length: {metrics['avg_chain_length']:.2f}")
        print(f"  Coverage: {metrics['mention_coverage']:.2%}")
        print(f"  Pronoun ratio: {metrics['pronoun_ratio']:.2%}")
        print(f"  Average backward distance: {metrics['avg_backward_distance']:.2f} tokens")

if __name__ == "__main__":
    main()

