from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
import models, schemas, auth as auth_utils

router = APIRouter(prefix="/servicios", tags=["servicios"])


@router.get("", response_model=List[schemas.ServicioOut])
def list_servicios(
    integrante_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    query = db.query(models.Servicio)
    if integrante_id:
        ids = db.query(models.ServicioIntegrante.servicio_id).filter(
            models.ServicioIntegrante.integrante_id == integrante_id
        ).subquery()
        query = query.filter(models.Servicio.id.in_(ids))
    return query.order_by(models.Servicio.fecha.desc()).all()


@router.get("/{servicio_id}", response_model=schemas.ServicioOut)
def get_servicio(
    servicio_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    s = db.query(models.Servicio).filter(models.Servicio.id == servicio_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="No encontrado")
    return s


@router.post("", response_model=schemas.ServicioOut, status_code=201)
def create_servicio(
    data: schemas.ServicioCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    s = models.Servicio(**data.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.put("/{servicio_id}", response_model=schemas.ServicioOut)
def update_servicio(
    servicio_id: int,
    data: schemas.ServicioUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    s = db.query(models.Servicio).filter(models.Servicio.id == servicio_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(s, k, v)
    db.commit()
    db.refresh(s)
    return s


@router.delete("/{servicio_id}", status_code=204)
def delete_servicio(
    servicio_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    s = db.query(models.Servicio).filter(models.Servicio.id == servicio_id).first()
    if s:
        db.delete(s)
        db.commit()


@router.post("/{servicio_id}/integrantes", status_code=201)
def add_servicio_integrante(
    servicio_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    si = models.ServicioIntegrante(
        servicio_id=servicio_id,
        integrante_id=data["integrante_id"],
    )
    db.add(si)
    db.commit()
    return {"ok": True}


@router.delete("/{servicio_id}/integrantes/{integrante_id}", status_code=204)
def remove_servicio_integrante(
    servicio_id: int,
    integrante_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    si = db.query(models.ServicioIntegrante).filter(
        models.ServicioIntegrante.servicio_id == servicio_id,
        models.ServicioIntegrante.integrante_id == integrante_id,
    ).first()
    if si:
        db.delete(si)
        db.commit()
