import csv
import requests
import os


class book_processing:

    def __init__(self, folder, csv_file):
        self.folder = folder
        self.csv_file = csv_file

    def download(self):
        os.makedirs(self.folder, exist_ok=True)
        with open(self.csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row["kindle_book"]
                filename = row["name"].replace(" ", "_") + ".mobi"  # filename from CSV
                path = os.path.join(self.folder, filename)

                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    with open(path, "wb") as book:
                        book.write(response.content)
                    print(f"Saved: {filename}")
                except Exception as e:
                    print(f"Failed: {url} | {e}")

    def remove_empty_files(self):
        for filename in os.listdir(self.folder):
            path = os.path.join(self.folder, filename)
            if os.path.isfile(path) and os.path.getsize(path) == 0:
                os.remove(path)
                print(f"Deleted empty file: {filename}")
