import json
import os

DB_FILE = "taller.json"

def leer_ordenes() -> list:
    #Lee el archivo taller.json y devuelve la lista de órdenes.
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def guardar_ordenes(ordenes: list):
    #Guarda la lista de órdenes en el archivo taller.json.
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(ordenes, f, indent=4, ensure_ascii=False)