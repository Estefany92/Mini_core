"""
APP / ROUTING (parte del Controller en Flask)
==============================================
En Flask, las "rutas" (@app.route) son las que reciben la petición HTTP,
leen los datos del formulario, llaman a la lógica de negocio (controllers.py)
y le pasan el resultado a la Vista (templates/index.html) con render_template.

Flujo de una petición:
    Usuario llena el formulario -> POST "/"
      -> app.py (ruta) lee fecha_inicio y fecha_fin
      -> controllers.py calcula los costos (consulta el Modelo)
      -> app.py renderiza templates/index.html con los resultados (Vista)
"""

import os
from datetime import datetime

from flask import Flask, render_template, request

from models import db
from controllers import calcular_costos_por_repartidor
from seed_data import seed_if_empty


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    # DATABASE_URL la puede inyectar Render (p. ej. si usas Postgres);
    # si no existe, cae en SQLite local como hasta ahora.
    db_url = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'logistica.db')}"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Crea las tablas y siembra los datos de ejemplo si aún no existen.
    # Esto reemplaza tener que correr `python seed_data.py` a mano,
    # algo que no se puede hacer en el servidor de Render.
    with app.app_context():
        seed_if_empty()

    @app.route("/", methods=["GET", "POST"])
    def index():
        resultados = None
        fecha_inicio_str = ""
        fecha_fin_str = ""
        error = None

        if request.method == "POST":
            fecha_inicio_str = request.form.get("fecha_inicio", "")
            fecha_fin_str = request.form.get("fecha_fin", "")

            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

                if fecha_inicio > fecha_fin:
                    error = "La Fecha Inicio no puede ser posterior a la Fecha Fin."
                else:
                    resultados = calcular_costos_por_repartidor(fecha_inicio, fecha_fin)
            except (ValueError, TypeError):
                error = "Debes ingresar ambas fechas en un formato válido."

        return render_template(
            "index.html",
            resultados=resultados,
            fecha_inicio=fecha_inicio_str,
            fecha_fin=fecha_fin_str,
            error=error,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
