import stanza
import json
from tqdm import tqdm

# Initializing stanza pipeline
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse', use_gpu=False)

subordinate_deps = {'acl', 'acl:relcl', 'advcl', 'ccomp', 'xcomp'}

def get_subordinate_depth(word_id, head_map):
    max_depth = 0
    for dep_id, dep_rel in head_map.get(word_id, []):
        if dep_rel in subordinate_deps:
            child_depth = 1 + get_subordinate_depth(dep_id, head_map)
        else:
            child_depth = get_subordinate_depth(dep_id, head_map)
        max_depth = max(max_depth, child_depth)
    return max_depth

def compute_dependency_distance(sentence):
    distances = [abs(word.id - word.head) for word in sentence.words if word.head != 0]
    return sum(distances) / len(distances) if distances else 0

# Reading texts
file_path = "/Users/lijiachen/Desktop/硕士/25 Spring/7.1 Text Analytics in the Digital Humanities/trump_merged.jsonl"
all_text = ""
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        record = json.loads(line)
        all_text += " " + record['Text']

print("Parsing text...")
doc = nlp(all_text)

embedding_depths = []
dependency_distances = []

for sentence in tqdm(doc.sentences, desc="Processing sentences"):
    head_map = {}
    for word in sentence.words:
        head_map.setdefault(word.head, []).append((word.id, word.deprel))

    # Computing embedding depth
    max_depth = get_subordinate_depth(0, head_map)
    embedding_depths.append(max_depth)

    # Computing average dependency distance
    avg_distance = compute_dependency_distance(sentence)
    dependency_distances.append(avg_distance)

# Results
if embedding_depths:
    avg_embedding_depth = sum(embedding_depths) / len(embedding_depths)
    max_embedding_depth = max(embedding_depths)
else:
    avg_embedding_depth = max_embedding_depth = 0

if dependency_distances:
    avg_dependency_distance = sum(dependency_distances) / len(dependency_distances)
else:
    avg_dependency_distance = 0

print(f"Average Embedding Depth: {avg_embedding_depth:.2f}")
print(f"Max Embedding Depth: {max_embedding_depth}")
print(f"Average Dependency Distance: {avg_dependency_distance:.2f}")
