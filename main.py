from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="API de Gestión de Tareas Académicas", version="1.0.0")

db_tareas = []

class Tarea(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    titulo: str
    descripcion: Optional[str] = None
    materia: str = Field(..., min_length=3)
    completada: bool = False

@app.post("/tareas/", response_model=Tarea)
async def crear_tarea(tarea: Tarea):
    db_tareas.append(tarea)
    return tarea

@app.get("/tareas/", response_model=List[Tarea])
async def listar_tareas():
    return db_tareas

@app.get("/tareas/{tarea_id}", response_model=Tarea)
async def obtener_tarea(tarea_id: UUID):
    for t in db_tareas:
        if t.id == tarea_id:
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.put("/tareas/{tarea_id}/completar", response_model=Tarea)
async def completar_tarea(tarea_id: UUID):
    for t in db_tareas:
        if t.id == tarea_id:
            t.completada = True
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/tareas/{tarea_id}")
async def eliminar_tarea(tarea_id: UUID):
    for index, t in enumerate(db_tareas):
        if t.id == tarea_id:
            db_tareas.pop(index)
            return {"mensaje": "Tarea eliminada exitosamente"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")