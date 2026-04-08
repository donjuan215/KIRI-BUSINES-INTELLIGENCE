import json

def load_rules(tenant_id):
    path = f"tenants/{tenant_id}/rules.json"
    with open(path, "r") as f:
        return json.load(f)