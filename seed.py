from database import SessionLocal, engine, Base
from models import User, Colaborador, Proveedor, Actividad
from auth import get_password_hash
from datetime import date

db = SessionLocal()

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# --- USUARIOS ---
if not db.query(User).filter_by(email="admin@jht.com").first():
    admin = User(email="admin@jht.com", hashed_password=get_password_hash("admin123"), role="admin")
    db.add(admin)
else:
    admin = db.query(User).filter_by(email="admin@jht.com").first()

if not db.query(User).filter_by(email="conductor@jht.com").first():
    conductor = User(email="conductor@jht.com", hashed_password=get_password_hash("demo123"), role="conductor")
    db.add(conductor)
else:
    conductor = db.query(User).filter_by(email="conductor@jht.com").first()

db.commit()  # Para obtener los IDs

# --- COLABORADORES ---
colabs_data = ["ABEL", "LLIUYACC EDISON", "SANCHEZ TEODORO"]
for nombre in colabs_data:
    if not db.query(Colaborador).filter_by(nombre=nombre).first():
        db.add(Colaborador(nombre=nombre))

# --- PROVEEDORES ---
provs_data = ["LUBRICENTRO A&J", "SERVICENTRO ARO S.A.C.", "LUBRICANTES A&J"]
for nombre in provs_data:
    if not db.query(Proveedor).filter_by(nombre=nombre).first():
        db.add(Proveedor(nombre=nombre))

# --- ACTIVIDADES ---
actividades = [
    {
        "nombre": "ABEL",
        "actividad": "CAMBIO DE ACEITE DE CORONA Y CAJA",
        "prioridad": 5,
        "placa": "Y1F",
        "a_cargo": "LUBRICENTRO A&J",
        "fecha_atencion": date(2023, 11, 11),
        "avance": 5,
        "estado": "CONCLUIDO",
        "observaciones": "",
        "file_path": "uploads/foto1.jpg",
    },
    {
        "nombre": "LLIUYACC EDISON",
        "actividad": "CAMBIO DE FOCO",
        "prioridad": 4,
        "placa": "BLW",
        "a_cargo": "",
        "fecha_atencion": date(2024, 3, 2),
        "avance": 4,
        "estado": "CONCLUIDO",
        "observaciones": "",
        "file_path": "uploads/foto2.jpg",
    },
    {
        "nombre": "SANCHEZ TEODORO",
        "actividad": "Mantenimiento General Unidad D0J 943",
        "prioridad": 4,
        "placa": "D0J",
        "a_cargo": "SERVICENTRO ARO S.A.C.",
        "fecha_atencion": date(2024, 3, 4),
        "avance": 4,
        "estado": "CONCLUIDO",
        "observaciones": "CAMBIO DE ACEITES Y FILTROS",
        "file_path": "uploads/foto3.jpg",
    }
]

for act_data in actividades:
    existe = db.query(Actividad).filter_by(nombre=act_data["nombre"], actividad=act_data["actividad"]).first()
    if not existe:
        act = Actividad(**act_data, user_id=conductor.id)
        db.add(act)

db.commit()
db.close()

print("✅ Base de datos precargada con éxito.")

# uvicorn main:app --reload
#flutter run -d web-server
#curl -X POST http://localhost:8000/login -H "accept: application/json" -H "Content-Type: application/json" -d "{\"email\": \"admin@jht.com\", \"password\": \"admin123\"}"
#curl -X POST http://localhost:8000/login -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin@jht.com&password=admin123"
#cd proyecto2/backend
# https://bfastapipostgresql.onrender.com/docs

# proyecto2\backend


#admin@jht.com
#admin123

#conductor@jht.com
#demo123
