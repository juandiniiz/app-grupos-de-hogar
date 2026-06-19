import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import models
import auth as auth_utils
from datetime import date, datetime

TEST_DATABASE_URL = "sqlite:///./test_app_igreja.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db():
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def seed_data(db):
    """Create base test data. Returns dict of IDs (not ORM objects) to avoid DetachedInstanceError."""
    # Users
    admin = models.User(
        email="admin@test.com",
        password_hash=auth_utils.get_password_hash("admin1234"),
        nombre="Admin Test",
        rol="admin",
    )
    supervisor = models.User(
        email="supervisor@test.com",
        password_hash=auth_utils.get_password_hash("super1234"),
        nombre="Supervisor Test",
        rol="supervisor",
    )
    responsable_user = models.User(
        email="responsable@test.com",
        password_hash=auth_utils.get_password_hash("resp1234"),
        nombre="Responsable Test",
        rol="responsable",
    )
    db.add_all([admin, supervisor, responsable_user])
    db.flush()

    # Integrantes
    i1 = models.Integrante(
        nombre="Juan",
        apellidos="Garcia",
        email="juan@test.com",
        telefono="600111222",
        fecha_nacimiento=date(1990, 5, 15),
        is_membro=True,
        bautizado=True,
        discipulado_inicial="terminado",
        pre_batismo="cursando",
        endereco="Calle Mayor 1",
        latitude=39.47,
        longitude=-0.38,
    )
    i2 = models.Integrante(
        nombre="Maria",
        apellidos="Lopez",
        email="maria@test.com",
        telefono="600333444",
        novo_crente=True,
        is_membro=False,
        discipulado_inicial="no_iniciado",
    )
    i3 = models.Integrante(
        nombre="Pedro",
        apellidos="Martinez",
        email="pedro@test.com",
        is_membro=True,
        bautizado=True,
        iglesia_procedente=True,
        iglesia_procedente_nome="Iglesia Anterior",
        latitude=39.48,
        longitude=-0.37,
    )
    i4 = models.Integrante(
        nombre="Ana",
        apellidos="Fernandez",
        email="ana@test.com",
        novo_batizado=True,
        is_membro=True,
    )
    db.add_all([i1, i2, i3, i4])
    db.flush()

    supervisor.integrante_id = i1.id
    responsable_user.integrante_id = i2.id
    db.flush()

    # Grupos
    g1 = models.Grupo(
        nombre="Grupo Norte",
        responsable_id=i1.id,
        supervisor_id=i3.id,
        dia_semana="lunes",
        hora="19:00",
        frecuencia="semanal",
        endereco="Calle Norte 5",
        latitude=39.47,
        longitude=-0.38,
    )
    g2 = models.Grupo(
        nombre="Grupo Sur",
        responsable_id=i2.id,
        dia_semana="miercoles",
        hora="20:00",
        frecuencia="quincenal",
        latitude=39.46,
        longitude=-0.39,
    )
    db.add_all([g1, g2])
    db.flush()

    db.add_all([
        models.GrupoIntegrante(grupo_id=g1.id, integrante_id=i1.id, rol_en_grupo="responsable"),
        models.GrupoIntegrante(grupo_id=g1.id, integrante_id=i2.id, rol_en_grupo="member"),
        models.GrupoIntegrante(grupo_id=g1.id, integrante_id=i3.id, rol_en_grupo="supervisor"),
        models.GrupoIntegrante(grupo_id=g2.id, integrante_id=i2.id, rol_en_grupo="responsable"),
        models.GrupoIntegrante(grupo_id=g2.id, integrante_id=i4.id, rol_en_grupo="member"),
    ])
    db.flush()

    # Ministerio
    m1 = models.Ministerio(nombre="Alabanza", descripcion="Ministerio de musica")
    db.add(m1)
    db.flush()
    db.add(models.MinisterioIntegrante(ministerio_id=m1.id, integrante_id=i1.id, es_responsable=True))
    db.add(models.MinisterioIntegrante(ministerio_id=m1.id, integrante_id=i3.id, es_responsable=False))
    db.flush()

    t1 = models.MinisterioTarefa(ministerio_id=m1.id, nombre="Tocar guitarra")
    db.add(t1)
    db.flush()
    db.add(models.MinisterioTarefaIntegrante(tarefa_id=t1.id, integrante_id=i1.id))
    db.flush()

    # Reuniones
    r1 = models.Reunion(
        grupo_id=g1.id,
        fecha=date(2026, 1, 15),
        tipo="periodica",
        asistentes_count=3,
        visitantes_count=1,
        novos_crentes_count=0,
    )
    r2 = models.Reunion(
        grupo_id=g1.id,
        fecha=date(2026, 2, 10),
        tipo="comunhao",
        asistentes_count=4,
        visitantes_count=2,
        novos_crentes_count=1,
    )
    db.add_all([r1, r2])
    db.flush()

    db.add_all([
        models.IntegranteReunion(integrante_id=i1.id, reunion_id=r1.id, presente=True),
        models.IntegranteReunion(integrante_id=i2.id, reunion_id=r1.id, presente=False),
        models.IntegranteReunion(integrante_id=i1.id, reunion_id=r2.id, presente=True),
        models.IntegranteReunion(integrante_id=i2.id, reunion_id=r2.id, presente=True),
    ])

    o1 = models.OracaoReunion(reunion_id=r1.id, texto="Por la familia Garcia", respondida=False)
    o2 = models.OracaoReunion(
        reunion_id=r1.id,
        texto="Por sanidad de Maria",
        respondida=True,
        fecha_respondida=date(2026, 1, 20),
    )
    db.add_all([o1, o2])
    db.flush()

    test1 = models.Testimonio(
        titulo="Sanidad milagrosa",
        contenido="Dios sano completamente mi enfermedad despues de orar en el grupo.",
        integrante_id=i1.id,
        grupo_id=g1.id,
        fecha=date(2026, 1, 15),
        destacado=True,
    )
    test2 = models.Testimonio(
        titulo="Provision economica",
        contenido="En el momento mas dificil, Dios proveyó de manera sobrenatural.",
        grupo_id=g2.id,
        fecha=date(2026, 2, 1),
        destacado=False,
    )
    db.add_all([test1, test2])
    db.flush()

    s1 = models.Servicio(titulo="Voluntario Hall", fecha=datetime(2026, 3, 1), descripcion="Servicio en la entrada")
    db.add(s1)
    db.flush()
    db.add(models.ServicioIntegrante(servicio_id=s1.id, integrante_id=i1.id))

    op1 = models.Oracion(
        titulo="Por mi familia",
        descripcion="Que Dios guarde a mi familia",
        integrante_id=i1.id,
        fecha=date(2026, 1, 1),
    )
    db.add(op1)

    db.commit()

    # Return only IDs to avoid DetachedInstanceError
    return {
        "admin_id": admin.id,
        "supervisor_id": supervisor.id,
        "responsable_id": responsable_user.id,
        "i1_id": i1.id,
        "i2_id": i2.id,
        "i3_id": i3.id,
        "i4_id": i4.id,
        "g1_id": g1.id,
        "g2_id": g2.id,
        "m1_id": m1.id,
        "t1_id": t1.id,
        "r1_id": r1.id,
        "r2_id": r2.id,
        "o1_id": o1.id,
        "o2_id": o2.id,
        "test1_id": test1.id,
        "test2_id": test2.id,
        "s1_id": s1.id,
    }


@pytest.fixture(scope="session")
def admin_token(client, seed_data):
    res = client.post("/api/auth/login", data={"username": "admin@test.com", "password": "admin1234"})
    assert res.status_code == 200
    return res.json()["access_token"]


@pytest.fixture(scope="session")
def supervisor_token(client, seed_data):
    res = client.post("/api/auth/login", data={"username": "supervisor@test.com", "password": "super1234"})
    assert res.status_code == 200
    return res.json()["access_token"]


@pytest.fixture(scope="session")
def responsable_token(client, seed_data):
    res = client.post("/api/auth/login", data={"username": "responsable@test.com", "password": "resp1234"})
    assert res.status_code == 200
    return res.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}
