python# core/reporter.py
# KYRI.IA — Módulo de Cierre de Caja Inteligente
# Socio: construido para ser el reporte que ningún otro sistema da

import json
import os
from datetime import datetime

class KyriReporter:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.state = self._load_json("state.json")
        self.config = self._load_json("config.json")
        self.products = self._load_json("products.json")

    def _load_json(self, filename: str) -> dict:
        path = os.path.join("tenants", self.tenant_id, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def _save_state(self):
        path = os.path.join("tenants", self.tenant_id, "state.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def generar_reporte_cierre(self) -> str:
        now = datetime.now()
        fecha = now.strftime("%A %d %b %Y").capitalize()
        hora = now.strftime("%I:%M %p")

        productos = self.state.get("products", {})
        business_name = self.state.get("business_name", self.tenant_id)
        meta_diaria = self.config.get("daily_goal", 0)

        # ── VENTAS ──────────────────────────────────────────
        total_ingresos = 0
        total_costo = 0
        total_ganancia = 0
        ventas_por_producto = []

        for pid, p in productos.items():
            vendidos = p.get("sold", 0)
            precio = p.get("price", 0)
            costo = p.get("cost", 0)
            ingreso = vendidos * precio
            ganancia = vendidos * (precio - costo)
            total_ingresos += ingreso
            total_costo += vendidos * costo
            total_ganancia += ganancia
            if vendidos > 0:
                ventas_por_producto.append({
                    "nombre": p.get("name", pid),
                    "vendidos": vendidos,
                    "ingreso": ingreso,
                    "ganancia": ganancia
                })

        ventas_por_producto.sort(key=lambda x: x["ingreso"], reverse=True)
        margen = (total_ganancia / total_ingresos * 100) if total_ingresos > 0 else 0

        # ── STOCK CRÍTICO ────────────────────────────────────
        stock_critico = []
        stock_advertencia = []
        for pid, p in productos.items():
            stock = p.get("stock", 0)
            sold = p.get("sold", 0)
            nombre = p.get("name", pid)
            # Proyección: días restantes al ritmo actual
            dias_restantes = round(stock / sold, 1) if sold > 0 else 999
            if stock <= 5:
                stock_critico.append(f"🔴 {nombre} — {stock} uds (se agota en {dias_restantes} días)")
            elif stock <= 15:
                stock_advertencia.append(f"🟡 {nombre} — {stock} uds (quedan ~{dias_restantes} días)")

        # ── META DEL DÍA ─────────────────────────────────────
        if meta_diaria > 0:
            pct_meta = (total_ingresos / meta_diaria) * 100
            if pct_meta >= 100:
                meta_txt = f"✅ Meta cumplida ({pct_meta:.1f}%)"
            elif pct_meta >= 80:
                meta_txt = f"🟡 Cerca de la meta ({pct_meta:.1f}%)"
            else:
                meta_txt = f"🔴 Meta no alcanzada ({pct_meta:.1f}%)"
        else:
            meta_txt = "⚙️ Sin meta configurada"

        # ── SALUD DEL NEGOCIO ────────────────────────────────
        salud_emoji = "🟢" if margen >= 30 else ("🟡" if margen >= 15 else "🔴")
        if margen >= 30:
            salud_msg = "Negocio saludable. Margen sólido."
        elif margen >= 15:
            salud_msg = "Margen ajustado. Revisa costos de productos con menor rentabilidad."
        else:
            salud_msg = "Margen crítico. Urge revisar precios o reducir costos."

        # ── INSIGHT KYRI (la IA habla) ───────────────────────
        insight = self._generar_insight(ventas_por_producto, stock_critico, margen, meta_diaria, total_ingresos)

        # ── CONSTRUIR MENSAJE ────────────────────────────────
        separador = "─" * 28

        msg = f"""
📊 *CIERRE DEL DÍA — {business_name.upper()}*
📅 {fecha} | {hora}
{separador}

💰 *RESUMEN DE VENTAS*
├ Ingresos totales: *${total_ingresos:,.0f}*
├ Costo de ventas: ${total_costo:,.0f}
├ Ganancia neta: *${total_ganancia:,.0f}*
├ Margen: {salud_emoji} {margen:.1f}%
└ {meta_txt}
{separador}"""

        # Top productos
        if ventas_por_producto:
            msg += "\n\n🛒 *PRODUCTOS DEL DÍA*"
            medallas = ["🥇", "🥈", "🥉"]
            for i, p in enumerate(ventas_por_producto[:5]):
                med = medallas[i] if i < 3 else "  •"
                msg += f"\n{med} {p['nombre']} — {p['vendidos']} uds / ${p['ingreso']:,.0f}"
            msg += f"\n{separador}"

        # Stock crítico
        if stock_critico or stock_advertencia:
            msg += "\n\n⚠️ *STOCK*"
            for s in stock_critico:
                msg += f"\n{s}"
            for s in stock_advertencia:
                msg += f"\n{s}"
            msg += f"\n{separador}"

        # Salud del negocio
        msg += f"\n\n📈 *SALUD DEL NEGOCIO*"
        msg += f"\n{salud_emoji} {salud_msg}"
        msg += f"\n{separador}"

        # KYRI habla
        msg += f"\n\n🤖 *KYRI dice:*"
        msg += f"\n_{insight}_"
        msg += f"\n{separador}"
        msg += f"\n✅ _Sistema activo. Próximo reporte: mañana al cierre._"

        # Guardar en state
        self.state["last_report"] = msg
        self._save_state()

        return msg.strip()

    def _generar_insight(self, ventas, stock_critico, margen, meta, total):
        insights = []

        if ventas:
            top = ventas[0]
            insights.append(f"{top['nombre']} fue tu producto estrella hoy con ${top['ingreso']:,.0f} en ventas.")

        if stock_critico:
            insights.append(f"Tienes {len(stock_critico)} producto(s) en stock crítico — revisa antes de abrir mañana.")

        if margen < 15:
            insights.append("El margen está muy ajustado. Considera revisar el precio de los productos con mayor rotación.")
        elif margen >= 30:
            insights.append("Excelente margen hoy. El negocio está siendo rentable.")

        if meta > 0 and total < meta * 0.8:
            falta = meta - total
            insights.append(f"Faltaron ${falta:,.0f} para la meta. Mañana es una nueva oportunidad.")

        return " ".join(insights) if insights else "Día registrado correctamente