from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from datetime import date, datetime
from database import get_db
import models, schemas, auth as auth_utils

router = APIRouter(prefix="/integrantes", tags=["integrantes"])


def build_integrante_out(integrante: models.Integrante) -> dict:
    edad = None
    if integrante.fecha_nacimiento:
        today = date.today()
        fn = integrante.fecha_nacimiento
        edad = today.year - fn.year - ((today.month, today.day) < (fn.month, fn.day))

    grupos = []
    for gi in integrante.grupo_integrantes:
        grupos.append({
            "grupo_id": gi.grupo_id,
            "grupo_nombre": gi.grupo.nombre if gi.grupo else "",
            "rol_en_grupo": gi.rol_en_grupo,
        })

    ministerios = []
    for mi in integrante.ministerio_integrantes:
        ministerios.append({
            "id": mi.ministerio_id,
            "nombre": mi.ministerio.nombre if mi.ministerio else "",
            "es_responsable": mi.es_responsable,
        })

    return {
        **{c.name: getattr(integrante, c.name) for c in integrante.__table__.columns},
        "edad": edad,
        "grupos": grupos,
        "ministerios": ministerios,
    }


def maybe_create_user(integrante: models.Integrante, grupos_data: list, db: Session):
    """Create a user account if integrante has a leadership role and doesn't have one."""
    needs_account = any(
        g.get("rol_en_grupo") in ["responsable", "supervisor", "ayudante"]
        for g in (grupos_data or [])
    )
    if needs_account and integrante.email:
        existing = db.query(models.User).filter(models.User.integrante_id == integrante.id).first()
        if not existing:
            user = models.User(
                email=integrante.email,
                password_hash=auth_utils.get_password_hash("temporal1234"),
                nombre=f"{integrante.nombre} {integrante.apellidos}",
                rol="responsable",
                integrante_id=integrante.id,
            )
            db.add(user)


@router.get("", response_model=List[schemas.IntegranteOut])
def list_integrantes(
    q: Optional[str] = None,
    grupo_id: Optional[int] = None,
    sin_grupo: Optional[bool] = None,
    is_membro: Optional[bool] = None,
    rol: Optional[str] = None,
    ministerio_id: Optional[int] = None,
    es_responsable_ministerio: Optional[bool] = None,
    novo_crente: Optional[bool] = None,
    novo_batizado: Optional[bool] = None,
    bautizado: Optional[bool] = None,
    iglesia_procedente: Optional[bool] = None,
    discipulado_inicial: Optional[str] = None,
    pre_batismo: Optional[str] = None,
    escuela_biblica: Optional[str] = None,
    escuela_discipulado: Optional[str] = None,
    treinamento: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    query = db.query(models.Integrante).filter(models.Integrante.activo == True)

    # Role-based access
    accessible_ids = auth_utils.get_accessible_group_ids(current_user, db)
    if accessible_ids is not None:
        if accessible_ids:
            integrante_ids_in_groups = db.query(models.GrupoIntegrante.integrante_id).filter(
                models.GrupoIntegrante.grupo_id.in_(accessible_ids)
            ).subquery()
            query = query.filter(models.Integrante.id.in_(integrante_ids_in_groups))
        else:
            return []

    if q:
        query = query.filter(or_(
            models.Integrante.nombre.ilike(f"%{q}%"),
            models.Integrante.apellidos.ilike(f"%{q}%"),
            models.Integrante.email.ilike(f"%{q}%"),
        ))

    if is_membro is not None:
        query = query.filter(models.Integrante.is_membro == is_membro)
    if novo_crente is not None:
        query = query.filter(models.Integrante.novo_crente == novo_crente)
    if novo_batizado is not None:
        query = query.filter(models.Integrante.novo_batizado == novo_batizado)
    if bautizado is not None:
        query = query.filter(models.Integrante.bautizado == bautizado)
    if iglesia_procedente is not None:
        query = query.filter(models.Integrante.iglesia_procedente == iglesia_procedente)
    if discipulado_inicial:
        query = query.filter(models.Integrante.discipulado_inicial == discipulado_inicial)
    if pre_batismo:
        query = query.filter(models.Integrante.pre_batismo == pre_batismo)
    if escuela_biblica:
        query = query.filter(models.Integrante.escuela_biblica == escuela_biblica)
    if escuela_discipulado:
        query = query.filter(models.Integrante.escuela_discipulado == escuela_discipulado)
    if treinamento:
        query = query.filter(models.Integrante.treinamento == treinamento)

    if sin_grupo:
        integrantes_con_grupo = db.query(models.GrupoIntegrante.integrante_id).subquery()
        query = query.filter(~models.Integrante.id.in_(integrantes_con_grupo))
    elif grupo_id is not None:
        grupo_member_ids = db.query(models.GrupoIntegrante.integrante_id).filter(
            models.GrupoIntegrante.grupo_id == grupo_id
        ).subquery()
        query = query.filter(models.Integrante.id.in_(grupo_member_ids))

    if rol:
        gi_sub = db.query(models.GrupoIntegrante.integrante_id).filter(
            models.GrupoIntegrante.rol_en_grupo == rol
        ).subquery()
        query = query.filter(models.Integrante.id.in_(gi_sub))

    if ministerio_id is not None:
        mi_sub = db.query(models.MinisterioIntegrante.integrante_id).filter(
            models.MinisterioIntegrante.ministerio_id == ministerio_id
        )
        if es_responsable_ministerio is not None:
            mi_sub = mi_sub.filter(models.MinisterioIntegrante.es_responsable == es_responsable_ministerio)
        mi_sub = mi_sub.subquery()
        query = query.filter(models.Integrante.id.in_(mi_sub))

    integrantes = query.order_by(models.Integrante.nombre).all()
    return [build_integrante_out(i) for i in integrantes]


@router.get("/mapa", response_model=List[schemas.IntegranteMapaOut])
def integrantes_mapa(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    query = db.query(models.Integrante).filter(
        models.Integrante.activo == True,
        models.Integrante.latitude.isnot(None),
        models.Integrante.longitude.isnot(None),
    )
    accessible_ids = auth_utils.get_accessible_group_ids(current_user, db)
    if accessible_ids is not None and accessible_ids:
        ids = db.query(models.GrupoIntegrante.integrante_id).filter(
            models.GrupoIntegrante.grupo_id.in_(accessible_ids)
        ).subquery()
        query = query.filter(models.Integrante.id.in_(ids))

    result = []
    for i in query.all():
        grupo_nombre = None
        if i.grupo_integrantes:
            grupo_nombre = i.grupo_integrantes[0].grupo.nombre if i.grupo_integrantes[0].grupo else None
        result.append({
            "id": i.id, "nombre": i.nombre, "apellidos": i.apellidos,
            "latitude": i.latitude, "longitude": i.longitude, "grupo_nombre": grupo_nombre,
        })
    return result


@router.get("/{integrante_id}", response_model=schemas.IntegranteOut)
def get_integrante(
    integrante_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    i = db.query(models.Integrante).filter(models.Integrante.id == integrante_id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Integrante no encontrado")
    return build_integrante_out(i)


@router.post("", response_model=schemas.IntegranteOut, status_code=201)
def create_integrante(
    data: schemas.IntegranteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    grupos_data = data.grupos or []
    ministerios_data = data.ministerios or []

    integrante_dict = data.model_dump(exclude={"grupos", "ministerios"})
    integrante = models.Integrante(**integrante_dict)
    db.add(integrante)
    db.flush()

    for g in grupos_data:
        gi = models.GrupoIntegrante(
            grupo_id=g["grupo_id"],
            integrante_id=integrante.id,
            rol_en_grupo=g.get("rol_en_grupo"),
        )
        db.add(gi)
        # Update grupo's role fields
        if g.get("rol_en_grupo") == "responsable":
            grupo = db.query(models.Grupo).filter(models.Grupo.id == g["grupo_id"]).first()
            if grupo and not grupo.responsable_id:
                grupo.responsable_id = integrante.id
        elif g.get("rol_en_grupo") == "supervisor":
            grupo = db.query(models.Grupo).filter(models.Grupo.id == g["grupo_id"]).first()
            if grupo and not grupo.supervisor_id:
                grupo.supervisor_id = integrante.id
        elif g.get("rol_en_grupo") == "ayudante":
            grupo = db.query(models.Grupo).filter(models.Grupo.id == g["grupo_id"]).first()
            if grupo and not grupo.ayudante_id:
                grupo.ayudante_id = integrante.id

    for m in ministerios_data:
        mi = models.MinisterioIntegrante(
            ministerio_id=m["ministerio_id"],
            integrante_id=integrante.id,
            es_responsable=m.get("es_responsable", False),
        )
        db.add(mi)

    maybe_create_user(integrante, grupos_data, db)
    db.commit()
    db.refresh(integrante)
    return build_integrante_out(integrante)


@router.put("/{integrante_id}", response_model=schemas.IntegranteOut)
def update_integrante(
    integrante_id: int,
    data: schemas.IntegranteUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    i = db.query(models.Integrante).filter(models.Integrante.id == integrante_id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Integrante no encontrado")

    update_data = data.model_dump(exclude_unset=True, exclude={"grupos", "ministerios"})
    for k, v in update_data.items():
        setattr(i, k, v)

    if data.grupos is not None:
        db.query(models.GrupoIntegrante).filter(
            models.GrupoIntegrante.integrante_id == integrante_id
        ).delete()
        for g in data.grupos:
            gi = models.GrupoIntegrante(
                grupo_id=g["grupo_id"],
                integrante_id=integrante_id,
                rol_en_grupo=g.get("rol_en_grupo"),
            )
            db.add(gi)

    if data.ministerios is not None:
        db.query(models.MinisterioIntegrante).filter(
            models.MinisterioIntegrante.integrante_id == integrante_id
        ).delete()
        for m in data.ministerios:
            mi = models.MinisterioIntegrante(
                ministerio_id=m["ministerio_id"],
                integrante_id=integrante_id,
                es_responsable=m.get("es_responsable", False),
            )
            db.add(mi)

    db.commit()
    db.refresh(i)
    return build_integrante_out(i)


@router.delete("/{integrante_id}", status_code=204)
def delete_integrante(
    integrante_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    i = db.query(models.Integrante).filter(models.Integrante.id == integrante_id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Integrante no encontrado")

    # Check: cannot delete if sole responsable of a group
    grupos_as_responsable = db.query(models.Grupo).filter(
        models.Grupo.responsable_id == integrante_id
    ).all()
    for grupo in grupos_as_responsable:
        other_responsable = db.query(models.GrupoIntegrante).filter(
            models.GrupoIntegrante.grupo_id == grupo.id,
            models.GrupoIntegrante.rol_en_grupo == "responsable",
            models.GrupoIntegrante.integrante_id != integrante_id,
        ).first()
        if not other_responsable:
            raise HTTPException(
                status_code=400,
                detail=f"No se puede eliminar: es el único responsable del grupo '{grupo.nombre}'. Asigna otro responsable primero.",
            )

    i.activo = False
    db.commit()


@router.get("/{integrante_id}/asistencia")
def get_integrante_asistencia(
    integrante_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    today = date.today()
    mes_inicio = today.replace(day=1)
    ano_inicio = today.replace(month=1, day=1)

    grupos_ids = [
        gi.grupo_id
        for gi in db.query(models.GrupoIntegrante).filter(
            models.GrupoIntegrante.integrante_id == integrante_id
        ).all()
    ]
    if not grupos_ids:
        return {"ultimo_mes": 0.0, "ultimo_ano": 0.0, "total": 0.0}

    def calc_pct(fecha_inicio=None):
        r_query = db.query(models.Reunion).filter(models.Reunion.grupo_id.in_(grupos_ids))
        if fecha_inicio:
            r_query = r_query.filter(models.Reunion.fecha >= fecha_inicio)
        total_reuniones = r_query.count()
        if total_reuniones == 0:
            return 0.0
        reuniones_ids = [r.id for r in r_query.all()]
        presentes = db.query(models.IntegranteReunion).filter(
            models.IntegranteReunion.integrante_id == integrante_id,
            models.IntegranteReunion.reunion_id.in_(reuniones_ids),
            models.IntegranteReunion.presente == True,
        ).count()
        return round((presentes / total_reuniones) * 100, 1)

    return {
        "ultimo_mes": calc_pct(mes_inicio),
        "ultimo_ano": calc_pct(ano_inicio),
        "total": calc_pct(),
    }
