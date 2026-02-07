import os
import json
import csv
from pathlib import Path

# 🔹 Output directory constant
OUTPUT_DIR = Path("output")

# 🔹 Create folder automatically if not exists
OUTPUT_DIR.mkdir(exist_ok=True)


class OutputHandler:
    
    @staticmethod
    def save_txt(filename: str, content: str):
        # save inside output folder
        path = OUTPUT_DIR / filename
        path.write_text(content, encoding="utf-8")
        print(f"[Saved TXT] {path}")
    
    @staticmethod
    def save_json(filename: str, data):
        # save inside output folder
        path = OUTPUT_DIR / filename
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[Saved JSON] {path}")
    
    @staticmethod
    def save_csv(filename: str, data: list):
        """
        data: list of dicts or list of lists
        """
        if not data:
            return
        
        # save inside output folder
        path = OUTPUT_DIR / filename

        # determine headers
        if isinstance(data[0], dict):
            headers = data[0].keys()
        else:
            headers = [f"Column{i+1}" for i in range(len(data[0]))]
        
        with open(path, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in data:
                if isinstance(row, dict):
                    writer.writerow(row.values())
                else:
                    writer.writerow(row)

        print(f"[Saved CSV] {path}")
