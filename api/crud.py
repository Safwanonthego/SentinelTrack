from api.database import load_db, save_db
from api.models import Vulnerability

#Functions:
#   set_id(db)
#   get_all()
#   get_one(id)
#   create(vuln)
#   update(id, vuln)
#   delete(id)

# Initializes The Id for The Vulnerabilities
def set_id(db):
    if not db:
        return 1
    return max(vuln.get("id",0) for vuln in db) + 1

# Gets All The Vulnerabilities
def get_all():
    return load_db()

# Gets One Specific Vulnerability
def get_one(id):
    db = load_db()
    for vuln in db:
        if vuln.get("id") == id:
            return vuln
    return None

# Create A New Vulnerability
def create(vuln):
    db = load_db()
    vuln_dict = vuln.dict()
    vuln_dict["id"] = set_id(db)
    db.append(vuln_dict)
    save_db(db)
    return vuln_dict

# Update An Existing Vulnerability
def update(id, vuln):
    db = load_db()
#   enumerate() is same as i=0 for v in db: #code i += 1
    for i, v in enumerate(db):
        if v.get("id") == id:
            new = vuln.dict()
            new["id"] = id
            db[i] = new
            save_db(db)
            return new
    return None

# Delete An Existing Vulnerability
def delete(id):
    db = load_db()
#   Creates A New DB Excluding The One With Similar ID
    new_db = [v for v in db if v.get("id") != id]
    if len(new_db) == len(db):
        return False
    save_db(new_db)
    return True






