from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
import models, schemas, auth as auth_utils

router = APIRouter(prefix="/testimonios", tags=["testimonios"])


def build_testimonio_out(t: models.Testimonio) -> dict:
    return {
        **{c.name: getattr(t, c.name) for c in t.__table__.columns},
        "integrante_nombre": f"{t.integrante.nombre} {t.integrante.apellidos}" if t.integrante else None,
        "grupo_nombre": t.grupo.nombre if t.grupo else None,
    }


@router.get("", response_model=List[schemas.TestimonioOut])
def list_testimonios(
    destacado: Optional[bool] = None,
    grupo_id: Optional[int] = None,
    integrante_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    query = db.query(models.Testimonio)
    if destacado is not None:
        query = query.filter(models.Testimonio.destacado == destacado)
    if grupo_id:
        query = query.filter(models.Testimonio.grupo_id == grupo_id)
    if integrante_id:
        query = query.filter(models.Testimonio.integrante_id == integrante_id)
    return [build_testimonio_out(t) for t in query.order_by(models.Testimonio.fecha.desc()).all()]


@router.get("/{testimonio_id}", response_model=schemas.TestimonioOut)
def get_testimonio(
    testimonio_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    t = db.query(models.Testimonio).filter(models.Testimonio.id == testimonio_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="No encontrado")
    return build_testimonio_out(t)


@router.post("", response_model=schemas.TestimonioOut, status_code=201)
def create_testimonio(
    data: schemas.TestimonioCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    t = models.Testimonio(**data.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return build_testimonio_out(t)


@router.put("/{testimonio_id}", response_model=schemas.TestimonioOut)
def update_testimonio(
    testimonio_id: int,
    data: schemas.TestimonioUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    t = db.query(models.Testimonio).filter(models.Testimonio.id == testimonio_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)
    return build_testimonio_out(t)


@router.delete("/{testimonio_id}", status_code=204)
def delete_testimonio(
    testimonio_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    t = db.query(models.Testimonio).filter(models.Testimonio.id == testimonio_id).first()
    if t:
        db.delete(t)
        db.commit()
