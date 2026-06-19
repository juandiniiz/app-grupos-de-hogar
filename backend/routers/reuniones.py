from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
import models, schemas, auth as auth_utils

router = APIRouter(prefix="/reuniones", tags=["reuniones"])


@router.get("", response_model=List[schemas.ReunionOut])
def list_reuniones(
    grupo_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    query = db.query(models.Reunion)
    accessible_ids = auth_utils.get_accessible_group_ids(current_user, db)
    if accessible_ids is not None:
        if accessible_ids:
            query = query.filter(models.Reunion.grupo_id.in_(accessible_ids))
        else:
            return []
    if grupo_id:
        query = query.filter(models.Reunion.grupo_id == grupo_id)
    return query.order_by(models.Reunion.fecha.desc()).all()


@router.get("/{reunion_id}", response_model=schemas.ReunionDetalleOut)
def get_reunion(
    reunion_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    r = db.query(models.Reunion).filter(models.Reunion.id == reunion_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    asistencia = []
    for ir in r.asistencia:
        i = ir.integrante
        asistencia.append({
            "id": ir.id,
            "integrante_id": i.id,
            "integrante_nombre": f"{i.nombre} {i.apellidos}",
            "presente": ir.presente,
        })

    return {
        **{c.name: getattr(r, c.name) for c in r.__table__.columns},
        "asistencia": asistencia,
        "oraciones": r.oraciones,
    }


@router.post("", response_model=schemas.ReunionOut, status_code=201)
def create_reunion(
    data: schemas.ReunionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    reunion = models.Reunion(**data.model_dump())
    db.add(reunion)
    db.flush()

    # Auto-create asistencia records for all group members
    grupo = db.query(models.Grupo).filter(models.Grupo.id == data.grupo_id).first()
    if grupo:
        for gi in grupo.integrantes:
            ir = models.IntegranteReunion(
                integrante_id=gi.integrante_id,
                reunion_id=reunion.id,
                presente=False,
            )
            db.add(ir)

    db.commit()
    db.refresh(reunion)
    return reunion


@router.put("/{reunion_id}", response_model=schemas.ReunionOut)
def update_reunion(
    reunion_id: int,
    data: schemas.ReunionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    r = db.query(models.Reunion).filter(models.Reunion.id == reunion_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r


@router.delete("/{reunion_id}", status_code=204)
def delete_reunion(
    reunion_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    r = db.query(models.Reunion).filter(models.Reunion.id == reunion_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    db.delete(r)
    db.commit()


@router.post("/{reunion_id}/asistencia")
def update_asistencia(
    reunion_id: int,
    data: List[dict],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    for item in data:
        ir = db.query(models.IntegranteReunion).filter(
            models.IntegranteReunion.reunion_id == reunion_id,
            models.IntegranteReunion.integrante_id == item["integrante_id"],
        ).first()
        if ir:
            ir.presente = item.get("presente", False)
        else:
            ir = models.IntegranteReunion(
                reunion_id=reunion_id,
                integrante_id=item["integrante_id"],
                presente=item.get("presente", False),
            )
            db.add(ir)

    # Update asistentes_count
    reunion = db.query(models.Reunion).filter(models.Reunion.id == reunion_id).first()
    if reunion:
        reunion.asistentes_count = db.query(models.IntegranteReunion).filter(
            models.IntegranteReunion.reunion_id == reunion_id,
            models.IntegranteReunion.presente == True,
        ).count()
    db.commit()
    return {"ok": True}


@router.get("/{reunion_id}/oraciones", response_model=List[schemas.OracaoReunionOut])
def get_oraciones(
    reunion_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    return db.query(models.OracaoReunion).filter(
        models.OracaoReunion.reunion_id == reunion_id
    ).all()


@router.post("/{reunion_id}/oraciones", response_model=schemas.OracaoReunionOut, status_code=201)
def add_oracao(
    reunion_id: int,
    data: schemas.OracaoReunionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    o = models.OracaoReunion(reunion_id=reunion_id, **data.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    return o


@router.put("/{reunion_id}/oraciones/{oracao_id}", response_model=schemas.OracaoReunionOut)
def update_oracao(
    reunion_id: int,
    oracao_id: int,
    data: schemas.OracaoReunionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    o = db.query(models.OracaoReunion).filter(
        models.OracaoReunion.id == oracao_id,
        models.OracaoReunion.reunion_id == reunion_id,
    ).first()
    if not o:
        raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(o, k, v)
    db.commit()
    db.refresh(o)
    return o


@router.delete("/{reunion_id}/oraciones/{oracao_id}", status_code=204)
def delete_oracao(
    reunion_id: int,
    oracao_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    o = db.query(models.OracaoReunion).filter(
        models.OracaoReunion.id == oracao_id
    ).first()
    if o:
        db.delete(o)
        db.commit()
