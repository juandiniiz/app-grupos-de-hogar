"""Seed script: populates the database with realistic Spanish church data."""
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
import models
import auth as auth_utils


def seed_database(db: Session):
    print("Seeding database...")

    # ── Integrantes (created first so we can link users) ─────────
    personas_raw = [
        # (nombre, apellidos, email, telefono, fecha_nac, is_membro, bautizado, novo_crente, novo_batizado,
        #  iglesia_procedente, iglesia_proc_nome, discipulado, pre_bat, esc_bib, esc_disc, trein, lat, lng)
        ("Carlos",    "Martínez López",    "carlos.martinez@gmail.com",    "+34 612 345 678", date(1985, 3, 15),  True,  True,  False, False, True,  "CCLN",             "terminado",   "terminado",   "terminado",   "cursando",    "no_iniciado", 39.4920, -0.3775),
        ("Ana",       "Rodríguez Pérez",   "ana.rodriguez@gmail.com",      "+34 623 456 789", date(1990, 7, 22),  True,  True,  False, False, True,  "Iglesia Bautista", "terminado",   "cursando",    "terminado",   "no_iniciado", "no_iniciado", 39.4851, -0.3642),
        ("Miguel",    "Fernández García",  "miguel.fernandez@gmail.com",   "+34 634 567 890", date(1978, 11, 5),  True,  True,  False, False, True,  "CCLN",             "terminado",   "terminado",   "no_iniciado", "no_iniciado", "no_iniciado", 39.4780, -0.3810),
        ("Laura",     "González Sánchez",  "laura.gonzalez@gmail.com",     "+34 645 678 901", date(1995, 2, 28),  True,  True,  False, True,  True,  "CCLN",             "terminado",   "terminado",   "cursando",    "cursando",    "no_iniciado", 39.4999, -0.3700),
        ("Pedro",     "López Díaz",        "pedro.lopez@gmail.com",        "+34 656 789 012", date(1982, 9, 14),  True,  True,  False, False, True,  "Nueva Vida",       "terminado",   "terminado",   "terminado",   "terminado",   "cursando",    39.4730, -0.3550),
        ("Isabel",    "Martín Torres",     "isabel.martin@gmail.com",      "+34 667 890 123", date(1988, 6, 30),  True,  True,  False, False, False, None,               "terminado",   "terminado",   "cursando",    "no_iniciado", "no_iniciado", 39.4660, -0.3720),
        ("José",      "Sánchez Ruiz",      "jose.sanchez@gmail.com",       "+34 678 901 234", date(1975, 12, 1),  True,  True,  False, False, True,  "Comunidad Cristiana", "terminado", "terminado",  "terminado",   "terminado",   "terminado",   39.4810, -0.3490),
        ("Carmen",    "Díaz Moreno",       "carmen.diaz@gmail.com",        "+34 689 012 345", date(1992, 4, 17),  True,  True,  False, True,  False, None,               "cursando",    "cursando",    "no_iniciado", "no_iniciado", "no_iniciado", 39.4950, -0.3860),
        ("Antonio",   "Ruiz Jiménez",      "antonio.ruiz@gmail.com",       "+34 690 123 456", date(1980, 8, 23),  True,  True,  False, False, True,  "CCLN",             "terminado",   "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", 39.4700, -0.3600),
        ("Elena",     "Moreno Álvarez",    "elena.moreno@gmail.com",       "+34 601 234 567", date(1997, 1, 9),   False, False, True,  False, False, None,               "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", 39.5050, -0.3750),
        ("Francisco", "Jiménez Castro",    "fran.jimenez@gmail.com",       "+34 612 345 000", date(1973, 5, 18),  True,  True,  False, False, True,  "Vida Nueva",       "terminado",   "terminado",   "cursando",    "no_iniciado", "no_iniciado", 39.4620, -0.3680),
        ("Sofía",     "Álvarez Romero",    "sofia.alvarez@gmail.com",      "+34 623 456 111", date(1994, 10, 25), True,  True,  False, True,  False, None,               "cursando",    "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", 39.4880, -0.3820),
        ("David",     "Castro Navarro",    "david.castro@gmail.com",       "+34 634 567 222", date(1989, 3, 7),   True,  True,  False, False, False, None,               "terminado",   "cursando",    "no_iniciado", "no_iniciado", "no_iniciado", 39.4760, -0.3490),
        ("Lucía",     "Navarro Serrano",   "lucia.navarro@gmail.com",      "+34 645 678 333", date(2000, 7, 14),  False, False, True,  False, False, None,               "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", 39.5020, -0.3580),
        ("Alejandro", "Serrano Molina",    "alex.serrano@gmail.com",       "+34 656 789 444", date(1986, 11, 29), True,  True,  False, False, True,  "CCLN",             "terminado",   "terminado",   "terminado",   "cursando",    "cursando",    39.4690, -0.3760),
        ("Marta",     "Molina Ortega",     "marta.molina@gmail.com",       "+34 667 890 555", date(1993, 2, 3),   True,  True,  False, True,  True,  "Roca de Refugio",  "terminado",   "cursando",    "no_iniciado", "no_iniciado", "no_iniciado", 39.4970, -0.3630),
        ("Javier",    "Ortega Delgado",    "javier.ortega@gmail.com",      "+34 678 901 666", date(1977, 6, 21),  True,  True,  False, False, True,  "CCLN",             "terminado",   "terminado",   "cursando",    "no_iniciado", "no_iniciado", 39.4840, -0.3870),
        ("Nuria",     "Delgado Vega",      "nuria.delgado@gmail.com",      "+34 689 012 777", date(1999, 9, 8),   False, False, True,  False, False, None,               "cursando",    "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", 39.4910, -0.3710),
        ("Roberto",   "Vega Iglesias",     "roberto.vega@gmail.com",       "+34 690 123 888", date(1983, 4, 16),  True,  True,  False, False, False, None,               "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", 39.4750, -0.3530),
        ("Patricia",  "Iglesias Blanco",   "patricia.iglesias@gmail.com",  "+34 601 234 999", date(1991, 12, 27), True,  True,  False, True,  True,  "CCLN",             "terminado",   "terminado",   "cursando",    "cursando",    "no_iniciado", 39.4830, -0.3660),
    ]

    integrantes_objs = []
    for (nombre, apellidos, email, tel, fnac, is_mb, baut, novo_c, novo_b,
         igl_proc, igl_nome, disc, pre_bat, esc_bib, esc_disc, trein, lat, lng) in personas_raw:
        i = models.Integrante(
            nombre=nombre,
            apellidos=apellidos,
            email=email,
            telefono=tel,
            fecha_nacimiento=fnac,
            latitude=lat,
            longitude=lng,
            is_membro=is_mb,
            bautizado=baut,
            novo_crente=novo_c,
            novo_batizado=novo_b,
            iglesia_procedente=igl_proc,
            iglesia_procedente_nome=igl_nome,
            discipulado_inicial=disc,
            pre_batismo=pre_bat,
            escuela_biblica=esc_bib,
            escuela_discipulado=esc_disc,
            treinamento=trein,
            activo=True,
        )
        db.add(i)
        integrantes_objs.append(i)

    db.flush()
    for i in integrantes_objs:
        db.refresh(i)

    # ── Users ────────────────────────────────────────────────────
    admin = models.User(
        email="admin@puntodeencuentro.es",
        password_hash=auth_utils.get_password_hash("admin1234"),
        nombre="Pastor Admin",
        rol="admin",
        activo=True,
        integrante_id=integrantes_objs[0].id,
    )
    supervisor_user = models.User(
        email="supervisor@puntodeencuentro.es",
        password_hash=auth_utils.get_password_hash("super1234"),
        nombre="Ana Rodríguez",
        rol="supervisor",
        activo=True,
        integrante_id=integrantes_objs[1].id,
    )
    responsable_user = models.User(
        email="responsable@puntodeencuentro.es",
        password_hash=auth_utils.get_password_hash("resp1234"),
        nombre="Carlos Martínez",
        rol="responsable",
        activo=True,
        integrante_id=integrantes_objs[0].id,
    )
    db.add(admin)
    db.add(supervisor_user)
    db.add(responsable_user)

    # ── Grupos ────────────────────────────────────────────────────
    grupos_data = [
        # (nombre, dia, hora, frecuencia, responsable_idx, ayudante_idx, supervisor_idx, endereco, lat, lng)
        ("Grupo Norte",    "lunes",    "19:30", "semanal",   0, 3, 1, "Calle Mayor 12, Valencia",    39.4920, -0.3775),
        ("Grupo Sur",      "miercoles","20:00", "semanal",   4, 7, 5, "Avenida del Puerto 45, Valencia", 39.4660, -0.3720),
        ("Grupo Centro",   "jueves",   "19:00", "quincenal", 6, 11, 1, "Plaza del Ayuntamiento 3, Valencia", 39.4700, -0.3760),
        ("Grupo Jóvenes",  "viernes",  "18:00", "semanal",   2, 13, 1, "Calle Colón 8, Valencia",    39.4780, -0.3810),
        ("Grupo Familias", "sabado",   "10:30", "mensual",   14, 19, 5, "Paseo de la Alameda 20, Valencia", 39.4730, -0.3550),
    ]

    grupos_objs = []
    for (nombre, dia, hora, frec, resp_idx, ayu_idx, sup_idx, end, lat, lng) in grupos_data:
        g = models.Grupo(
            nombre=nombre,
            dia_semana=dia,
            hora=hora,
            frecuencia=frec,
            responsable_id=integrantes_objs[resp_idx].id,
            ayudante_id=integrantes_objs[ayu_idx].id,
            supervisor_id=integrantes_objs[sup_idx].id,
            endereco=end,
            latitude=lat,
            longitude=lng,
            activo=True,
        )
        db.add(g)
        grupos_objs.append(g)

    db.flush()
    for g in grupos_objs:
        db.refresh(g)

    # ── Assign integrantes to grupos with roles ───────────────────
    # (integrante_idx, grupo_idx, rol)
    assignments = [
        # Grupo Norte
        (0, 0, "responsable"),
        (3, 0, "ayudante"),
        (7, 0, "member"),
        (9, 0, "member"),
        # Grupo Sur
        (4, 1, "responsable"),
        (5, 1, "supervisor"),
        (7, 1, "ayudante"),
        (11, 1, "member"),
        # Grupo Centro
        (6, 2, "responsable"),
        (2, 2, "member"),
        (8, 2, "member"),
        (10, 2, "member"),
        # Grupo Jóvenes
        (2, 3, "responsable"),
        (12, 3, "member"),
        (13, 3, "member"),
        (16, 3, "member"),
        # Grupo Familias
        (14, 4, "responsable"),
        (15, 4, "member"),
        (17, 4, "member"),
        (18, 4, "member"),
        (19, 4, "ayudante"),
    ]
    for i_idx, g_idx, rol in assignments:
        gi = models.GrupoIntegrante(
            grupo_id=grupos_objs[g_idx].id,
            integrante_id=integrantes_objs[i_idx].id,
            rol_en_grupo=rol,
        )
        db.add(gi)

    # ── Ministerios ──────────────────────────────────────────────
    ministerios_data = [
        ("Alabanza", "Ministerio de música y adoración para los cultos dominicales."),
        ("Jóvenes",  "Actividades y discipulado para jóvenes de 12 a 25 años."),
        ("Evangelismo", "Salidas de evangelismo y alcance comunitario."),
    ]
    ministerios_objs = []
    for nombre, desc in ministerios_data:
        m = models.Ministerio(nombre=nombre, descripcion=desc)
        db.add(m)
        ministerios_objs.append(m)

    db.flush()
    for m in ministerios_objs:
        db.refresh(m)

    # ── Ministerio tarefas ───────────────────────────────────────
    tarefas_data = [
        (0, "Sonido"),
        (0, "Guitarra"),
        (0, "Voz principal"),
        (1, "Coordinación eventos"),
        (1, "Redes sociales"),
        (2, "Visitas domiciliarias"),
        (2, "Distribución de folletos"),
    ]
    tarefas_objs = []
    for min_idx, nombre in tarefas_data:
        t = models.MinisterioTarefa(ministerio_id=ministerios_objs[min_idx].id, nombre=nombre)
        db.add(t)
        tarefas_objs.append(t)

    db.flush()
    for t in tarefas_objs:
        db.refresh(t)

    # ── Assign integrantes to ministerios ────────────────────────
    min_assignments = [
        # (integrante_idx, ministerio_idx, es_responsable)
        (3, 0, True),
        (7, 0, False),
        (11, 0, False),
        (13, 1, True),
        (16, 1, False),
        (17, 1, False),
        (6, 2, True),
        (14, 2, False),
        (19, 2, False),
    ]
    for i_idx, m_idx, es_resp in min_assignments:
        mi = models.MinisterioIntegrante(
            ministerio_id=ministerios_objs[m_idx].id,
            integrante_id=integrantes_objs[i_idx].id,
            es_responsable=es_resp,
        )
        db.add(mi)

    # ── Assign integrantes to tarefas ────────────────────────────
    tarefa_assignments = [
        (0, 7),   # Sonido -> Carmen
        (1, 3),   # Guitarra -> Laura
        (2, 11),  # Voz -> Sofía
        (3, 13),  # Coord eventos -> Lucía
        (4, 16),  # Redes -> Javier
        (5, 6),   # Visitas -> José
        (6, 14),  # Folletos -> Alejandro
    ]
    for t_idx, i_idx in tarefa_assignments:
        ti = models.MinisterioTarefaIntegrante(
            tarefa_id=tarefas_objs[t_idx].id,
            integrante_id=integrantes_objs[i_idx].id,
        )
        db.add(ti)

    db.commit()

    # ── Reuniones ─────────────────────────────────────────────────
    today = date.today()
    # Spread 10 reuniones over last 3 months
    reuniones_raw = [
        # (grupo_idx, days_ago, hora, tipo, asistentes, visitantes, novos_crentes, notas)
        (0, 7,  "19:30", "periodica",     8, 2, 0, "Buen ambiente, oramos por las misiones"),
        (0, 14, "19:30", "periodica",     7, 1, 0, "Estudio de Hechos 2"),
        (0, 21, "evangelistica", "evangelistica", 10, 5, 2, "Noche de evangelismo. Dos personas aceptaron a Cristo."),
        (1, 5,  "20:00", "periodica",     10, 1, 0, "Testimonio de Pedro muy edificante"),
        (1, 12, "20:00", "comunhao",      9,  0, 0, "Noche de comunión y alabanza"),
        (2, 9,  "19:00", "periodica",     6,  2, 1, "Estudio Romanos 8. Un visitante tomó decisión."),
        (2, 30, "19:00", "periodica",     5,  1, 0, "Estudio sobre la oración"),
        (3, 3,  "18:00", "periodica",     12, 4, 1, "Noche de adoración joven"),
        (4, 10, "10:30", "comunhao",      15, 2, 0, "Desayuno compartido y oración"),
        (4, 60, "10:30", "evangelistica", 18, 6, 3, "Reunión de evangelismo familiar"),
    ]

    reuniones_objs = []
    for (g_idx, days_ago, hora_or_tipo, tipo, asist, visit, novos, notas) in reuniones_raw:
        # Fix: if hora_or_tipo looks like a tipo, set hora to a default
        if ":" in hora_or_tipo:
            hora_val = hora_or_tipo
        else:
            tipo = hora_or_tipo
            hora_val = "19:00"

        r = models.Reunion(
            grupo_id=grupos_objs[g_idx].id,
            fecha=today - timedelta(days=days_ago),
            hora=hora_val,
            tipo=tipo,
            asistentes_count=asist,
            visitantes_count=visit,
            novos_crentes_count=novos,
            notas=notas,
        )
        db.add(r)
        reuniones_objs.append(r)

    db.flush()
    for r in reuniones_objs:
        db.refresh(r)

    # ── Asistencia ────────────────────────────────────────────────
    # For each reunion, create IntegranteReunion records
    grupo_miembros = {}
    for gi in db.query(models.GrupoIntegrante).all():
        grupo_miembros.setdefault(gi.grupo_id, []).append(gi.integrante_id)

    import random
    random.seed(42)
    for r in reuniones_objs:
        miembros = grupo_miembros.get(r.grupo_id, [])
        for integrante_id in miembros:
            presente = random.random() > 0.3  # ~70% attendance
            ir = models.IntegranteReunion(
                integrante_id=integrante_id,
                reunion_id=r.id,
                presente=presente,
            )
            db.add(ir)

    # ── Oraciones de reunion ─────────────────────────────────────
    oracao_data = [
        (0, "Sanidad para la madre de Carlos", False, None),
        (0, "Trabajo para Elena", False, None),
        (4, "Restauración de matrimonio en el grupo", True, today - timedelta(days=8)),
        (7, "Dirección para los jóvenes en sus estudios", False, None),
    ]
    for r_idx, texto, respondida, fecha_resp in oracao_data:
        o = models.OracaoReunion(
            reunion_id=reuniones_objs[r_idx].id,
            texto=texto,
            respondida=respondida,
            fecha_respondida=fecha_resp,
        )
        db.add(o)

    # ── Testimonios ───────────────────────────────────────────────
    testimonios_data = [
        # (titulo, contenido, integrante_idx, grupo_idx, reunion_idx, days_ago, destacado)
        (
            "Dios sanó mi rodilla",
            "Durante la reunión del grupo, el Señor me sanó de un dolor crónico en la rodilla que me afectaba hace años. ¡Aleluya!",
            4, 1, 3, 5, True,
        ),
        (
            "Trabajo inesperado",
            "Llevaba 6 meses desempleado y confiando en Dios. Esta semana me llamaron para una entrevista y me contrataron el mismo día. Su fidelidad es grande.",
            7, 1, 4, 12, True,
        ),
        (
            "Paz en la tormenta",
            "Atravesé una crisis familiar muy dura pero Dios me sostuvo en cada momento. Su paz sobrepasa todo entendimiento.",
            11, 1, None, 25, False,
        ),
        (
            "Primera vez en el grupo",
            "Vine por primera vez a un grupo de hogar con mucho miedo, pero sentí el amor de Dios a través de estas personas desde el primer momento.",
            13, 3, 7, 3, False,
        ),
        (
            "Familia reconciliada",
            "Después de tres años sin hablar con mi padre, Dios obró un milagro y nos reconciliamos en Navidad. El grupo oró por esto durante meses.",
            14, 4, None, 15, True,
        ),
    ]
    for (titulo, contenido, i_idx, g_idx, r_idx, days_ago, dest) in testimonios_data:
        t = models.Testimonio(
            titulo=titulo,
            contenido=contenido,
            integrante_id=integrantes_objs[i_idx].id,
            grupo_id=grupos_objs[g_idx].id,
            reunion_id=reuniones_objs[r_idx].id if r_idx is not None else None,
            fecha=today - timedelta(days=days_ago),
            destacado=dest,
        )
        db.add(t)

    # ── Servicios ─────────────────────────────────────────────────
    servicios_data = [
        ("Culto Dominical",      today - timedelta(days=7),  "Culto dominical de adoración y predicación"),
        ("Noche de Adoración",   today - timedelta(days=21), "Noche especial de adoración con todos los grupos"),
        ("Culto de Bienvenida",  today - timedelta(days=35), "Culto especial para nuevos visitantes e integrantes"),
    ]
    servicios_objs = []
    for titulo, fecha_d, desc in servicios_data:
        s = models.Servicio(
            titulo=titulo,
            fecha=datetime.combine(fecha_d, datetime.min.time()).replace(hour=11),
            descripcion=desc,
        )
        db.add(s)
        servicios_objs.append(s)

    db.flush()
    for s in servicios_objs:
        db.refresh(s)

    # Assign some integrantes to servicios
    servicio_asignaciones = [
        (0, [0, 3, 6]),
        (1, [3, 7, 11]),
        (2, [0, 1, 4, 6]),
    ]
    for s_idx, i_idxs in servicio_asignaciones:
        for i_idx in i_idxs:
            si = models.ServicioIntegrante(
                servicio_id=servicios_objs[s_idx].id,
                integrante_id=integrantes_objs[i_idx].id,
            )
            db.add(si)

    # ── Oraciones personales ─────────────────────────────────────
    oraciones_data = [
        ("Sanidad para mi madre",   "Mi madre tiene una operación próximamente, pido oración por su recuperación.", 0, None, today - timedelta(days=5), False),
        ("Trabajo nuevo",           "Estoy buscando empleo y necesito dirección de Dios.", 3, None, today - timedelta(days=10), False),
        ("Matrimonio restaurado",   "Gracias a Dios mi matrimonio está mejorando. ¡Oración respondida!", 6, None, today - timedelta(days=30), True),
        ("Hijo pródigo",            "Mi hijo se alejó de Dios. Pido que vuelva a casa.", 9, None, today - timedelta(days=8), False),
        ("Misiones en África",      "Orar por el equipo misionero que sale el próximo mes.", 2, 2, today - timedelta(days=3), False),
    ]
    for titulo, desc, i_idx, g_idx, fecha_d, respondida in oraciones_data:
        o = models.Oracion(
            titulo=titulo,
            descripcion=desc,
            integrante_id=integrantes_objs[i_idx].id,
            grupo_id=grupos_objs[g_idx].id if g_idx is not None else None,
            fecha=fecha_d,
            respondida=respondida,
        )
        db.add(o)

    db.commit()

    print("Database seeded successfully!")
    print("Admin:       admin@puntodeencuentro.es / admin1234")
    print("Supervisor:  supervisor@puntodeencuentro.es / super1234")
    print("Responsable: responsable@puntodeencuentro.es / resp1234")
