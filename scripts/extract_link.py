import os
import requests
from bs4 import BeautifulSoup
import time
import csv

save_dir = "D://president"
os.makedirs(save_dir, exist_ok=True)

csv_file_path = os.path.join(save_dir, "clinton_links.csv")

base_url = "https://www.presidency.ucsb.edu/advanced-search"
headers = {
    "User-Agent": "Mozilla/5.0"
}

all_bush_links = []

for page in range(10):
    params = {
        "person2": "200298",
        "category2[]": ["73", "74", "52", "46", "45", "65", "64", "49"],
        "items_per_page": "50",
        "page": page
    }

    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    all_a_tags = soup.find_all("a")

    for a in all_a_tags:
        href = a.get("href", "")
        if href.startswith("/documents/"):
            title = a.get_text(strip=True)
            full_link = "https://www.presidency.ucsb.edu" + href
            all_bush_links.append((title, full_link))

    print(f"Page {page + 1} extracted, current total: {len(all_bush_links)} items")
    time.sleep(1)


with open(csv_file_path, mode="w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Link"])
    writer.writerows(all_bush_links)

print(f"\nAll done, extracted a total of {len(all_bush_links)} speech links!")
print(f"File saved to: {csv_file_path}")

import csv

input_csv = r"D://president/clinton_links.csv"
output_csv = r"D://president/clinton_links_filtered.csv"

with open(input_csv, mode="r", encoding="utf-8") as infile, \
     open(output_csv, mode="w", newline='', encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        title = row["Title"]
        if "Guidebook" not in title and "Category Attributes" not in title:
            writer.writerow(row)

print(f"Filtering completed, saved to: {output_csv}")
