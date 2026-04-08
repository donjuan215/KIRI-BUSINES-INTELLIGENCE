from core.engine import Engine

# Crear instancia del negocio
store = Engine("store_001")

# Eventos de prueba
store.handle_event("system_started")

# Registrar venta con payload
store.handle_event("sale_registered", {"qty": 2})

# Chequeo diario
store.handle_event("daily_check")