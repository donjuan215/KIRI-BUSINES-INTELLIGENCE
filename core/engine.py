from core.rules_loader import load_rules
from core.state import load_state, save_state
from core.actions import execute


class Engine:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self.rules = load_rules(tenant_id)
        self.state = load_state(tenant_id)

    def handle_event(self, event_name, payload=None):
        print(f"[ENGINE][{self.tenant_id}] Evento recibido: {event_name}")

        event_rules = self.rules.get(event_name, {})
        actions = event_rules.get("actions", [])

        for action in actions:
            execute(action, self.tenant_id, self.state, payload)

        save_state(self.tenant_id, self.state)