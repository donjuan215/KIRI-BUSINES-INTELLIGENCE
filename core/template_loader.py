import json
import os
import shutil


def apply_template(template_path, tenant_id):
    tenant_path = os.path.join("tenants", tenant_id)
    os.makedirs(tenant_path, exist_ok=True)

    # Archivos destino
    rules_dest = os.path.join(tenant_path, "rules.json")
    state_dest = os.path.join(tenant_path, "state.json")

    # Cargar template
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)

    # Crear rules.json SOLO si no existe
    if not os.path.exists(rules_dest):
        with open(rules_dest, "w", encoding="utf-8") as f:
            json.dump(template.get("rules", {}), f, indent=2)

    # Crear state.json SOLO si no existe
    if not os.path.exists(state_dest):
        with open(state_dest, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

    print(f"[TEMPLATE] Template '{template.get('name')}' aplicado a {tenant_id}")