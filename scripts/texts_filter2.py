import json
import re
from tqdm import tqdm

def extract_trump_speech(text):

    pattern = re.compile(r'^([A-Z]+[a-z]*?(?: [A-Z]+[a-z]*?)*[.:])', re.MULTILINE)

    segments = pattern.split(text)

    trump_aliases = {"President Obama.", "The President.", "The President:", "President Obama:", "THE PRESIDENT:", "PRESIDENT OBAMA:", "OBAMA:"}
    trump_speech = []

    for i in range(1, len(segments), 2):
        speaker = segments[i].strip()
        content = segments[i + 1].strip() if i + 1 < len(segments) else ""

        if speaker in trump_aliases:
            for line in content.splitlines():
                line = line.strip()
                if line and re.search(r'[.!?]', line):
                    trump_speech.append(line)

    return "\n".join(trump_speech)

input_path = r"D:\president\texts\obama_texts_filtered.jsonl"
output_path = r"D:\president\texts\obama_speech_only.jsonl"

def count_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for i, _ in enumerate(f, 1):
            pass
    return i

total_lines = count_lines(input_path)

with open(input_path, "r", encoding="utf-8") as infile, \
     open(output_path, "w", encoding="utf-8") as outfile:

    for line_number, line in enumerate(tqdm(infile, total=total_lines, desc="Processing"), 1):
        data = json.loads(line)
        original_text = data.get("Text", "")

        trump_text = extract_trump_speech(original_text)

        if trump_text == "":
            print(f"Line {line_number} did not contain Trump speech")

        output_data = {
            "Title": data.get("Title", ""),
            "Date": data.get("Date", ""),
            "Text": trump_text,
            "Link": data.get("Link", "")
        }
        outfile.write(json.dumps(output_data, ensure_ascii=False) + '\n')



