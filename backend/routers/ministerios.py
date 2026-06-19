from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
import models, schemas, auth as auth_utils

router = APIRouter(prefix="/ministerios", tags=["ministerios"])


def build_ministerio_out(m: models.Ministerio) -> dict:
    responsables = [
        {
            "id": mi.integrante.id,
            "nombre": mi.integrante.nombre,
            "apellidos": mi.integrante.apellidos,
            "es_responsable": mi.es_responsable,
        }
        for mi in m.integrantes
        if mi.es_responsable and mi.integrante
    ]
    tarefas = []
    for t in m.tarefas:
        tarefas.append({
            "id": t.id,
            "nombre": t.nombre,
            "ministerio_id": t.ministerio_id,
            "integrantes": [
                {
                    "id": ti.integrante.id,
                    "nombre": ti.integrante.nombre,
                    "apellidos": ti.integrante.apellidos,
                }
                for ti in t.integrantes
                if ti.integrante
            ],
        })
    return {
        "id": m.id,
        "nombre": m.nombre,
        "descripcion": m.descripcion,
        "created_at": m.created_at,
        "integrantes_count": len(m.integrantes),
        "responsables": responsables,
        "tarefas": tarefas,
    }


@router.get("", response_model=List[schemas.MinisterioOut])
def list_ministerios(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    return [
        build_ministerio_out(m)
        for m in db.query(models.Ministerio).order_by(models.Ministerio.nombre).all()
    ]


@router.get("/{ministerio_id}", response_model=schemas.MinisterioOut)
def get_ministerio(
    ministerio_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    m = db.query(models.Ministerio).filter(models.Ministerio.id == ministerio_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="No encontrado")
    return build_ministerio_out(m)


@router.post("", response_model=schemas.MinisterioOut, status_code=201)
def create_ministerio(
    data: schemas.MinisterioCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    m = models.Ministerio(**data.model_dump())
    db.add(m)
    db.commit()
    db.refresh(m)
    return build_ministerio_out(m)


@router.put("/{ministerio_id}", response_model=schemas.MinisterioOut)
def update_ministerio(
    ministerio_id: int,
    data: schemas.MinisterioUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    m = db.query(models.Ministerio).filter(models.Ministerio.id == ministerio_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(m, k, v)
    db.commit()
    db.refresh(m)
    return build_ministerio_out(m)


@router.delete("/{ministerio_id}", status_code=204)
def delete_ministerio(
    ministerio_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    m = db.query(models.Ministerio).filter(models.Ministerio.id == ministerio_id).first()
    if m:
        db.delete(m)
        db.commit()


@router.post("/{ministerio_id}/integrantes", status_code=201)
def add_ministerio_integrante(
    ministerio_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    existing = db.query(models.MinisterioIntegrante).filter(
        models.MinisterioIntegrante.ministerio_id == ministerio_id,
        models.MinisterioIntegrante.integrante_id == data["integrante_id"],
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya está en el ministerio")
    mi = models.MinisterioIntegrante(
        ministerio_id=ministerio_id,
        integrante_id=data["integrante_id"],
        es_responsable=data.get("es_responsable", False),
    )
    db.add(mi)
    db.commit()
    return {"ok": True}


@router.delete("/{ministerio_id}/integrantes/{integrante_id}", status_code=204)
def remove_ministerio_integrante(
    ministerio_id: int,
    integrante_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    mi = db.query(models.MinisterioIntegrante).filter(
        models.MinisterioIntegrante.ministerio_id == ministerio_id,
        models.MinisterioIntegrante.integrante_id == integrante_id,
    ).first()
    if mi:
        db.delete(mi)
        db.commit()


@router.post("/{ministerio_id}/tarefas", status_code=201)
def add_tarefa(
    ministerio_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    t = models.MinisterioTarefa(ministerio_id=ministerio_id, nombre=data["nombre"])
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"id": t.id, "nombre": t.nombre, "ministerio_id": t.ministerio_id, "integrantes": []}


@router.put("/tarefas/{tarefa_id}")
def update_tarefa(
    tarefa_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    t = db.query(models.MinisterioTarefa).filter(models.MinisterioTarefa.id == tarefa_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="No encontrado")
    t.nombre = data.get("nombre", t.nombre)
    db.commit()
    return {"ok": True}


@router.delete("/tarefas/{tarefa_id}", status_code=204)
def delete_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    t = db.query(models.MinisterioTarefa).filter(models.MinisterioTarefa.id == tarefa_id).first()
    if t:
        db.delete(t)
        db.commit()


@router.post("/tarefas/{tarefa_id}/integrantes", status_code=201)
def add_tarefa_integrante(
    tarefa_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    ti = models.MinisterioTarefaIntegrante(
        tarefa_id=tarefa_id,
        integrante_id=data["integrante_id"],
    )
    db.add(ti)
    db.commit()
    return {"ok": True}


@router.delete("/tarefas/{tarefa_id}/integrantes/{integrante_id}", status_code=204)
def remove_tarefa_integrante(
    tarefa_id: int,
    integrante_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    ti = db.query(models.MinisterioTarefaIntegrante).filter(
        models.MinisterioTarefaIntegrante.tarefa_id == tarefa_id,
        models.MinisterioTarefaIntegrante.integrante_id == integrante_id,
    ).first()
    if ti:
        db.delete(ti)
        db.commit()
