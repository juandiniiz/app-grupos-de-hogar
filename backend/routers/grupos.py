from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
import models, schemas, auth as auth_utils

router = APIRouter(prefix="/grupos", tags=["grupos"])


def build_grupo_out(g: models.Grupo, db: Session) -> dict:
    return {
        **{c.name: getattr(g, c.name) for c in g.__table__.columns},
        "responsable_nombre": f"{g.responsable.nombre} {g.responsable.apellidos}" if g.responsable else None,
        "ayudante_nombre": f"{g.ayudante.nombre} {g.ayudante.apellidos}" if g.ayudante else None,
        "supervisor_nombre": f"{g.supervisor.nombre} {g.supervisor.apellidos}" if g.supervisor else None,
        "grupo_pai_nombre": g.grupo_pai.nombre if g.grupo_pai else None,
        "integrantes_count": len(g.integrantes),
    }


@router.get("", response_model=List[schemas.GrupoOut])
def list_grupos(
    frecuencia: Optional[str] = None,
    dia_semana: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    query = db.query(models.Grupo).filter(models.Grupo.activo == True)
    accessible_ids = auth_utils.get_accessible_group_ids(current_user, db)
    if accessible_ids is not None:
        if accessible_ids:
            query = query.filter(models.Grupo.id.in_(accessible_ids))
        else:
            return []
    if frecuencia:
        query = query.filter(models.Grupo.frecuencia == frecuencia)
    if dia_semana:
        query = query.filter(models.Grupo.dia_semana == dia_semana)
    return [build_grupo_out(g, db) for g in query.order_by(models.Grupo.nombre).all()]


@router.get("/mapa", response_model=List[schemas.GrupoMapaOut])
def grupos_mapa(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    query = db.query(models.Grupo).filter(
        models.Grupo.activo == True,
        models.Grupo.latitude.isnot(None),
    )
    accessible_ids = auth_utils.get_accessible_group_ids(current_user, db)
    if accessible_ids is not None and accessible_ids:
        query = query.filter(models.Grupo.id.in_(accessible_ids))
    return query.all()


@router.get("/{grupo_id}", response_model=schemas.GrupoOut)
def get_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    g = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return build_grupo_out(g, db)


@router.post("", response_model=schemas.GrupoOut, status_code=201)
def create_grupo(
    data: schemas.GrupoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    integrantes_data = data.integrantes or []
    grupo_dict = data.model_dump(exclude={"integrantes"})
    grupo = models.Grupo(**grupo_dict)
    db.add(grupo)
    db.flush()
    for item in integrantes_data:
        gi = models.GrupoIntegrante(
            grupo_id=grupo.id,
            integrante_id=item["integrante_id"],
            rol_en_grupo=item.get("rol_en_grupo"),
        )
        db.add(gi)
    db.commit()
    db.refresh(grupo)
    return build_grupo_out(grupo, db)


@router.put("/{grupo_id}", response_model=schemas.GrupoOut)
def update_grupo(
    grupo_id: int,
    data: schemas.GrupoUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    g = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    update_data = data.model_dump(exclude_unset=True, exclude={"integrantes"})
    for k, v in update_data.items():
        setattr(g, k, v)
    if data.integrantes is not None:
        db.query(models.GrupoIntegrante).filter(
            models.GrupoIntegrante.grupo_id == grupo_id
        ).delete()
        for item in data.integrantes:
            gi = models.GrupoIntegrante(
                grupo_id=grupo_id,
                integrante_id=item["integrante_id"],
                rol_en_grupo=item.get("rol_en_grupo"),
            )
            db.add(gi)
    db.commit()
    db.refresh(g)
    return build_grupo_out(g, db)


@router.delete("/{grupo_id}", status_code=204)
def delete_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    g = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    g.activo = False
    db.commit()


@router.get("/{grupo_id}/integrantes")
def get_grupo_integrantes(
    grupo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    from datetime import date
    g = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    result = []
    for gi in g.integrantes:
        i = gi.integrante
        total_reuniones = db.query(models.Reunion).filter(
            models.Reunion.grupo_id == grupo_id
        ).count()
        presentes = 0
        if total_reuniones > 0:
            reunion_ids = [
                r.id
                for r in db.query(models.Reunion).filter(
                    models.Reunion.grupo_id == grupo_id
                ).all()
            ]
            presentes = db.query(models.IntegranteReunion).filter(
                models.IntegranteReunion.integrante_id == i.id,
                models.IntegranteReunion.presente == True,
                models.IntegranteReunion.reunion_id.in_(reunion_ids),
            ).count()
        asistencia_pct = round((presentes / total_reuniones) * 100, 1) if total_reuniones > 0 else 0.0
        result.append({
            "id": i.id,
            "nombre": i.nombre,
            "apellidos": i.apellidos,
            "telefono": i.telefono,
            "email": i.email,
            "rol_en_grupo": gi.rol_en_grupo,
            "asistencia_pct": asistencia_pct,
            "novo_crente": i.novo_crente,
            "bautizado": i.bautizado,
            "novo_batizado": i.novo_batizado,
        })
    return result


@router.post("/{grupo_id}/integrantes", status_code=201)
def add_grupo_integrante(
    grupo_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    existing = db.query(models.GrupoIntegrante).filter(
        models.GrupoIntegrante.grupo_id == grupo_id,
        models.GrupoIntegrante.integrante_id == data["integrante_id"],
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Integrante ya está en el grupo")
    gi = models.GrupoIntegrante(
        grupo_id=grupo_id,
        integrante_id=data["integrante_id"],
        rol_en_grupo=data.get("rol_en_grupo"),
    )
    db.add(gi)
    db.commit()
    return {"ok": True}


@router.delete("/{grupo_id}/integrantes/{integrante_id}", status_code=204)
def remove_grupo_integrante(
    grupo_id: int,
    integrante_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    gi = db.query(models.GrupoIntegrante).filter(
        models.GrupoIntegrante.grupo_id == grupo_id,
        models.GrupoIntegrante.integrante_id == integrante_id,
    ).first()
    if not gi:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(gi)
    db.commit()
