from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime, timedelta
from database import engine, get_db, Base
import models, schemas, auth as auth_utils
from routers import auth, integrantes, grupos, ministerios, servicios, reuniones, oraciones, testimonios

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grupos de Hogar API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(integrantes.router, prefix="/api")
app.include_router(grupos.router, prefix="/api")
app.include_router(ministerios.router, prefix="/api")
app.include_router(servicios.router, prefix="/api")
app.include_router(reuniones.router, prefix="/api")
app.include_router(oraciones.router, prefix="/api")
app.include_router(testimonios.router, prefix="/api")


@app.get("/api/stats/dashboard", response_model=schemas.DashboardStats)
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    accessible_ids = auth_utils.get_accessible_group_ids(current_user, db)

    # Determine filters
    if accessible_ids is not None and not accessible_ids:
        # No access at all
        return schemas.DashboardStats()

    has_group_filter = accessible_ids is not None and len(accessible_ids) > 0

    # Groups
    g_query = db.query(models.Grupo).filter(models.Grupo.activo == True)
    if has_group_filter:
        g_query = g_query.filter(models.Grupo.id.in_(accessible_ids))
    total_grupos = g_query.count()

    # Integrantes
    if has_group_filter:
        integrante_ids_q = db.query(models.GrupoIntegrante.integrante_id).filter(
            models.GrupoIntegrante.grupo_id.in_(accessible_ids)
        ).subquery()
        i_base = db.query(models.Integrante).filter(
            models.Integrante.activo == True,
            models.Integrante.id.in_(integrante_ids_q),
        )
    else:
        i_base = db.query(models.Integrante).filter(models.Integrante.activo == True)

    total_integrantes = i_base.count()
    total_membros = i_base.filter(models.Integrante.is_membro == True).count()

    integrantes_con_grupo = db.query(models.GrupoIntegrante.integrante_id).distinct().subquery()
    integrantes_sin_grupo = db.query(models.Integrante).filter(
        models.Integrante.activo == True,
        ~models.Integrante.id.in_(integrantes_con_grupo),
    ).count()
    integrantes_sin_grupo_pct = round((integrantes_sin_grupo / total_integrantes * 100), 1) if total_integrantes > 0 else 0.0

    membros_con_grupo = db.query(models.GrupoIntegrante.integrante_id).join(
        models.Integrante, models.Integrante.id == models.GrupoIntegrante.integrante_id
    ).filter(models.Integrante.is_membro == True).distinct().subquery()
    membros_total = db.query(models.Integrante).filter(
        models.Integrante.activo == True,
        models.Integrante.is_membro == True,
    ).count()
    membros_sin_grupo = db.query(models.Integrante).filter(
        models.Integrante.activo == True,
        models.Integrante.is_membro == True,
        ~models.Integrante.id.in_(membros_con_grupo),
    ).count()
    membros_sin_grupo_pct = round((membros_sin_grupo / membros_total * 100), 1) if membros_total > 0 else 0.0

    total_en_ministerio = db.query(models.MinisterioIntegrante.integrante_id).distinct().count()

    supervisores_count = db.query(models.GrupoIntegrante.integrante_id).filter(
        models.GrupoIntegrante.rol_en_grupo == "supervisor"
    ).distinct().count()
    responsables_count = db.query(models.GrupoIntegrante.integrante_id).filter(
        models.GrupoIntegrante.rol_en_grupo == "responsable"
    ).distinct().count()
    ayudantes_count = db.query(models.GrupoIntegrante.integrante_id).filter(
        models.GrupoIntegrante.rol_en_grupo == "ayudante"
    ).distinct().count()

    # Fe stats
    total_visitantes = db.query(func.sum(models.Reunion.visitantes_count)).scalar() or 0
    total_novos_crentes_reuniones = db.query(func.sum(models.Reunion.novos_crentes_count)).scalar() or 0
    total_batizados = db.query(models.Integrante).filter(
        models.Integrante.bautizado == True, models.Integrante.activo == True
    ).count()
    total_de_outra_igreja = db.query(models.Integrante).filter(
        models.Integrante.iglesia_procedente == True, models.Integrante.activo == True
    ).count()
    avg_visitantes = round(total_visitantes / total_grupos, 1) if total_grupos > 0 else 0.0
    avg_novos_crentes = round(total_novos_crentes_reuniones / total_grupos, 1) if total_grupos > 0 else 0.0

    # Reuniones
    r_base = db.query(models.Reunion)
    if has_group_filter:
        r_base = r_base.filter(models.Reunion.grupo_id.in_(accessible_ids))
    reuniones_periodicas = r_base.filter(models.Reunion.tipo == "periodica").count()
    reuniones_comunhao = r_base.filter(models.Reunion.tipo == "comunhao").count()
    reuniones_evangelisticas = r_base.filter(models.Reunion.tipo == "evangelistica").count()

    grupos_freq = db.query(models.Grupo).filter(models.Grupo.activo == True)
    if has_group_filter:
        grupos_freq = grupos_freq.filter(models.Grupo.id.in_(accessible_ids))
    reuniones_semanais = grupos_freq.filter(models.Grupo.frecuencia == "semanal").count()
    reuniones_quinzenais = grupos_freq.filter(models.Grupo.frecuencia == "quincenal").count()
    reuniones_mensais = grupos_freq.filter(models.Grupo.frecuencia == "mensual").count()

    # Asistencia
    today = date.today()
    mes_inicio = today.replace(day=1)
    ano_inicio = today.replace(month=1, day=1)

    def calc_asistencia_global(fecha_inicio=None):
        rq = db.query(models.Reunion)
        if has_group_filter:
            rq = rq.filter(models.Reunion.grupo_id.in_(accessible_ids))
        if fecha_inicio:
            rq = rq.filter(models.Reunion.fecha >= fecha_inicio)
        reuniones_ids = [r.id for r in rq.all()]
        if not reuniones_ids:
            return 0.0
        total_posibles = db.query(models.IntegranteReunion).filter(
            models.IntegranteReunion.reunion_id.in_(reuniones_ids)
        ).count()
        presentes = db.query(models.IntegranteReunion).filter(
            models.IntegranteReunion.reunion_id.in_(reuniones_ids),
            models.IntegranteReunion.presente == True,
        ).count()
        return round((presentes / total_posibles) * 100, 1) if total_posibles > 0 else 0.0

    # Formacion
    def count_formacion(campo, valor):
        return db.query(models.Integrante).filter(
            models.Integrante.activo == True,
            getattr(models.Integrante, campo) == valor,
        ).count()

    # Oraciones
    total_oraciones = db.query(models.Oracion).count()
    oraciones_respondidas = db.query(models.Oracion).filter(models.Oracion.respondida == True).count()

    # Testimonios destacados
    from routers.testimonios import build_testimonio_out
    testimonios_destacados_objs = (
        db.query(models.Testimonio)
        .filter(models.Testimonio.destacado == True)
        .order_by(models.Testimonio.fecha.desc())
        .limit(4)
        .all()
    )
    testimonios_destacados = [build_testimonio_out(t) for t in testimonios_destacados_objs]

    return schemas.DashboardStats(
        total_grupos=total_grupos,
        total_integrantes=total_integrantes,
        total_membros=total_membros,
        integrantes_sin_grupo=integrantes_sin_grupo,
        integrantes_sin_grupo_pct=integrantes_sin_grupo_pct,
        membros_sin_grupo=membros_sin_grupo,
        membros_sin_grupo_pct=membros_sin_grupo_pct,
        total_en_ministerio=total_en_ministerio,
        supervisores_count=supervisores_count,
        responsables_count=responsables_count,
        ayudantes_count=ayudantes_count,
        total_visitantes=total_visitantes,
        avg_visitantes_por_grupo=avg_visitantes,
        total_novos_crentes=total_novos_crentes_reuniones,
        avg_novos_crentes_por_grupo=avg_novos_crentes,
        total_batizados=total_batizados,
        total_de_outra_igreja=total_de_outra_igreja,
        reuniones_periodicas=reuniones_periodicas,
        reuniones_comunhao=reuniones_comunhao,
        reuniones_evangelisticas=reuniones_evangelisticas,
        reuniones_semanais=reuniones_semanais,
        reuniones_quinzenais=reuniones_quinzenais,
        reuniones_mensais=reuniones_mensais,
        asistencia_ultimo_mes=calc_asistencia_global(mes_inicio),
        asistencia_ultimo_ano=calc_asistencia_global(ano_inicio),
        asistencia_total=calc_asistencia_global(),
        discipulado_no_iniciado=count_formacion("discipulado_inicial", "no_iniciado"),
        discipulado_cursando=count_formacion("discipulado_inicial", "cursando"),
        discipulado_terminado=count_formacion("discipulado_inicial", "terminado"),
        pre_batismo_no_iniciado=count_formacion("pre_batismo", "no_iniciado"),
        pre_batismo_cursando=count_formacion("pre_batismo", "cursando"),
        pre_batismo_terminado=count_formacion("pre_batismo", "terminado"),
        escuela_biblica_no_iniciado=count_formacion("escuela_biblica", "no_iniciado"),
        escuela_biblica_cursando=count_formacion("escuela_biblica", "cursando"),
        escuela_biblica_terminado=count_formacion("escuela_biblica", "terminado"),
        escuela_discipulado_no_iniciado=count_formacion("escuela_discipulado", "no_iniciado"),
        escuela_discipulado_cursando=count_formacion("escuela_discipulado", "cursando"),
        escuela_discipulado_terminado=count_formacion("escuela_discipulado", "terminado"),
        treinamento_no_iniciado=count_formacion("treinamento", "no_iniciado"),
        treinamento_cursando=count_formacion("treinamento", "cursando"),
        treinamento_terminado=count_formacion("treinamento", "terminado"),
        total_oraciones=total_oraciones,
        oraciones_respondidas=oraciones_respondidas,
        testimonios_destacados=testimonios_destacados,
    )


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.on_event("startup")
def startup_event():
    db = next(get_db())
    try:
        if db.query(models.User).count() == 0:
            from seed import seed_database
            seed_database(db)
    finally:
        db.close()
