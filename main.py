from fastapi import FastAPI, HTTPException, status
from schemas import OrdenCreate
from database import leer_ordenes, guardar_ordenes
from fastapi import status
from schemas import OrdenUpdate

app = FastAPI()

@app.post("/ordenes", status_code=status.HTTP_201_CREATED)
def crear_orden(orden: OrdenCreate):
    ordenes = leer_ordenes()
    
    # Validación de motocicleta existente
    for item in ordenes:
        if item.get("placa") == orden.placa:
            if item.get("estado") != "Entregada":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La moto ya se encuentra en el taller"
                )
    
    # Crear el diccionario con los datos de entrada y añadir la lógica de negocio requerida
    nueva_orden = orden.dict()
    nueva_orden["estado"] = "En diagnóstico"
    nueva_orden["costo_reparacion"] = 0
    
    # Agregar a la lista y persistir en taller.json
    ordenes.append(nueva_orden)
    guardar_ordenes(ordenes)
    
    return {
        "mensaje": "Orden de ingreso creada exitosamente",
        "orden": nueva_orden
    }

@app.get("/ordenes", status_code=status.HTTP_200_OK)
def consultar_ordenes():
    ordenes = leer_ordenes()
    return ordenes


@app.put("/ordenes/{placa}", status_code=status.HTTP_200_OK)
def actualizar_orden(placa: str, datos_actualizacion: OrdenUpdate):
    ordenes = leer_ordenes()
    orden_encontrada = None
    
    # Regla 1: Verificar si la placa existe en taller.json
    for item in ordenes:
        if item.get("placa") == placa:
            orden_encontrada = item
            break
            
    if not orden_encontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="404 Not Found"
        )
        
    # Regla 2: Validar costo de reparación si se marca como reparada
    if datos_actualizacion.nuevo_estado == "Reparada" and datos_actualizacion.costo_reparacion <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede marcar como reparada sin asignar un costo de reparación"
        )
        
    # Regla 3: Actualizar el estado y el costo en taller.json si todo es correcto
    orden_encontrada["estado"] = datos_actualizacion.nuevo_estado
    orden_encontrada["costo_reparacion"] = datos_actualizacion.costo_reparacion
    
    guardar_ordenes(ordenes)
    
    return {
        "mensaje": "Orden actualizada exitosamente",
        "orden": orden_encontrada
    }