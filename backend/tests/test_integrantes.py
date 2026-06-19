def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_list_integrantes_admin_sees_all(client, admin_token, seed_data):
    res = client.get("/api/integrantes", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 4
    nombres = [i["nombre"] for i in body]
    assert "Juan" in nombres
    assert "Maria" in nombres


def test_list_integrantes_no_auth_returns_401(client):
    res = client.get("/api/integrantes")
    assert res.status_code == 401


def test_filter_by_is_membro(client, admin_token, seed_data):
    res = client.get("/api/integrantes?is_membro=true", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(i["is_membro"] for i in body)
    assert len(body) >= 3


def test_filter_by_novo_crente(client, admin_token, seed_data):
    res = client.get("/api/integrantes?novo_crente=true", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(i["novo_crente"] for i in body)
    assert len(body) >= 1
    assert any(i["nombre"] == "Maria" for i in body)


def test_filter_by_bautizado(client, admin_token, seed_data):
    res = client.get("/api/integrantes?bautizado=true", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(i["bautizado"] for i in body)
    assert len(body) >= 2


def test_filter_by_novo_batizado(client, admin_token, seed_data):
    res = client.get("/api/integrantes?novo_batizado=true", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(i["novo_batizado"] for i in body)
    assert any(i["nombre"] == "Ana" for i in body)


def test_filter_by_grupo_id(client, admin_token, seed_data):
    g1_id = seed_data["g1_id"]
    res = client.get(f"/api/integrantes?grupo_id={g1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert len(body) >= 3


def test_filter_sin_grupo(client, admin_token, seed_data):
    res = client.get("/api/integrantes?sin_grupo=true", headers=auth(admin_token))
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_filter_by_discipulado_inicial(client, admin_token, seed_data):
    res = client.get("/api/integrantes?discipulado_inicial=terminado", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(i["discipulado_inicial"] == "terminado" for i in body)
    assert any(i["nombre"] == "Juan" for i in body)


def test_filter_by_pre_batismo(client, admin_token, seed_data):
    res = client.get("/api/integrantes?pre_batismo=cursando", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(i["pre_batismo"] == "cursando" for i in body)


def test_filter_search_by_nombre(client, admin_token, seed_data):
    res = client.get("/api/integrantes?q=Juan", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert len(body) >= 1
    assert any(i["nombre"] == "Juan" for i in body)


def test_filter_by_ministerio_id(client, admin_token, seed_data):
    m1_id = seed_data["m1_id"]
    res = client.get(f"/api/integrantes?ministerio_id={m1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert len(body) >= 2
    nombres = [i["nombre"] for i in body]
    assert "Juan" in nombres
    assert "Pedro" in nombres


def test_get_integrante_by_id(client, admin_token, seed_data):
    i1_id = seed_data["i1_id"]
    res = client.get(f"/api/integrantes/{i1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert body["nombre"] == "Juan"
    assert body["apellidos"] == "Garcia"
    assert body["bautizado"] is True


def test_get_integrante_not_found(client, admin_token):
    res = client.get("/api/integrantes/99999", headers=auth(admin_token))
    assert res.status_code == 404


def test_create_integrante_minimal(client, admin_token, seed_data):
    res = client.post(
        "/api/integrantes",
        json={"nombre": "Carlos", "apellidos": "Ruiz"},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["nombre"] == "Carlos"
    assert body["apellidos"] == "Ruiz"
    assert body["id"] is not None


def test_create_integrante_with_grupo(client, admin_token, seed_data):
    g1_id = seed_data["g1_id"]
    res = client.post(
        "/api/integrantes",
        json={
            "nombre": "Luis",
            "apellidos": "Sanchez",
            "grupos": [{"grupo_id": g1_id, "rol_en_grupo": "member"}],
        },
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["nombre"] == "Luis"
    assert len(body["grupos"]) >= 1
    assert body["grupos"][0]["grupo_id"] == g1_id


def test_create_integrante_with_ministerio(client, admin_token, seed_data):
    m1_id = seed_data["m1_id"]
    res = client.post(
        "/api/integrantes",
        json={
            "nombre": "Rosa",
            "apellidos": "Gonzalez",
            "ministerios": [{"ministerio_id": m1_id, "es_responsable": False}],
        },
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert len(body["ministerios"]) >= 1


def test_update_integrante(client, admin_token, seed_data):
    i4_id = seed_data["i4_id"]
    res = client.put(
        f"/api/integrantes/{i4_id}",
        json={"nombre": "Ana", "apellidos": "Fernandez Updated", "telefono": "699000111"},
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["apellidos"] == "Fernandez Updated"
    assert body["telefono"] == "699000111"


def test_delete_integrante_soft(client, admin_token, db):
    import models
    fresh = models.Integrante(nombre="Temporal", apellidos="Delete")
    db.add(fresh)
    db.commit()
    fresh_id = fresh.id

    res = client.delete(f"/api/integrantes/{fresh_id}", headers=auth(admin_token))
    assert res.status_code == 204

    db.expire_all()
    updated = db.query(models.Integrante).filter(models.Integrante.id == fresh_id).first()
    assert updated.activo is False


def test_delete_integrante_sole_responsable_fails(client, admin_token, db):
    import models
    sole = models.Integrante(nombre="SoleResp", apellidos="Test")
    db.add(sole)
    db.flush()
    fresh_group = models.Grupo(nombre="Solo Group Test", responsable_id=sole.id)
    db.add(fresh_group)
    db.flush()
    gi = models.GrupoIntegrante(grupo_id=fresh_group.id, integrante_id=sole.id, rol_en_grupo="responsable")
    db.add(gi)
    db.commit()
    sole_id = sole.id

    res = client.delete(f"/api/integrantes/{sole_id}", headers=auth(admin_token))
    assert res.status_code == 400
    assert "responsable" in res.json()["detail"].lower()


def test_get_integrante_asistencia(client, admin_token, seed_data):
    i1_id = seed_data["i1_id"]
    res = client.get(f"/api/integrantes/{i1_id}/asistencia", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert "total" in body
    assert "ultimo_mes" in body
    assert "ultimo_ano" in body


def test_integrantes_mapa(client, admin_token, seed_data):
    res = client.get("/api/integrantes/mapa", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 2
    for item in body:
        assert item["latitude"] is not None
        assert item["longitude"] is not None


def test_responsable_sees_only_own_group_integrantes(client, responsable_token, seed_data):
    # responsable is linked to i2 (Maria), who is responsable of g2
    # g2 has Maria (i2) and Ana (i4)
    res = client.get("/api/integrantes", headers=auth(responsable_token))
    assert res.status_code == 200
    body = res.json()
    nombres = [i["nombre"] for i in body]
    assert "Maria" in nombres
    assert "Ana" in nombres
