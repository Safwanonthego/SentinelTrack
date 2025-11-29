import argparse
import requests
import json
from tabulate import tabulate

API = "http://127.0.0.1:57940"

TITLE_CYAN = lambda string : f"\033[1;96m {string} \033[0m"
ERROR_RED = lambda string : f"\033[1;31m {string} \033[0m"



def vuln_add():

    print("Enter Vulnerability Details:")
    title = input("Title: ")
    asset = input("Asset (IP/Hostname): ")
    description = input("Description: ")
    severity = input("Severity [Low/Medium/High/Critical]: ")
    steps = input("Steps To Reproduce: ")
    mitigation = input("Mitigation: ")
    status = input("Status [Open/Fixed/Accepted/False Positive]: ")

    vuln_data = {
        "title"         : title,
        "asset"         : asset,
        "description"   : description,
        "severity"      : severity,
        "steps"         : steps,
        "mitigation"    : mitigation,
        "status"        : status
    }

    r_post = requests.post(f"{API}/vulnerabilities", json=vuln_data)
    
    if r_post.status_code in (200,201):
        print("New Record Created:")
        data = r_post.json()
        table = []
        table.append([data.get("id"), data.get("title"), data.get("asset"), data.get("status")])
        print(tabulate(table, headers=["ID", "Title", "Asset", "Status"]))
    
    else:
        err_post = r_post.json()
        print(ERROR_RED(f"Error: {err_post.get('detail')} (Response {r_post.status_code})"))



def vuln_list():
    
    r_get = requests.get(f"{API}/vulnerabilities")
    
    if r_get.status_code !=200:
        err_get = r_get.json()
        print(ERROR_RED(f"Error: {err_get.get('detail')} (Response {r_get.status_code})"))
        return
    
    data = r_get.json()
    
    if not data:
        print("No Vulnerability Record Found")
        return
    
    data_val = []
    headers=[TITLE_CYAN("ID"), TITLE_CYAN("Title"), TITLE_CYAN("Asset"), TITLE_CYAN("Severity"), TITLE_CYAN("Status")]
    for vuln in data:
        data_val.append([vuln.get("id"), vuln.get("title"), vuln.get("asset"), vuln.get("severity"), vuln.get("status")])
    print(tabulate(data_val, headers, tablefmt="heavy_grid"))
    


def vuln_info(id):
    r_get = requests.get(f"{API}/vulnerabilities/{id}")
    
    if r_get.status_code != 200:
        err_get = r_get.json()
        print(ERROR_RED(f"Error: {err_get.get('detail')} (Response {r_get.status_code})"))
        return

    curr_data = r_get.json()
    
    headings = ["id", "title", "asset", "severity", "status", "description", "steps", "mitigation"]
    
    for info in headings:
        
        if info not in ("description", "steps", "mitigation"):
            print(f"{info.upper():<{13}}: {curr_data.get(info)}")
        
        else:
            print(f"\n\033[4m{info.upper():^{13}}\033[0m: \n{curr_data.get(info):>{10}}")



def vuln_update(id):
    
    r_get = requests.get(f"{API}/vulnerabilities/{id}")
    
    if r_get.status_code != 200:
        err_get = r_get.json()
        print(ERROR_RED(f"Error: {err_get.get('detail')} (Response {r_get.status_code})"))
        return
    
    curr_data = r_get.json()
    
    print("Leave Blank To Keep Current Value\n")
    
    def updated_val(prompt, curr_val):
        val = input(f"{prompt} [{curr_val}]: ")
        return val if val != "" else curr_val

    updated_vuln_data = {
        "title"         : updated_val("Title", curr_data.get("title", "")),
        "asset"         : updated_val("Asset", curr_data.get("asset", "")),
        "description"   : updated_val("Description", curr_data.get("description", "")),
        "severity"      : updated_val("Severity", curr_data.get("severity", "")),
        "steps"         : updated_val("Steps", curr_data.get("steps", "")),
        "mitigation"    : updated_val("Mitigation", curr_data.get("mitigation", "")),
        "status"        : updated_val("Status", curr_data.get("status", "")),
    }

    r_put = requests.put(f"{API}/vulnerabilities/{id}", json=updated_vuln_data)
    
    if r_put.status_code == 200:
        print(f"\nUpdated Record [ID {id}]:")
        data = r_put.json()
        table = []
        table.append([data.get("id"), data.get("title"), data.get("asset"), data.get("status")])
        print(tabulate(table, headers=["ID", "Title", "Asset", "Status"]))
    
    else:
        err_put = r_put.json()
        print(ERROR_RED(f"Error: {err_put.get('detail')} (Response {r_put.status_code})"))



def vuln_delete(id):
    
    r_delete = requests.delete(f"{API}/vulnerabilities/{id}")
    
    if r_delete.status_code == 200:
        print(f"\nDeleted Record [ID {id}]:")
    
    else:
        err_delete = r_delete.json()
        print(ERROR_RED(f"Error: {err_delete.get('detail')} (Response {r_delete.status_code})"))



def main():

    parser = argparse.ArgumentParser(prog="sentineltrack.py")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("add")
    
    listp = sub.add_parser("list")
    listp.add_argument("id", type=int, nargs='?', default=None)
    
    updtp = sub.add_parser("update")
    updtp.add_argument("id", type=int)

    deltp = sub.add_parser("delete")
    deltp.add_argument("id", type=int)


    args = parser.parse_args()

    match args.cmd:
        
        case "add":
            vuln_add()
        
        case "list":
            if args.id is not None:
                vuln_info(args.id)
            else:
                vuln_list()
        
        case "update":
            vuln_update(args.id)
        
        case "delete":
            vuln_delete(args.id)
        
        case _:
            parser.print_help()
        


if __name__ == "__main__":
    main()

