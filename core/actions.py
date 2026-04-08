def execute(action, tenant_id, state, payload=None):

    # -----------------------------
    # Sistema iniciado
    # -----------------------------
    if action == "log_start":
        business_name = state.get("business_name")

        if not business_name:
            state["business_name"] = tenant_id

        print(f"[ACTION][{tenant_id}] Sistema iniciado para {tenant_id}")

    # -----------------------------
    # Registrar venta
    # -----------------------------
    elif action == "log_sale":

        qty = 1
        if payload and "qty" in payload:
            qty = payload["qty"]

        state["sales"] = state.get("sales", 0) + qty

        print(
            f"[ACTION][{tenant_id}] Venta registrada. Total de ventas: {state['sales']}"
        )

    # -----------------------------
    # Buen rendimiento
    # -----------------------------
    elif action == "notify_good_sales":
        print("🟢 Buen rendimiento de ventas")

    # -----------------------------
    # Verificar si hubo ventas
    # -----------------------------
    elif action == "check_no_sales":
        sales = state.get("sales", 0)

        if sales == 0:
            from core.engine import Engine
            Engine(tenant_id).handle_event("no_sales")

    # -----------------------------
    # Alerta sin ventas
    # -----------------------------
    elif action == "alert_no_sales":
        from core.notifications.whatsapp_sender import send_whatsapp

        msg = f"🔴 {tenant_id}: No hubo ventas hoy"
        print(msg)

        send_whatsapp(msg)

        alerts = state.get("alerts", [])
        alerts.append(msg)
        state["alerts"] = alerts

    # -----------------------------
    # Generar insights
    # -----------------------------
    elif action == "generate_insights":
        from core.insights.basic import generate_insights

        insights = generate_insights(state)
        state["insights"] = insights

        for insight in insights:
            print(f"[INSIGHT] {insight}")

    # -----------------------------
    # Enviar reporte diario
    # -----------------------------
    elif action == "send_daily_report":
        from core.insights.daily_report import generate_daily_report
        from core.notifications.whatsapp_sender import send_whatsapp

        report = generate_daily_report(state, tenant_id)

        print(report)
        send_whatsapp(report)

    # -----------------------------
    # Acción desconocida
    # -----------------------------
    else:
        print(f"[WARNING] Acción no reconocida: {action}")