import json
from pathlib import Path

# Defining Directories and File Path
BASE_DIR= Path(__file__).resolve().parents[1]
DATABASE_DIR= BASE_DIR / "Database"
DATABASE_FILE= DATABASE_DIR / "vulnData.json"

# Creating The Database Directory If Not Exists
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# Loads The Whole Database From The Json File
def load_db():
    if not DATABASE_FILE.exists():
        DATABASE_FILE.write_text("[]", encoding="utf-8")
        return[]

#   Load The DB. But If File Is Corrupt, Reset The File (Empty DB)
    try:
        return json.loads(DATABASE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        DATABASE_FILE.write_text("[]", encoding="utf-8")
        return[]

# Saves The Database Onto The Json file
def save_db(data):
    DATABASE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
