"""Seed script: populates the database with realistic Spanish church data."""
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
import models
import auth as auth_utils


def seed_database(db: Session):
    if db.query(models.User).count() > 0:
        print("Database already seeded, skipping.")
        return

    print("Seeding database...")
    today = date.today()

    # ── Integrantes ──────────────────────────────────────────────────────────
    # Columns: nombre, apellidos, email, telefono, fecha_nacimiento,
    #          endereco, latitude, longitude,
    #          is_membro, bautizado, novo_crente, novo_batizado,
    #          iglesia_procedente, iglesia_procedente_nome,
    #          discipulado_inicial, pre_batismo, escuela_biblica,
    #          escuela_discipulado, treinamento,
    #          numero_membro, observaciones
    personas_raw = [
        # 0 - Carlos Méndez (supervisor user)
        (
            "Carlos", "Méndez", "carlos.mendez@ccln.es", "634 512 301",
            date(1982, 4, 12),
            "Calle Colón 15, Valencia", 39.4750, -0.3760,
            True, True, False, False,
            False, None,
            "terminado", "terminado", "cursando", "no_iniciado", "no_iniciado",
            1, "Líder consolidado del grupo Norte",
        ),
        # 1 - Lucía Torres (responsable user)
        (
            "Lucía", "Torres", "lucia.torres@ccln.es", "621 487 902",
            date(1988, 9, 3),
            "Av. del Cid 22, Valencia", 39.4650, -0.3850,
            True, True, False, False,
            False, None,
            "terminado", "terminado", "no_iniciado", "no_iniciado", "no_iniciado",
            2, "Responsable del grupo Sur",
        ),
        # 2 - Miguel Santos (ayudante user)
        (
            "Miguel", "Santos", "miguel.santos@ccln.es", "698 234 115",
            date(1990, 1, 25),
            "Calle Xátiva 8, Valencia", 39.4700, -0.3700,
            True, True, False, False,
            False, None,
            "cursando", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado",
            3, "Ayudante activo en el grupo Norte",
        ),
        # 3 - Ana García
        (
            "Ana", "García", "ana.garcia@gmail.com", "612 389 047",
            date(2001, 6, 18),
            "Calle de la Paz 7, Valencia", 39.4720, -0.3740,
            False, False, True, False,
            False, None,
            "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado",
            None, "Nueva creyente, comenzó a asistir hace 3 meses",
        ),
        # 4 - Roberto Silva
        (
            "Roberto", "Silva", "roberto.silva@gmail.com", "645 778 230",
            date(1977, 11, 7),
            "Plaza del Ayuntamiento 1, Valencia", 39.4693, -0.3773,
            True, True, False, False,
            True, "Iglesia Bautista Central",
            "terminado", "terminado", "terminado", "cursando", "no_iniciado",
            4, "Procede de iglesia bautista, experiencia ministerial",
        ),
        # 5 - Elena Martínez
        (
            "Elena", "Martínez", "elena.martinez@gmail.com", "666 102 844",
            date(1995, 3, 30),
            "Calle Xátiva 8, Valencia", 39.4703, -0.3698,
            True, True, False, True,
            False, None,
            "terminado", "terminado", "no_iniciado", "no_iniciado", "no_iniciado",
            5, "Recién bautizada, responsable del grupo Este",
        ),
        # 6 - David Rodríguez
        (
            "David", "Rodríguez", "david.rodriguez@gmail.com", "677 345 912",
            date(1987, 7, 14),
            "Calle de Sagunto 3, Valencia", 39.4810, -0.3680,
            True, True, False, False,
            False, None,
            "terminado", "cursando", "no_iniciado", "no_iniciado", "no_iniciado",
            6, None,
        ),
        # 7 - Carmen López
        (
            "Carmen", "López", "carmen.lopez@gmail.com", "609 567 333",
            date(1993, 12, 5),
            "Gran Vía Marqués del Turia 18, Valencia", 39.4680, -0.3770,
            True, False, False, False,
            False, None,
            "cursando", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado",
            None, "En proceso de discipulado",
        ),
        # 8 - Alejandro Gómez
        (
            "Alejandro", "Gómez", "alejandro.gomez@gmail.com", "633 901 478",
            date(1985, 8, 22),
            "Av. del Puerto 12, Valencia", 39.4660, -0.3720,
            True, True, False, False,
            True, "Comunidad Cristiana Vida Nueva",
            "terminado", "terminado", "cursando", "no_iniciado", "no_iniciado",
            7, None,
        ),
        # 9 - Isabel Fernández
        (
            "Isabel", "Fernández", "isabel.fernandez@gmail.com", "655 234 890",
            date(1980, 2, 17),
            "Calle Cirilo Amorós 9, Valencia", 39.4670, -0.3760,
            True, True, False, False,
            False, None,
            "terminado", "terminado", "terminado", "terminado", "no_iniciado",
            8, "Voluntaria en múltiples ministerios",
        ),
        # 10 - Manuel Pérez
        (
            "Manuel", "Pérez", "manuel.perez@gmail.com", "618 456 721",
            date(1975, 5, 9),
            "Plaza del Ayuntamiento 1, Valencia", 39.4693, -0.3775,
            True, True, False, False,
            True, "Iglesia Evangélica de Valencia",
            "terminado", "terminado", "terminado", "cursando", "cursando",
            9, "Responsable del grupo Centro",
        ),
        # 11 - Sofía Ruiz
        (
            "Sofía", "Ruiz", "sofia.ruiz@gmail.com", "682 109 634",
            date(1998, 10, 11),
            "Calle de Guillem de Castro 25, Valencia", 39.4730, -0.3820,
            True, True, False, False,
            False, None,
            "cursando", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado",
            None, None,
        ),
        # 12 - Francisco Jiménez
        (
            "Francisco", "Jiménez", "francisco.jimenez@gmail.com", "644 832 057",
            date(1970, 3, 28),
            "Av. de la Plata 5, Valencia", 39.4720, -0.3950,
            True, True, False, False,
            True, "Iglesia Pentecostal Rey de Reyes",
            "terminado", "terminado", "terminado", "terminado", "terminado",
            10, "Responsable del grupo Oeste",
        ),
        # 13 - Laura Moreno
        (
            "Laura", "Moreno", "laura.moreno@gmail.com", "671 345 218",
            date(1997, 6, 4),
            "Calle de la Blanquería 11, Valencia", 39.4780, -0.3710,
            False, False, False, False,
            False, None,
            "cursando", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado",
            None, "Asiste regularmente, en proceso de membresía",
        ),
        # 14 - Joaquín Díaz
        (
            "Joaquín", "Díaz", "joaquin.diaz@gmail.com", "628 903 461",
            date(1989, 1, 16),
            "Calle de Sorní 6, Valencia", 39.4720, -0.3680,
            True, True, False, False,
            False, None,
            "terminado", "cursando", "no_iniciado", "no_iniciado", "no_iniciado",
            11, None,
        ),
        # 15 - Patricia Navarro
        (
            "Patricia", "Navarro", "patricia.navarro@gmail.com", "657 012 839",
            date(1992, 8, 27),
            "Calle de la Reina 8, Valencia", 39.4650, -0.3800,
            True, True, False, False,
            False, None,
            "terminado", "terminado", "no_iniciado", "no_iniciado", "no_iniciado",
            12, "Evangelista comprometida",
        ),
        # 16 - Sergio Castro
        (
            "Sergio", "Castro", "sergio.castro@gmail.com", "693 567 104",
            date(1983, 11, 19),
            "Av. del Cid 30, Valencia", 39.4648, -0.3856,
            True, True, False, False,
            False, None,
            "terminado", "terminado", "no_iniciado", "no_iniciado", "no_iniciado",
            13, None,
        ),
        # 17 - Cristina Herrera
        (
            "Cristina", "Herrera", "cristina.herrera@gmail.com", "614 789 325",
            date(1996, 4, 8),
            "Calle Xátiva 12, Valencia", 39.4698, -0.3702,
            True, True, False, True,
            False, None,
            "terminado", "terminado", "no_iniciado", "no_iniciado", "no_iniciado",
            14, "Participa en ministerio de alabanza",
        ),
        # 18 - Alberto Vega
        (
            "Alberto", "Vega", "alberto.vega@gmail.com", "639 456 870",
            date(1994, 9, 2),
            "Calle de Caballeros 17, Valencia", 39.4750, -0.3790,
            True, True, False, False,
            False, None,
            "cursando", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado",
            None, None,
        ),
        # 19 - Natalia Reyes
        (
            "Natalia", "Reyes", "natalia.reyes@gmail.com", "661 234 987",
            date(1999, 7, 15),
            "Av. de la Plata 9, Valencia", 39.4718, -0.3948,
            False, False, False, False,
            False, None,
            "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado", "no_iniciado",
            None, "Nueva asistente, muy interesada en crecer",
        ),
    ]

    integrantes_objs = []
    for idx, (
        nombre, apellidos, email, telefono, fecha_nacimiento,
        endereco, latitude, longitude,
        is_membro, bautizado, novo_crente, novo_batizado,
        iglesia_procedente, iglesia_procedente_nome,
        discipulado_inicial, pre_batismo, escuela_biblica,
        escuela_discipulado, treinamento,
        numero_membro, observaciones,
    ) in enumerate(personas_raw):
        i = models.Integrante(
            nombre=nombre,
            apellidos=apellidos,
            email=email,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            endereco=endereco,
            latitude=latitude,
            longitude=longitude,
            is_membro=is_membro,
            bautizado=bautizado,
            novo_crente=novo_crente,
            novo_batizado=novo_batizado,
            iglesia_procedente=iglesia_procedente,
            iglesia_procedente_nome=iglesia_procedente_nome,
            discipulado_inicial=discipulado_inicial,
            pre_batismo=pre_batismo,
            escuela_biblica=escuela_biblica,
            escuela_discipulado=escuela_discipulado,
            treinamento=treinamento,
            numero_membro=numero_membro,
            observaciones=observaciones,
            activo=True,
        )
        db.add(i)
        integrantes_objs.append(i)

    db.flush()
    for i in integrantes_objs:
        db.refresh(i)

    # Short aliases
    carlos    = integrantes_objs[0]   # Carlos Méndez
    lucia     = integrantes_objs[1]   # Lucía Torres
    miguel    = integrantes_objs[2]   # Miguel Santos
    ana       = integrantes_objs[3]   # Ana García
    roberto   = integrantes_objs[4]   # Roberto Silva
    elena     = integrantes_objs[5]   # Elena Martínez
    david     = integrantes_objs[6]   # David Rodríguez
    carmen    = integrantes_objs[7]   # Carmen López
    alejandro = integrantes_objs[8]   # Alejandro Gómez
    isabel    = integrantes_objs[9]   # Isabel Fernández
    manuel    = integrantes_objs[10]  # Manuel Pérez
    sofia     = integrantes_objs[11]  # Sofía Ruiz
    francisco = integrantes_objs[12]  # Francisco Jiménez
    laura     = integrantes_objs[13]  # Laura Moreno
    joaquin   = integrantes_objs[14]  # Joaquín Díaz
    patricia  = integrantes_objs[15]  # Patricia Navarro
    sergio    = integrantes_objs[16]  # Sergio Castro
    cristina  = integrantes_objs[17]  # Cristina Herrera
    alberto   = integrantes_objs[18]  # Alberto Vega
    natalia   = integrantes_objs[19]  # Natalia Reyes

    # ── Users ────────────────────────────────────────────────────────────────
    user_admin = models.User(
        email="admin@puntodeencuentro.es",
        password_hash=auth_utils.get_password_hash("admin1234"),
        nombre="Pastor Admin",
        rol="admin",
        activo=True,
        integrante_id=None,
    )
    user_supervisor = models.User(
        email="carlos.mendez@ccln.es",
        password_hash=auth_utils.get_password_hash("super1234"),
        nombre="Carlos Méndez",
        rol="supervisor",
        activo=True,
        integrante_id=carlos.id,
    )
    user_responsable = models.User(
        email="lucia.torres@ccln.es",
        password_hash=auth_utils.get_password_hash("resp1234"),
        nombre="Lucía Torres",
        rol="responsable",
        activo=True,
        integrante_id=lucia.id,
    )
    user_ayudante = models.User(
        email="miguel.santos@ccln.es",
        password_hash=auth_utils.get_password_hash("ayud1234"),
        nombre="Miguel Santos",
        rol="ayudante",
        activo=True,
        integrante_id=miguel.id,
    )
    db.add(user_admin)
    db.add(user_supervisor)
    db.add(user_responsable)
    db.add(user_ayudante)
    db.flush()

    # ── Grupos ───────────────────────────────────────────────────────────────
    grupo_norte = models.Grupo(
        nombre="Grupo Norte",
        dia_semana="lunes",
        hora="19:30",
        frecuencia="semanal",
        responsable_id=carlos.id,
        supervisor_id=roberto.id,
        ayudante_id=miguel.id,
        endereco="Calle Colón 15, Valencia",
        latitude=39.4750,
        longitude=-0.3760,
        observaciones="Grupo consolidado con varios años de trayectoria.",
        activo=True,
    )
    grupo_sur = models.Grupo(
        nombre="Grupo Sur",
        dia_semana="miercoles",
        hora="20:00",
        frecuencia="quincenal",
        responsable_id=lucia.id,
        supervisor_id=carlos.id,
        ayudante_id=None,
        endereco="Av. del Cid 22, Valencia",
        latitude=39.4650,
        longitude=-0.3850,
        observaciones="Grupo en crecimiento, zona residencial sur.",
        activo=True,
    )
    grupo_este = models.Grupo(
        nombre="Grupo Este",
        dia_semana="jueves",
        hora="19:00",
        frecuencia="semanal",
        responsable_id=elena.id,
        supervisor_id=carlos.id,
        ayudante_id=None,
        endereco="Calle Xátiva 8, Valencia",
        latitude=39.4700,
        longitude=-0.3700,
        observaciones="Grupo joven liderado por Elena.",
        activo=True,
    )
    grupo_oeste = models.Grupo(
        nombre="Grupo Oeste",
        dia_semana="viernes",
        hora="18:30",
        frecuencia="mensual",
        responsable_id=francisco.id,
        supervisor_id=None,
        ayudante_id=None,
        endereco="Av. de la Plata 5, Valencia",
        latitude=39.4720,
        longitude=-0.3950,
        observaciones="Grupo mensual con familias de la zona oeste.",
        activo=True,
    )
    grupo_centro = models.Grupo(
        nombre="Grupo Centro",
        dia_semana="sabado",
        hora="11:00",
        frecuencia="quincenal",
        responsable_id=manuel.id,
        supervisor_id=carlos.id,
        ayudante_id=None,
        endereco="Plaza del Ayuntamiento 1, Valencia",
        latitude=39.4693,
        longitude=-0.3773,
        observaciones="Grupo céntrico con diversidad de perfiles.",
        activo=True,
    )
    db.add(grupo_norte)
    db.add(grupo_sur)
    db.add(grupo_este)
    db.add(grupo_oeste)
    db.add(grupo_centro)
    db.flush()
    for g in [grupo_norte, grupo_sur, grupo_este, grupo_oeste, grupo_centro]:
        db.refresh(g)

    grupos_objs = [grupo_norte, grupo_sur, grupo_este, grupo_oeste, grupo_centro]

    # ── GrupoIntegrante assignments ──────────────────────────────────────────
    gi_data = [
        # Grupo Norte
        (grupo_norte.id, carlos.id,    "responsable"),
        (grupo_norte.id, miguel.id,    "ayudante"),
        (grupo_norte.id, roberto.id,   "supervisor"),
        (grupo_norte.id, ana.id,       "member"),
        (grupo_norte.id, elena.id,     "member"),
        (grupo_norte.id, david.id,     "member"),
        (grupo_norte.id, carmen.id,    "member"),
        # Grupo Sur
        (grupo_sur.id,   lucia.id,     "responsable"),
        (grupo_sur.id,   alejandro.id, "member"),
        (grupo_sur.id,   isabel.id,    "member"),
        (grupo_sur.id,   patricia.id,  "member"),
        (grupo_sur.id,   sergio.id,    "member"),
        # Grupo Este
        (grupo_este.id,  elena.id,     "responsable"),
        (grupo_este.id,  laura.id,     "member"),
        (grupo_este.id,  joaquin.id,   "member"),
        (grupo_este.id,  cristina.id,  "member"),
        (grupo_este.id,  alberto.id,   "member"),
        # Grupo Oeste
        (grupo_oeste.id, francisco.id, "responsable"),
        (grupo_oeste.id, natalia.id,   "member"),
        (grupo_oeste.id, sofia.id,     "member"),
        (grupo_oeste.id, david.id,     "member"),
        # Grupo Centro
        (grupo_centro.id, manuel.id,   "responsable"),
        (grupo_centro.id, carmen.id,   "member"),
        (grupo_centro.id, alberto.id,  "member"),
        (grupo_centro.id, natalia.id,  "member"),
        (grupo_centro.id, cristina.id, "member"),
    ]
    # Deduplicate (elena appears in Norte and Este - Norte only as member, Este as responsable)
    seen_gi = set()
    for grupo_id, integrante_id, rol in gi_data:
        key = (grupo_id, integrante_id)
        if key not in seen_gi:
            seen_gi.add(key)
            db.add(models.GrupoIntegrante(
                grupo_id=grupo_id,
                integrante_id=integrante_id,
                rol_en_grupo=rol,
            ))
    # david also in Norte and Oeste - both are fine since different grupos, already distinct keys above

    db.flush()

    # ── Ministerios ──────────────────────────────────────────────────────────
    min_alabanza = models.Ministerio(
        nombre="Ministerio de Alabanza",
        descripcion="Ministerio de música y adoración para los cultos dominicales y reuniones de grupos.",
    )
    min_jovenes = models.Ministerio(
        nombre="Ministerio de Jóvenes",
        descripcion="Actividades, campamentos y discipulado para jóvenes de 15 a 30 años.",
    )
    min_evangelismo = models.Ministerio(
        nombre="Ministerio de Evangelismo",
        descripcion="Alcance comunitario, visitas domiciliarias y evangelismo en redes sociales.",
    )
    db.add(min_alabanza)
    db.add(min_jovenes)
    db.add(min_evangelismo)
    db.flush()
    for m in [min_alabanza, min_jovenes, min_evangelismo]:
        db.refresh(m)

    # Tarefas de cada ministerio
    tarefas_alabanza_nombres = ["Guitarra eléctrica", "Piano/Teclado", "Vocales", "Batería"]
    tarefas_jovenes_nombres  = ["Coordinación de actividades", "Enseñanza", "Logística"]
    tarefas_evang_nombres    = ["Visitas domiciliarias", "Redes sociales", "Distribución materiales"]

    tarefas_alabanza = []
    for nombre in tarefas_alabanza_nombres:
        t = models.MinisterioTarefa(ministerio_id=min_alabanza.id, nombre=nombre)
        db.add(t)
        tarefas_alabanza.append(t)

    tarefas_jovenes = []
    for nombre in tarefas_jovenes_nombres:
        t = models.MinisterioTarefa(ministerio_id=min_jovenes.id, nombre=nombre)
        db.add(t)
        tarefas_jovenes.append(t)

    tarefas_evang = []
    for nombre in tarefas_evang_nombres:
        t = models.MinisterioTarefa(ministerio_id=min_evangelismo.id, nombre=nombre)
        db.add(t)
        tarefas_evang.append(t)

    db.flush()
    for t in tarefas_alabanza + tarefas_jovenes + tarefas_evang:
        db.refresh(t)

    # Integrantes de ministerios
    min_integrante_data = [
        # (ministerio_id, integrante, es_responsable)
        (min_alabanza.id,    carlos,   True),
        (min_alabanza.id,    elena,    False),
        (min_alabanza.id,    david,    False),
        (min_alabanza.id,    cristina, False),
        (min_jovenes.id,     miguel,   True),
        (min_jovenes.id,     ana,      False),
        (min_jovenes.id,     laura,    False),
        (min_jovenes.id,     joaquin,  False),
        (min_jovenes.id,     alberto,  False),
        (min_evangelismo.id, roberto,  True),
        (min_evangelismo.id, patricia, False),
        (min_evangelismo.id, sergio,   False),
        (min_evangelismo.id, natalia,  False),
    ]
    for min_id, integrante_obj, es_resp in min_integrante_data:
        db.add(models.MinisterioIntegrante(
            ministerio_id=min_id,
            integrante_id=integrante_obj.id,
            es_responsable=es_resp,
        ))

    db.flush()

    # ── Reuniones ────────────────────────────────────────────────────────────
    # Grupo Norte: 4 reuniones (3 periodica, 1 comunhao)
    r_norte_1 = models.Reunion(
        grupo_id=grupo_norte.id,
        fecha=today - timedelta(days=120),
        hora="19:30",
        tipo="periodica",
        asistentes_count=6,
        visitantes_count=1,
        novos_crentes_count=0,
        notas="Estudio de Filipenses 4. Buen tiempo de comunión.",
        observaciones=None,
    )
    r_norte_2 = models.Reunion(
        grupo_id=grupo_norte.id,
        fecha=today - timedelta(days=90),
        hora="19:30",
        tipo="periodica",
        asistentes_count=7,
        visitantes_count=2,
        novos_crentes_count=0,
        notas="Estudio sobre la fe. Dos visitantes del barrio.",
        observaciones=None,
    )
    r_norte_3 = models.Reunion(
        grupo_id=grupo_norte.id,
        fecha=today - timedelta(days=45),
        hora="19:30",
        tipo="comunhao",
        asistentes_count=7,
        visitantes_count=0,
        novos_crentes_count=0,
        notas="Noche de comunión y santa cena. Muy edificante para todos.",
        observaciones=None,
    )
    r_norte_4 = models.Reunion(
        grupo_id=grupo_norte.id,
        fecha=today - timedelta(days=14),
        hora="19:30",
        tipo="periodica",
        asistentes_count=5,
        visitantes_count=1,
        novos_crentes_count=1,
        notas="Estudio de Hechos 2. Un visitante tomó decisión de fe esta noche.",
        observaciones=None,
    )
    # Grupo Sur: 3 reuniones (2 periodica, 1 evangelistica)
    r_sur_1 = models.Reunion(
        grupo_id=grupo_sur.id,
        fecha=today - timedelta(days=90),
        hora="20:00",
        tipo="periodica",
        asistentes_count=4,
        visitantes_count=0,
        novos_crentes_count=0,
        notas="Primera reunión del grupo Sur. Buena dinámica.",
        observaciones=None,
    )
    r_sur_2 = models.Reunion(
        grupo_id=grupo_sur.id,
        fecha=today - timedelta(days=60),
        hora="20:00",
        tipo="evangelistica",
        asistentes_count=5,
        visitantes_count=3,
        novos_crentes_count=1,
        notas="Noche de evangelismo. Vecinos invitados. Una persona aceptó al Señor.",
        observaciones=None,
    )
    r_sur_3 = models.Reunion(
        grupo_id=grupo_sur.id,
        fecha=today - timedelta(days=21),
        hora="20:00",
        tipo="periodica",
        asistentes_count=5,
        visitantes_count=1,
        novos_crentes_count=0,
        notas="Estudio sobre el Espíritu Santo. Tiempo de oración muy especial.",
        observaciones=None,
    )
    # Grupo Este: 3 reuniones (todas periodica)
    r_este_1 = models.Reunion(
        grupo_id=grupo_este.id,
        fecha=today - timedelta(days=75),
        hora="19:00",
        tipo="periodica",
        asistentes_count=4,
        visitantes_count=0,
        novos_crentes_count=0,
        notas="Estudio del Sermón del Monte. Buena participación.",
        observaciones=None,
    )
    r_este_2 = models.Reunion(
        grupo_id=grupo_este.id,
        fecha=today - timedelta(days=45),
        hora="19:00",
        tipo="periodica",
        asistentes_count=5,
        visitantes_count=1,
        novos_crentes_count=0,
        notas="Estudio sobre identidad en Cristo. Cristina compartió su testimonio.",
        observaciones=None,
    )
    r_este_3 = models.Reunion(
        grupo_id=grupo_este.id,
        fecha=today - timedelta(days=7),
        hora="19:00",
        tipo="periodica",
        asistentes_count=4,
        visitantes_count=2,
        novos_crentes_count=0,
        notas="Oración por Valencia y las misiones locales.",
        observaciones=None,
    )
    # Grupo Oeste: 1 reunion periodica
    r_oeste_1 = models.Reunion(
        grupo_id=grupo_oeste.id,
        fecha=today - timedelta(days=30),
        hora="18:30",
        tipo="periodica",
        asistentes_count=3,
        visitantes_count=0,
        novos_crentes_count=0,
        notas="Reunión mensual con familias. Se oró por los hijos del grupo.",
        observaciones=None,
    )
    # Grupo Centro: 1 reunion comunhao
    r_centro_1 = models.Reunion(
        grupo_id=grupo_centro.id,
        fecha=today - timedelta(days=30),
        hora="11:00",
        tipo="comunhao",
        asistentes_count=5,
        visitantes_count=0,
        novos_crentes_count=0,
        notas="Desayuno compartido y tiempo de adoración. Gran unidad en el grupo.",
        observaciones=None,
    )

    reuniones_objs = [
        r_norte_1, r_norte_2, r_norte_3, r_norte_4,
        r_sur_1, r_sur_2, r_sur_3,
        r_este_1, r_este_2, r_este_3,
        r_oeste_1,
        r_centro_1,
    ]
    for r in reuniones_objs:
        db.add(r)
    db.flush()
    for r in reuniones_objs:
        db.refresh(r)

    # ── IntegranteReunion (asistencia ~75%) ──────────────────────────────────
    # Mapping grupo -> members list
    grupo_members_map = {
        grupo_norte.id: [carlos, miguel, roberto, ana, elena, david, carmen],
        grupo_sur.id:   [lucia, alejandro, isabel, patricia, sergio],
        grupo_este.id:  [elena, laura, joaquin, cristina, alberto],
        grupo_oeste.id: [francisco, natalia, sofia, david],
        grupo_centro.id:[manuel, carmen, alberto, natalia, cristina],
    }

    # Attendance patterns: True=presente, False=ausente, per member per reunion
    # We'll define explicit patterns for realism
    norte_members = [carlos, miguel, roberto, ana, elena, david, carmen]
    sur_members   = [lucia, alejandro, isabel, patricia, sergio]
    este_members  = [elena, laura, joaquin, cristina, alberto]
    oeste_members = [francisco, natalia, sofia, david]
    centro_members= [manuel, carmen, alberto, natalia, cristina]

    def add_asistencia(reunion, members, absent_indices):
        """Add attendance records; absent_indices are 0-based positions in members to mark absent."""
        for idx, member in enumerate(members):
            presente = idx not in absent_indices
            db.add(models.IntegranteReunion(
                integrante_id=member.id,
                reunion_id=reunion.id,
                presente=presente,
            ))

    # Norte reunions
    add_asistencia(r_norte_1, norte_members, [3, 6])          # ana, carmen absent
    add_asistencia(r_norte_2, norte_members, [4])             # elena absent
    add_asistencia(r_norte_3, norte_members, [3, 5])          # ana, david absent
    add_asistencia(r_norte_4, norte_members, [2, 6])          # roberto, carmen absent
    # Sur reunions
    add_asistencia(r_sur_1,   sur_members,   [2])             # isabel absent
    add_asistencia(r_sur_2,   sur_members,   [])              # all present
    add_asistencia(r_sur_3,   sur_members,   [3])             # patricia absent
    # Este reunions
    add_asistencia(r_este_1,  este_members,  [1])             # laura absent
    add_asistencia(r_este_2,  este_members,  [])              # all present
    add_asistencia(r_este_3,  este_members,  [2, 4])          # joaquin, alberto absent
    # Oeste reunion
    add_asistencia(r_oeste_1, oeste_members, [3])             # david absent
    # Centro reunion
    add_asistencia(r_centro_1,centro_members,[1])             # carmen absent

    db.flush()

    # ── OracaoReunion ────────────────────────────────────────────────────────
    oraciones_reunion_data = [
        # (reunion, texto, respondida, days_respondida_ago)
        (r_norte_1, "Sanidad para la madre de Carlos, que tiene una operación pendiente.", False, None),
        (r_norte_1, "Dirección de Dios para los jóvenes del grupo en sus decisiones de vida.", False, None),
        (r_norte_2, "Trabajo estable para Ana, que lleva semanas buscando empleo.", True, 60),
        (r_norte_2, "Restauración del matrimonio de una familia del barrio.", False, None),
        (r_norte_3, "Salvación de los familiares no creyentes de los miembros del grupo.", False, None),
        (r_norte_4, "El visitante que tomó decisión esta noche sea discipulado bien.", False, None),
        (r_norte_4, "Apertura de nuevos grupos en el barrio norte.", False, None),
        (r_sur_1,   "Crecimiento del grupo Sur en número y en profundidad espiritual.", False, None),
        (r_sur_2,   "Seguimiento de la persona que aceptó a Cristo esta noche.", False, None),
        (r_sur_2,   "Provisión económica para una familia del grupo que atraviesa dificultades.", True, 30),
        (r_sur_3,   "Unidad del grupo frente a tensiones recientes.", False, None),
        (r_este_1,  "Sabiduría para Elena en su liderazgo del grupo.", False, None),
        (r_este_2,  "Liberación espiritual para un familiar de Cristina.", False, None),
        (r_este_3,  "Apertura del corazón de los vecinos que visitaron el grupo.", False, None),
        (r_oeste_1, "Los hijos de las familias del grupo crezcan en fe.", False, None),
        (r_centro_1,"Que el grupo Centro se multiplique y plante un nuevo grupo.", False, None),
        (r_centro_1,"Gratitud a Dios por la unidad y el amor que hay en el grupo.", True, 0),
    ]

    for reunion, texto, respondida, days_resp in oraciones_reunion_data:
        fecha_respondida = (today - timedelta(days=days_resp)) if respondida and days_resp is not None else (today if respondida else None)
        db.add(models.OracaoReunion(
            reunion_id=reunion.id,
            texto=texto,
            respondida=respondida,
            fecha_respondida=fecha_respondida,
        ))

    db.flush()

    # ── Testimonios ──────────────────────────────────────────────────────────
    db.add(models.Testimonio(
        titulo="Restauración de mi matrimonio",
        contenido=(
            "Hace dos años mi matrimonio estaba al borde del divorcio. Habíamos perdido la comunicación, "
            "la confianza y el amor que un día nos unió. Llegué al grupo Norte roto por dentro, sin esperanza. "
            "Carlos y el equipo comenzaron a orar por nosotros semana tras semana. Mi esposa empezó a asistir "
            "también, primero con desconfianza, pero poco a poco Dios fue ablandando su corazón y el mío. "
            "Hoy, ocho meses después, puedo decir que tenemos un matrimonio nuevo. No perfecto, pero lleno del "
            "amor de Cristo. Esto no lo hicimos nosotros — lo hizo Dios a través de esta familia del grupo."
        ),
        integrante_id=david.id,
        grupo_id=grupo_norte.id,
        reunion_id=r_norte_3.id,
        fecha=today - timedelta(days=40),
        destacado=True,
    ))

    db.add(models.Testimonio(
        titulo="Sanidad de enfermedad crónica",
        contenido=(
            "Desde los 25 años convivo con una enfermedad autoinmune que los médicos decían que no tenía cura. "
            "Pasé años con dolor, fatiga y desánimo. En una reunión del grupo Sur, durante el tiempo de oración, "
            "sentí algo que nunca antes había experimentado: una paz absoluta y una sensación de calor en mi cuerpo. "
            "En mi próxima revisión médica, el doctor no podía explicar los resultados. Los marcadores inflamatorios "
            "habían bajado drásticamente. Hoy llevo seis meses sin síntomas. Dios es fiel y su poder no tiene límites."
        ),
        integrante_id=isabel.id,
        grupo_id=grupo_sur.id,
        reunion_id=r_sur_2.id,
        fecha=today - timedelta(days=55),
        destacado=True,
    ))

    db.add(models.Testimonio(
        titulo="Provisión económica sobrenatural",
        contenido=(
            "Mi empresa cerró de repente y me quedé sin trabajo ni ahorros suficientes para cubrir el mes. "
            "El grupo Este oró por mí con fe. A los tres días recibí una llamada de una empresa que había "
            "descartado semanas antes — habían revisado mi candidatura y querían contratarme de inmediato. "
            "El salario era exactamente lo que necesitaba para cubrir todas mis deudas. Dios provee cuando "
            "confiamos plenamente en Él."
        ),
        integrante_id=joaquin.id,
        grupo_id=grupo_este.id,
        reunion_id=r_este_2.id,
        fecha=today - timedelta(days=38),
        destacado=False,
    ))

    db.add(models.Testimonio(
        titulo="Liberación de adicciones",
        contenido=(
            "Durante diez años fui esclavo del alcohol. Lo intenté dejar muchas veces solo y siempre fracasé. "
            "Cuando llegué al grupo Norte no creía en nada, venía solo acompañando a un amigo. Pero el amor "
            "genuino de estas personas me llegó al alma. Carlos me acompañó en el proceso durante meses, "
            "orando conmigo cada semana. Hoy llevo dieciocho meses sobrio, tengo trabajo y mi familia está "
            "reunida de nuevo. Solo Cristo puede hacer esto."
        ),
        integrante_id=roberto.id,
        grupo_id=grupo_norte.id,
        reunion_id=r_norte_2.id,
        fecha=today - timedelta(days=75),
        destacado=True,
    ))

    db.add(models.Testimonio(
        titulo="Salvación de mi hijo",
        contenido=(
            "Oré durante cuatro años por la salvación de mi hijo mayor. Se había alejado de Dios, de la familia "
            "y caído en malos caminos. El grupo Centro nunca dejó de creer conmigo. En Navidad, sin que nadie "
            "lo esperara, mi hijo llegó a casa pidiendo perdón y queriendo hablar sobre Dios. Esta semana lo "
            "bautizamos. Lo que para los hombres era imposible, Dios lo hizo realidad."
        ),
        integrante_id=manuel.id,
        grupo_id=grupo_centro.id,
        reunion_id=r_centro_1.id,
        fecha=today - timedelta(days=15),
        destacado=False,
    ))

    db.flush()

    # ── Servicios ────────────────────────────────────────────────────────────
    # Next Sunday
    days_to_sunday = (6 - today.weekday()) % 7
    if days_to_sunday == 0:
        days_to_sunday = 7
    next_sunday = today + timedelta(days=days_to_sunday)
    second_sunday = next_sunday + timedelta(days=7)

    servicio_hall = models.Servicio(
        titulo="Voluntario Hall de Bienvenida",
        fecha=datetime.combine(next_sunday, datetime.min.time().replace(hour=10, minute=30)),
        descripcion="Recibir y acoger a los asistentes al culto dominical. Dar información a los nuevos visitantes.",
    )
    servicio_ninos = models.Servicio(
        titulo="Voluntario Cuidado de Niños",
        fecha=datetime.combine(next_sunday, datetime.min.time().replace(hour=11)),
        descripcion="Cuidado y enseñanza bíblica para niños de 3 a 12 años durante el culto dominical.",
    )
    servicio_sonido = models.Servicio(
        titulo="Voluntario Equipo de Sonido",
        fecha=datetime.combine(second_sunday, datetime.min.time().replace(hour=9, minute=30)),
        descripcion="Montaje, operación y desmontaje del equipo de sonido para el culto dominical.",
    )
    db.add(servicio_hall)
    db.add(servicio_ninos)
    db.add(servicio_sonido)
    db.flush()
    for s in [servicio_hall, servicio_ninos, servicio_sonido]:
        db.refresh(s)

    # Asignaciones de servicios
    for integrante_obj in [carlos, lucia, ana, roberto]:
        db.add(models.ServicioIntegrante(servicio_id=servicio_hall.id, integrante_id=integrante_obj.id))
    for integrante_obj in [carmen, sofia, natalia]:
        db.add(models.ServicioIntegrante(servicio_id=servicio_ninos.id, integrante_id=integrante_obj.id))
    for integrante_obj in [david, miguel, alejandro, sergio]:
        db.add(models.ServicioIntegrante(servicio_id=servicio_sonido.id, integrante_id=integrante_obj.id))

    db.flush()

    # ── Oraciones personales ─────────────────────────────────────────────────
    oraciones_personales = [
        (
            "Sanidad para mi madre",
            "Mi madre tiene una operación de columna la próxima semana. Pido oración por su recuperación completa y por la sabiduría de los médicos.",
            carlos, None, today - timedelta(days=8), False,
        ),
        (
            "Decisión sobre trabajo en otra ciudad",
            "Me ofrecieron un trabajo importante en Madrid. Necesito discernimiento de Dios — no quiero moverme si no es Su voluntad para mi vida aquí en Valencia.",
            miguel, None, today - timedelta(days=12), False,
        ),
        (
            "Restauración de relación familiar",
            "Llevaba tres años sin hablar con mi hermana por una ofensa del pasado. Pedí perdón esta semana y ella lo aceptó. ¡Dios restauró lo que parecía roto para siempre!",
            elena, grupo_este.id, today - timedelta(days=20), True,
        ),
        (
            "Mi hijo se alejó de la fe",
            "Mi hijo de 19 años dejó de ir a la iglesia y parece perdido espiritualmente. Pido oración para que Dios lo alcance de manera sobrenatural.",
            isabel, None, today - timedelta(days=5), False,
        ),
        (
            "Apertura de nuevas puertas ministeriales",
            "Siento que Dios me está llamando a algo más en el ministerio pero no tengo claridad. Pido oración para que Él abra las puertas correctas en el momento correcto.",
            francisco, grupo_oeste.id, today - timedelta(days=3), False,
        ),
    ]

    for titulo, descripcion, integrante_obj, grupo_obj_or_id, fecha_d, respondida in oraciones_personales:
        grupo_id_val = grupo_obj_or_id if isinstance(grupo_obj_or_id, int) or grupo_obj_or_id is None else grupo_obj_or_id
        db.add(models.Oracion(
            titulo=titulo,
            descripcion=descripcion,
            integrante_id=integrante_obj.id,
            grupo_id=grupo_id_val,
            fecha=fecha_d,
            respondida=respondida,
        ))

    db.commit()

    print("Database seeded successfully!")
    print("Credentials:")
    print("  Admin:       admin@puntodeencuentro.es   / admin1234")
    print("  Supervisor:  carlos.mendez@ccln.es       / super1234")
    print("  Responsable: lucia.torres@ccln.es        / resp1234")
    print("  Ayudante:    miguel.santos@ccln.es       / ayud1234")
