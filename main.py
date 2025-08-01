# main.py (actualizado)
from datetime import datetime
from sqlalchemy import inspect
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Proveedor, Colaborador, Actividad
from schemas import UserCreate, ProveedorCreate, ColaboradorCreate, ActividadCreate
from auth import get_current_user, authenticate_user, create_access_token
import shutil
import os
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request


app = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("\n🔴 Error de validación en la solicitud:")
    print(exc)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API activa. Usa /docs para ver la documentación."}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@app.post("/proveedores")
def create_proveedor(proveedor: ProveedorCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    nuevo = Proveedor(nombre=proveedor.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/proveedores")
def get_proveedores(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    return db.query(Proveedor).all()

@app.post("/colaboradores")
def create_colaborador(colaborador: ColaboradorCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    nuevo = Colaborador(nombre=colaborador.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/colaboradores")
def get_colaboradores(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    return db.query(Colaborador).all()

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.email,
        "role": current_user.role
    }

@app.post("/actividad/")
def create_actividad(
    actividad: str = Form(...),
    prioridad: int = Form(...),
    placa: str = Form(...),
    a_cargo: str = Form(...),
    fecha_atencion: str = Form(...),
    avance: int = Form(...),
    estado: str = Form(...),
    observaciones: str = Form(""),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        raise HTTPException(status_code=500, detail="Error guardando el archivo")

    try:
        fecha = datetime.strptime(fecha_atencion, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

    actividad_obj = Actividad(
        actividad=actividad,
        prioridad=prioridad,
        placa=placa,
        a_cargo=a_cargo,
        fecha_atencion=fecha,
        avance=avance,
        estado=estado,
        observaciones=observaciones,
        file_path=file_path,
        user_id=user.id
    )

    db.add(actividad_obj)
    db.commit()
    db.refresh(actividad_obj)

    return {"message": "Actividad creada correctamente", "id": actividad_obj.id}

@app.get("/mis_actividades")
def get_mis_actividades(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    actividades = db.query(Actividad).filter(Actividad.user_id == user.id).all()
    return [
        {
            "id": a.id,
            "actividad": a.actividad,
            "prioridad": a.prioridad,
            "placa": a.placa,
            "a_cargo": a.a_cargo,
            "fecha_atencion": a.fecha_atencion.strftime("%Y-%m-%d"),
            "avance": a.avance,
            "estado": a.estado,
            "observaciones": a.observaciones,
            "file_path": a.file_path
        } for a in actividades
    ]

@app.post("/crear_actividad")
def crear_actividad(
    nombre: str = Form(...),
    actividad: str = Form(...),
    prioridad: int = Form(...),
    placa: str = Form(...),
    a_cargo: str = Form(...),
    fecha_atencion: str = Form(...),
    avance: int = Form(...),
    estado: str = Form(...),
    observaciones: str = Form(""),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("⚠️ Datos recibidos:")
    print("actividad:", actividad)
    print("prioridad:", prioridad)
    print("archivo:", file.filename)
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    actividad_obj = Actividad(
        nombre=nombre,
        actividad=actividad,
        prioridad=prioridad,
        placa=placa,
        a_cargo=a_cargo,
        fecha_atencion=datetime.strptime(fecha_atencion, "%Y-%m-%d").date(),
        avance=avance,
        estado=estado,
        observaciones=observaciones,
        file_path=file_path,
        user_id=user.id
    )

    db.add(actividad_obj)
    db.commit()
    db.refresh(actividad_obj)
    return {"msg": "Actividad registrada", "id": actividad_obj.id}

@app.get("/debug/tables")
def list_tables(db: Session = Depends(get_db)):
    inspector = inspect(db.bind)
    return inspector.get_table_names()

@app.get("/debug/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(User).all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")