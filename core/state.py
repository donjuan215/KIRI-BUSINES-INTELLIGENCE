import json
import os

def load_state(tenant_id):
    path = f"tenants/{tenant_id}/state.json"
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_state(tenant_id, state):
    path = f"tenants/{tenant_id}/state.json"
    with open(path, "w") as f:
        json.dump(state, f, indent=2)