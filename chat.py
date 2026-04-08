import json
import os


def load_business_state(tenant_id):
    path = os.path.join("tenants", tenant_id, "state.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def chat():
    tenant_id = "store_001"
    print("💬 Chat del Negocio iniciado. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ").lower()

        if user_input == "salir":
            print("Chat cerrado.")
            break

        state = load_business_state(tenant_id)
        sales = state.get("sales", 0)
        insights = state.get("insights", [])

        if "ventas" in user_input:
            print(f"Sistema: Tus ventas totales son {sales}.")
            for ins in insights:
                print(f"Sistema: {ins}")

        else:
            print("Sistema: Puedo decirte cómo van tus ventas. Pregunta: '¿Cómo van mis ventas?'.")


if __name__ == "__main__":
    chat()