from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import DateTime
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="conductor")

    actividades = relationship("Actividad", back_populates="user")

class Actividad(Base):
    __tablename__ = "actividades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)  # <-- Asegúrate de incluir esta línea
    actividad = Column(String, nullable=False)
    prioridad = Column(Integer)
    placa = Column(String)
    a_cargo = Column(String)
    fecha_atencion = Column(Date)
    avance = Column(Integer)
    estado = Column(String)
    observaciones = Column(String)
    file_path = Column(String)  # Imagen adjunta
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="actividades")

class Proveedor(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

class Colaborador(Base):
    __tablename__ = "colaboradores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)