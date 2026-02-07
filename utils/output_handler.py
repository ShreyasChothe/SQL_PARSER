import json
import csv
from pathlib import Path

class OutputHandler:
    
    @staticmethod
    def save_txt(filename: str, content: str):
        path = Path(filename)
        path.write_text(content, encoding="utf-8")
    
    @staticmethod
    def save_json(filename: str, data):
        path = Path(filename)
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def save_csv(filename: str, data: list):
        """
        data: list of dicts or list of lists
        """
        path = Path(filename)
        if not data:
            return
        
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
