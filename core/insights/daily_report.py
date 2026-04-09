from datetime import datetime

def generate_daily_report(state, tenant_id):
    now = datetime.now()
    fecha = now.strftime("%d/%m/%Y")
    hora = now.strftime("%I:%M %p")

    # Si business_name no existe, usamos tenant_id como respaldo
    business_name = state.get("business_name", tenant_id)
    productos = state.get("products", {})
    meta_diaria = state.get("daily_goal", 0)

    total_ingresos = 0
    total_costo = 0
    total_ganancia = 0
    ventas_lista = []

    for pid, p in productos.items():
        vendidos = p.get("sold", 0)
        precio = p.get("price", 0)
        costo = p.get("cost", 0)
        
        ingreso = vendidos * precio
        costo_total_prod = vendidos * costo
        ganancia = ingreso - costo_total_prod
        
        total_ingresos += ingreso
        total_costo += costo_total_prod
        total_ganancia += ganancia
        
        if vendidos > 0:
            ventas_lista.append({
                "nombre": p.get("name", pid),
                "vendidos": vendidos,
                "ingreso": ingreso,
                "ganancia": ganancia
            })

    # Ordenar por ingresos de mayor a menor
    ventas_lista.sort(key=lambda x: x["ingreso"], reverse=True)
    
    # Cálculo de margen seguro
    margen = (total_ganancia / total_ingresos * 100) if total_ingresos > 0 else 0

    # Lógica de Meta
    if meta_diaria > 0:
        pct = (total_ingresos / meta_diaria) * 100
        if pct >= 100:
            meta_txt = f"Meta cumplida ({pct:.1f}%)"
        elif pct >= 75:
            meta_txt = f"Cerca ({pct:.1f}%)"
        else:
            meta_txt = f"No alcanzada ({pct:.1f}%)"
    else:
        meta_txt = "Sin meta configurada"

    # Análisis de Stock
    criticos = []
    advertencias = []
    for pid, p in productos.items():
        stock = p.get("stock", 0)
        sold = p.get("sold", 0)
        nombre = p.get("name", pid)
        
        # Evitar división por cero en proyección de días
        dias = round(stock / sold, 1) if sold > 0 else "∞"
        
        if stock <= 5:
            criticos.append(f"{nombre}: {stock} uds (~{dias} días)")
        elif stock <= 15:
            advertencias.append(f"{nombre}: {stock} uds (~{dias} días)")

    # Definición de Salud Financiera
    if margen >= 30:
        salud, consejo = "Saludable", "Margen sólido. Buen día."
    elif margen >= 15:
        salud, consejo = "Ajustado", "Margen bajo. Revisa costos."
    else:
        salud, consejo = "Crítico", "Margen muy bajo. Revisa precios urgente."

    # Construcción de Insights (KYRI)
    insights = []
    if ventas_lista:
        top = ventas_lista[0]
        insights.append(f"· {top['nombre']} lideró con ${top['ingreso']:,.0f}.")
    if criticos:
        insights.append(f"· {len(criticos)} producto(s) en stock crítico.")
    if meta_diaria > 0:
        if total_ingresos >= meta_diaria:
            insights.append("· Meta del día cumplida.")
        else:
            falta = meta_diaria - total_ingresos
            insights.append(f"· Faltaron ${falta:,.0f} para la meta.")
    
    if not insights:
        insights.append("· Día registrado correctamente.")

    # Formateo del Reporte Final
    sep = "-" * 26
    r = (
        f"CIERRE DEL DÍA - {business_name.upper()}\n"
        f"{fecha} | {hora}\n"
        f"{sep}\n\n"
        f"VENTAS\n"
        f"Ingresos totales: ${total_ingresos:,.0f}\n"
        f"Costo de ventas: ${total_costo:,.0f}\n"
        f"Ganancia neta:   ${total_ganancia:,.0f}\n"
        f"Margen:          {margen:.1f}%\n"
        f"Meta:            {meta_txt}\n"
        f"{sep}\n\n"
    )

    if ventas_lista:
        r += "PRODUCTOS DEL DÍA\n"
        for i, p in enumerate(ventas_lista[:5]):
            r += f"{i+1}. {p['nombre']} - {p['vendidos']} uds / ${p['ingreso']:,.0f}\n"
    else:
        r += "Sin ventas registradas hoy.\n"
    
    r += f"{sep}\n\n"

    if criticos or advertencias:
        r += "ALERTAS DE STOCK\n"
        for s in criticos: r += f"🔴 CRÍTICO: {s}\n"
        for s in advertencias: r += f"⚠️ AVISO: {s}\n"
        r += f"{sep}\n\n"

    r += f"SALUD: {salud}\n💡 {consejo}\n"
    r += f"{sep}\n\n"
    r += "KYRI dice:\n"
    r += "\n".join(insights) + "\n"
    r += f"{sep}\n"
    r += "Próximo reporte: mañana al cierre."

    return r.strip()