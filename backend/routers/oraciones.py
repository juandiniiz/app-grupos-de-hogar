from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
import models, schemas, auth as auth_utils

router = APIRouter(prefix="/oraciones", tags=["oraciones"])


@router.get("", response_model=List[schemas.OracionOut])
def list_oraciones(
    integrante_id: Optional[int] = None,
    grupo_id: Optional[int] = None,
    respondida: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    query = db.query(models.Oracion)
    if integrante_id:
        query = query.filter(models.Oracion.integrante_id == integrante_id)
    if grupo_id:
        query = query.filter(models.Oracion.grupo_id == grupo_id)
    if respondida is not None:
        query = query.filter(models.Oracion.respondida == respondida)
    return query.order_by(models.Oracion.fecha.desc()).all()


@router.post("", response_model=schemas.OracionOut, status_code=201)
def create_oracion(
    data: schemas.OracionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    o = models.Oracion(**data.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    return o


@router.put("/{oracion_id}", response_model=schemas.OracionOut)
def update_oracion(
    oracion_id: int,
    data: schemas.OracionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    o = db.query(models.Oracion).filter(models.Oracion.id == oracion_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(o, k, v)
    db.commit()
    db.refresh(o)
    return o


@router.delete("/{oracion_id}", status_code=204)
def delete_oracion(
    oracion_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    o = db.query(models.Oracion).filter(models.Oracion.id == oracion_id).first()
    if o:
        db.delete(o)
        db.commit()
