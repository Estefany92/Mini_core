# Mini Core — Costos de Envío por Repartidor (MVC con Flask)

Aplicación mínima que demuestra el patrón **MVC** resolviendo un problema
concreto de logística: dado un rango de fechas, calcular cuánto costó
cada repartidor según los kg enviados y la tarifa de la zona de entrega.

## ¿Cómo se ve el patrón MVC aquí?

| Capa | Archivo | Responsabilidad |
|------|---------|------------------|
| **Model** | `models.py` | Define `Repartidor`, `Zona`, `Envio` con Flask-SQLAlchemy. Solo estructura y persiste datos, no sabe nada de HTML ni de HTTP. |
| **Controller** | `controllers.py` + rutas en `app.py` | `controllers.py` contiene la regla de negocio (filtrar envíos por fecha, multiplicar peso × tarifa, sumar por repartidor). `app.py` recibe la petición HTTP, lee el formulario, llama al controlador y decide qué vista renderizar. |
| **View** | `templates/index.html` | Único template: formulario de fechas + tabla de resultados. Solo pinta lo que el Controller le entrega, no calcula nada. |

Flujo de una petición:

```
Usuario llena el formulario (Fecha Inicio / Fecha Fin)
        │  POST "/"
        ▼
app.py (Controller/routing) lee las fechas del form
        │
        ▼
controllers.py -> calcular_costos_por_repartidor(fecha_inicio, fecha_fin)
        │  consulta el Model (Repartidor, Envio, Zona)
        │  aplica: costo_envio = peso_kg * tarifa_por_kg de la zona
        │  suma por repartidor
        ▼
app.py renderiza templates/index.html (View) con los resultados
        ▼
Usuario ve la tabla: repartidor, envíos, kg, zona, tarifa, costo total
```

## Estructura del proyecto

```
mini_core/
├── app.py            # Entry point + rutas (Controller/routing de Flask)
├── controllers.py     # Lógica de negocio (Controller)
├── models.py           # Entidades Repartidor / Zona / Envio (Model)
├── seed_data.py         # Carga datos de ejemplo en la BD (SQLite)
├── requirements.txt
└── templates/
    └── index.html        # Formulario + tabla de resultados (View)
```

## Cómo ejecutarlo

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear la base de datos y cargar los datos de ejemplo (una sola vez)
python seed_data.py

# 3. Levantar la app
python app.py
```

Abre `http://127.0.0.1:5000/` en el navegador.

## Datos de ejemplo (seed) y resultado esperado

El seed crea 3 zonas, 4 repartidores y 11 envíos. Prueba el rango
**2025-05-01** a **2025-05-31**:

| Repartidor | Envíos | Total kg | Zona | Tarifa/kg | Costo Total |
|---|---|---|---|---|---|
| Andrés | 5 | 32 kg | Norte | $1.50 | **$48.00** |
| Camila | 3 | 18 kg | Sur | $2.00 | **$36.00** |
| Luis | 0 | — | — | — | No aplica *(su único envío es de junio, fuera del rango)* |
| Sofía | 2 | 18 kg | Norte, Centro | $1.50 / $1.75 | **$29.00** *(demuestra el cálculo cuando un repartidor envía a varias zonas: cada envío usa la tarifa de SU zona y luego se suman)* |

## Notas de diseño

- No hay CRUD ni formulario de ingreso de datos: los datos viven como
  seed en `seed_data.py`, tal como pide el enunciado.
- La base de datos es SQLite (`logistica.db`) para que el ejercicio sea
  autocontenido y no dependa de instalar un motor de BD aparte.
- `controllers.py` no importa nada de Flask ni de `render_template`:
  eso es intencional, para que la lógica de negocio quede separada de
  la capa web y sea fácil de leer/testear de forma aislada.
