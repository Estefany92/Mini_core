"""
MODEL (Modelo)
==============
Capa de Modelo del patrón MVC. Aquí se definen las entidades de datos
(Repartidor, Zona, Envio) usando Flask-SQLAlchemy como ORM.

Esta capa NO sabe nada de HTTP, formularios ni HTML. Su única
responsabilidad es representar y persistir los datos.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Zona(db.Model):
    """Tabla: Zonas -> zona de entrega y su tarifa por kg."""
    __tablename__ = "zonas"

    id_zona = db.Column(db.Integer, primary_key=True)
    nombre_zona = db.Column(db.String(50), nullable=False)
    tarifa_por_kg = db.Column(db.Numeric(10, 2), nullable=False)

    envios = db.relationship("Envio", backref="zona", lazy=True)

    def __repr__(self):
        return f"<Zona {self.nombre_zona} (${self.tarifa_por_kg}/kg)>"


class Repartidor(db.Model):
    """Tabla: Repartidor -> persona que realiza los envíos."""
    __tablename__ = "repartidores"

    id_repartidor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)

    envios = db.relationship("Envio", backref="repartidor", lazy=True)

    def __repr__(self):
        return f"<Repartidor {self.nombre}>"


class Envio(db.Model):
    """Tabla: Envios -> un paquete enviado por un repartidor a una zona."""
    __tablename__ = "envios"

    id_envio = db.Column(db.Integer, primary_key=True)
    id_repartidor = db.Column(
        db.Integer, db.ForeignKey("repartidores.id_repartidor"), nullable=False
    )
    id_zona = db.Column(db.Integer, db.ForeignKey("zonas.id_zona"), nullable=False)
    peso_kg = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_envio = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Envio {self.id_envio} - {self.peso_kg}kg - {self.fecha_envio}>"
