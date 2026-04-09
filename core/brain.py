import json

class Brain:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self.rules = self.load_rules()

    def load_rules(self):
        path = f"tenants/{self.tenant_id}/rules.json"
        with open(path, "r") as f:
            return json.load(f)

    def think(self, event_name, state):
        decisions = []

        for rule in self.rules:
            if rule["event"] != event_name:
                continue

            try:
                if eval(rule["condition"], {}, state):
                    decisions.append(rule["action"])
            except Exception as e:
                print(f"[RULE ERROR] {e}")

        return decisions
       