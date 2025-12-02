from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.models import Vulnerability
from api.crud import get_all, get_one, create, update, delete

app = FastAPI(title="SentinelTrack", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def stat():
    return {"Status": "Ok"}

@app.get("/vulnerabilities")
def get_vulns():
    return get_all()

@app.get("/vulnerabilities/{id}")
def get_vuln(id : int):
    vuln = get_one(id)
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability Not Found")
    return vuln

@app.post("/vulnerabilities", status_code=201)
def create_vuln(vuln : Vulnerability):
    created = create(vuln)
    return created

@app.put("/vulnerabilities/{id}")
def update_vuln(id : int, vuln : Vulnerability):
    updated = update(id, vuln)
    if not updated:
        raise HTTPException(status_code=404, detail="Vulnerability Not Found")
    return updated

@app.delete("/vulnerabilities/{id}")
def delete_vuln(id : int):
    deleted = delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vulnerability Not Found")
    return {"deleted" : id}


