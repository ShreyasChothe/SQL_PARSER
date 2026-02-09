# main.py
import logging
from utils.file_handler import FileHandler
from utils.output_handler import OutputHandler
from engine.validator import ValidatorEngine
from engine.exceptions import SQLError

# Initialize your logging here
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SQLValidator")

def run_validator(input_source):
    print(f"\n--- Process started for: {input_source} ---")
    
    # 1. Get the Data
    raw_sql = FileHandler.read(input_source)
    if not raw_sql:
        print("❌ Error: File is empty or not found.")
        return

    # 2. Validate (The "Clean" Way)
    result = ValidatorEngine.validate(raw_sql)

    # 3. Handle Results & Save Report
    OutputHandler.save_report(result)

    if isinstance(result, SQLError):
        print(f"❌ FAILED: {result.message} (Line: {result.line}, Col: {result.column})")
        logger.error(f"Validation failed for {input_source}")
    else:
        print(f"✅ PASSED: SQL is grammatically correct.")
        logger.info(f"Validation successful for {input_source}")

if __name__ == "__main__":
    # You can now run multiple tests cleanly
    test_queries = [
        "SELECT * FROM users;",
        "UPDATE employees SET salary = 5000 WHERE id = 1;",
        "SELECT name FROM (SELECT * FROM staff);"
    ]

    for query in test_queries:
        run_validator(query)