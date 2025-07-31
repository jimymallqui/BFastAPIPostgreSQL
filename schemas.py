from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str
    role: str
    class Config:
        from_attributes = True

class ActividadBase(BaseModel):
    nombre: str
    actividad: str
    prioridad: int
    placa: str
    a_cargo: str
    fecha_atencion: str
    avance: int
    estado: str
    observaciones: str = ""

class ActividadCreate(ActividadBase):
    pass

class Actividad(ActividadBase):
    id: int
    foto_url: str
    class Config:
        from_attributes = True

class ProveedorCreate(BaseModel):
    nombre: str

class Proveedor(ProveedorCreate):
    id: int
    class Config:
        from_attributes = True

class ColaboradorCreate(BaseModel):
    nombre: str

class Colaborador(ColaboradorCreate):
    id: int
    class Config:
        from_attributes = True