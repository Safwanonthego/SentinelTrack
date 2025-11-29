# SentinelTrack

## Quick start

1. Create a virtualenv and install dependencies:
```
python3 -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip3 install -r requirements.txt
```

2. Start the API server:
```
python3 -m uvicorn api.main:app --reload --port 57940
```

3. In another terminal, use the CLI:
```
source venv/bin/activate # or venv\Scripts\activate on Windows

python3 cli/sentineltrack.py add
python3 cli/sentineltrack.py list
python3 cli/sentineltrack.py list <ID>
python3 cli/sentineltrack.py update <ID>
python3 cli/sentineltrack.py delete <ID>
```

