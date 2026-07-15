"""
CONTROLLER (Controlador)
=========================
Capa de Controlador del patrón MVC. Aquí vive la LÓGICA DE NEGOCIO:
tomar un rango de fechas, consultar el Modelo, aplicar las reglas
del problema (peso_kg * tarifa_por_kg de la zona) y devolver un
resultado ya listo para que la Vista lo pinte.

El Controlador no genera HTML ni sabe nada del formato final;
solo produce estructuras de datos (listas/diccionarios) para la Vista.
"""

from models import Repartidor, Envio


def calcular_costos_por_repartidor(fecha_inicio, fecha_fin):
    """
    Regla de negocio principal del Mini Core:

    Para cada repartidor:
      1. Filtrar sus envíos con fecha_envio dentro de [fecha_inicio, fecha_fin].
      2. Por cada envío: costo_envio = peso_kg * tarifa_por_kg (de la zona del envío).
      3. costo_total del repartidor = suma de costo_envio de todos sus envíos del período.

    Si el repartidor tuvo envíos en varias zonas, cada envío se calcula
    con LA TARIFA DE SU PROPIA ZONA y luego se suman todos (no se promedia).

    Retorna una lista de diccionarios, uno por repartidor, ya lista para
    que la Vista (template) la recorra con un for.
    """
    repartidores = Repartidor.query.order_by(Repartidor.nombre).all()
    resultados = []

    for repartidor in repartidores:
        envios_periodo = (
            Envio.query.filter(
                Envio.id_repartidor == repartidor.id_repartidor,
                Envio.fecha_envio >= fecha_inicio,
                Envio.fecha_envio <= fecha_fin,
            )
            .all()
        )

        if not envios_periodo:
            resultados.append(
                {
                    "nombre": repartidor.nombre,
                    "cantidad_envios": 0,
                    "total_kg": 0.0,
                    "zonas": "—",
                    "tarifas": "—",
                    "costo_total": 0.0,
                }
            )
            continue

        total_kg = 0.0
        costo_total = 0.0
        zonas_vistas = []  # mantiene orden y evita duplicados
        detalle_tarifas = []

        for envio in envios_periodo:
            zona = envio.zona
            peso = float(envio.peso_kg)
            tarifa = float(zona.tarifa_por_kg)
            costo_total += peso * tarifa
            total_kg += peso

            if zona.nombre_zona not in zonas_vistas:
                zonas_vistas.append(zona.nombre_zona)
                detalle_tarifas.append(f"{zona.nombre_zona}: ${tarifa:.2f}/kg")

        resultados.append(
            {
                "nombre": repartidor.nombre,
                "cantidad_envios": len(envios_periodo),
                "total_kg": round(total_kg, 2),
                "zonas": ", ".join(zonas_vistas),
                "tarifas": " | ".join(detalle_tarifas),
                "costo_total": round(costo_total, 2),
            }
        )

    return resultados
