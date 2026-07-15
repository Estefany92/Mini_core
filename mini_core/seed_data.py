"""
SEED DATA
=========
Crea las tablas (Model) y las llena con datos de ejemplo, para que
el Mini Core tenga algo que consultar sin necesidad de un CRUD.

Se puede usar de dos formas:
  1. A mano en local:      python seed_data.py
  2. Automático al arrancar la app (ver seed_if_empty(), llamado
     desde app.py) — esto es lo que se usa en producción/Render,
     porque el disco es efímero y no hay forma de correr un script
     manualmente ahí.
"""

from datetime import date

from models import db, Zona, Repartidor, Envio


def seed_if_empty():
    """Crea las tablas si no existen y siembra datos SOLO si la
    tabla de Zonas está vacía (evita duplicar datos en cada arranque)."""
    db.create_all()

    if Zona.query.first() is not None:
        return  # ya hay datos, no volver a sembrar

    _sembrar_datos()


def _sembrar_datos():
    # ---------- Zonas ----------
    norte = Zona(nombre_zona="Norte", tarifa_por_kg=1.50)
    sur = Zona(nombre_zona="Sur", tarifa_por_kg=2.00)
    centro = Zona(nombre_zona="Centro", tarifa_por_kg=1.75)
    db.session.add_all([norte, sur, centro])
    db.session.commit()

    # ---------- Repartidores ----------
    andres = Repartidor(nombre="Andrés", email="andres@logistica.com")
    camila = Repartidor(nombre="Camila", email="camila@logistica.com")
    luis = Repartidor(nombre="Luis", email="luis@logistica.com")
    sofia = Repartidor(nombre="Sofía", email="sofia@logistica.com")
    db.session.add_all([andres, camila, luis, sofia])
    db.session.commit()

    # ---------- Envíos ----------
    envios = [
        # Andrés: 5 envíos, todos en Norte, en mayo -> 32 kg, $48.00
        Envio(id_repartidor=andres.id_repartidor, id_zona=norte.id_zona,
              peso_kg=6, fecha_envio=date(2025, 5, 2)),
        Envio(id_repartidor=andres.id_repartidor, id_zona=norte.id_zona,
              peso_kg=7, fecha_envio=date(2025, 5, 5)),
        Envio(id_repartidor=andres.id_repartidor, id_zona=norte.id_zona,
              peso_kg=6, fecha_envio=date(2025, 5, 10)),
        Envio(id_repartidor=andres.id_repartidor, id_zona=norte.id_zona,
              peso_kg=8, fecha_envio=date(2025, 5, 20)),
        Envio(id_repartidor=andres.id_repartidor, id_zona=norte.id_zona,
              peso_kg=5, fecha_envio=date(2025, 5, 28)),

        # Camila: 3 envíos, todos en Sur, en mayo -> 18 kg, $36.00
        Envio(id_repartidor=camila.id_repartidor, id_zona=sur.id_zona,
              peso_kg=6, fecha_envio=date(2025, 5, 3)),
        Envio(id_repartidor=camila.id_repartidor, id_zona=sur.id_zona,
              peso_kg=5, fecha_envio=date(2025, 5, 15)),
        Envio(id_repartidor=camila.id_repartidor, id_zona=sur.id_zona,
              peso_kg=7, fecha_envio=date(2025, 5, 25)),

        # Sofía: 2 envíos EN DOS ZONAS distintas dentro de mayo
        # -> demuestra que el cálculo es por envío y luego se suma
        Envio(id_repartidor=sofia.id_repartidor, id_zona=norte.id_zona,
              peso_kg=10, fecha_envio=date(2025, 5, 8)),   # 10 * 1.50 = 15.00
        Envio(id_repartidor=sofia.id_repartidor, id_zona=centro.id_zona,
              peso_kg=8, fecha_envio=date(2025, 5, 19)),   # 8 * 1.75 = 14.00
        # Total Sofía en mayo: 2 envíos, 18 kg, costo = $29.00

        # Luis: solo tiene un envío, pero es de JUNIO (fuera del rango de mayo)
        # -> al filtrar mayo, Luis debe salir con 0 envíos / "No aplica"
        Envio(id_repartidor=luis.id_repartidor, id_zona=centro.id_zona,
              peso_kg=10, fecha_envio=date(2025, 6, 5)),
    ]
    db.session.add_all(envios)
    db.session.commit()

    print("Base de datos poblada con éxito: 3 zonas, 4 repartidores, "
          f"{len(envios)} envíos.")
    print("Prueba el rango 2025-05-01 a 2025-05-31 en la app.")


if __name__ == "__main__":
    # Permite seguir corriendo `python seed_data.py` a mano en local.
    from app import create_app

    app = create_app()
    with app.app_context():
        db.drop_all()
        seed_if_empty()
