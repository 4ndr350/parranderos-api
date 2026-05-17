from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# os.environ para despliegue. Descomente cuando ya probo todo local.
client = MongoClient(os.environ["MONGO_URI"])

# Para pruebas locales (comente la linea de arriba y descomente esta):
# client = MongoClient("mongodb://<usuario>:<contrasena>@157.253.236.88:8087")

# Reemplace ISIS******* por el nombre de su base (el que ve en Compass)
db = client["ISIS*******"]


def serializar(doc):
    """Convierte ObjectId a string para que sea JSON-serializable."""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    cursor = db["comentarios_bares"].find({"bar_id": bar_id})
    comentarios = [serializar(doc) for doc in cursor]
    return comentarios


@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}


@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    cursor = db["eventos"].find({"bar_id": bar_id})
    eventos = [serializar(doc) for doc in cursor]
    return eventos


@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento guardado'}
