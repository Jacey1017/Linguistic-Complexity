import os
import csv
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import json
from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0"
}

def crawl_csv_to_jsonl(csv_input_path, jsonl_output_path):
    links = []
    with open(csv_input_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            links.append((row["Title"], row["Link"]))

    with open(jsonl_output_path, mode="w", encoding="utf-8") as jsonlfile:
        # Iterate over all links with a progress bar
        for idx, (title, link) in enumerate(tqdm(links, desc=f"Extracting {os.path.basename(csv_input_path)}"), 1):
            try:
                response = requests.get(link, headers=headers)
                response.encoding = 'utf-8'
                if response.status_code != 200:
                    print(f"\nRequest failed for link {idx}, status code: {response.status_code}, skipping: {link}")
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                date_tag = soup.find(class_="date-display-single")
                if date_tag:
                    raw_date = date_tag.get_text(strip=True)
                    try:
                        date_obj = datetime.strptime(raw_date, "%B %d, %Y")
                        date = date_obj.strftime("%Y-%m-%d")
                    except Exception:
                        date = raw_date
                else:
                    date = "N/A"

                content_div = soup.find("div", class_="field-docs-content")
                if not content_div:
                    print(f"\nNo content section found for link {idx}, skipping: {link}")
                    continue

                paragraphs = [p.get_text(strip=True) for p in content_div.find_all("p") if p.get_text(strip=True)]
                full_text = "\n".join(paragraphs)

                record = {
                    "Title": title,
                    "Date": date,
                    "Text": full_text,
                    "Link": link
                }
                jsonlfile.write(json.dumps(record, ensure_ascii=False) + "\n")

                time.sleep(0.3)

            except Exception as e:
                print(f"\nError at link {idx}: {type(e).__name__} - {e}")

    print(f"\nFile {jsonl_output_path} completed!")

if __name__ == "__main__":
    save_dir = "D://president"
    tasks = [
        ("obama_links_filtered.csv", "obama_texts.jsonl"),
        ("biden_links_filtered.csv", "biden_texts.jsonl"),
        ("trump_links_filtered.csv", "trump_texts.jsonl"),
        ("trump2_links_filtered.csv", "trump2_texts.jsonl"),
    ]

    for csv_name, jsonl_name in tasks:
        csv_path = os.path.join(save_dir, csv_name)
        jsonl_path = os.path.join(save_dir, jsonl_name)
        crawl_csv_to_jsonl(csv_path, jsonl_path)

