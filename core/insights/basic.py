def generate_insights(state):

    sales = state.get("sales", 0)
    profit = state.get("profit", 0)

    insights = []

    if sales == 0:
        insights.append("🔴 No hay ventas registradas aún.")

    elif sales < 5:
        insights.append("🟡 Ventas bajas hoy.")

    else:
        insights.append("🟢 Buen rendimiento de ventas.")

    insights.append(f"💰 Margen total: ${profit}")

    return insights