from sqlalchemy.orm import Session
import models
from fastapi import UploadFile
import shutil, os

def create_actividad(db: Session, data, user_id: int, file: UploadFile):
    path = f"uploads/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    actividad = models.Actividad(**data.dict(), user_id=user_id, foto_url=path)
    db.add(actividad)
    db.commit()
    db.refresh(actividad)
    return actividad

def get_actividades(db: Session, user):
    if user.role == "admin":
        return db.query(models.Actividad).all()
    return db.query(models.Actividad).filter(models.Actividad.user_id == user.id).all()

def get_all_actividades(db: Session):
    return db.query(models.Actividad).all()

def create_proveedor(db: Session, p):
    proveedor = models.Proveedor(**p.dict())
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor

def get_proveedores(db: Session):
    return db.query(models.Proveedor).all()

def create_colaborador(db: Session, c):
    colaborador = models.Colaborador(**c.dict())
    db.add(colaborador)
    db.commit()
    db.refresh(colaborador)
    return colaborador

def get_colaboradores(db: Session):
    return db.query(models.Colaborador).all()