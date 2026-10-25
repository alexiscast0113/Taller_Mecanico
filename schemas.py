from pydantic import BaseModel, Field
from pydantic import BaseModel, Field

class OrdenCreate(BaseModel):
    placa: str = Field(..., max_length=6, description="Placa de la motocicleta (máximo 6 caracteres)")
    modelo: str = Field(..., description="Modelo de la motocicleta")
    falla_reportada: str = Field(..., description="Descripción de la falla reportada")


class OrdenUpdate(BaseModel):
    nuevo_estado: str = Field(..., description="Nuevo estado de la orden")
    costo_reparacion: float = Field(..., description="Costo correspondiente a la reparación")