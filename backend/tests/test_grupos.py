def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_list_grupos(client, admin_token, seed_data):
    res = client.get("/api/grupos", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 2
    nombres = [g["nombre"] for g in body]
    assert "Grupo Norte" in nombres
    assert "Grupo Sur" in nombres


def test_list_grupos_no_auth(client):
    res = client.get("/api/grupos")
    assert res.status_code == 401


def test_filter_grupos_by_frecuencia(client, admin_token, seed_data):
    res = client.get("/api/grupos?frecuencia=semanal", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(g["frecuencia"] == "semanal" for g in body)
    assert any(g["nombre"] == "Grupo Norte" for g in body)


def test_filter_grupos_by_dia_semana(client, admin_token, seed_data):
    res = client.get("/api/grupos?dia_semana=miercoles", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(g["dia_semana"] == "miercoles" for g in body)
    assert any(g["nombre"] == "Grupo Sur" for g in body)


def test_grupos_mapa(client, admin_token, seed_data):
    res = client.get("/api/grupos/mapa", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 2


def test_get_grupo_by_id(client, admin_token, seed_data):
    g1_id = seed_data["g1_id"]
    res = client.get(f"/api/grupos/{g1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert body["nombre"] == "Grupo Norte"
    assert body["frecuencia"] == "semanal"
    assert body["responsable_nombre"] is not None


def test_get_grupo_not_found(client, admin_token):
    res = client.get("/api/grupos/99999", headers=auth(admin_token))
    assert res.status_code == 404


def test_create_grupo(client, admin_token, seed_data):
    res = client.post(
        "/api/grupos",
        json={"nombre": "Grupo Este", "frecuencia": "mensual", "dia_semana": "viernes"},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["nombre"] == "Grupo Este"
    assert body["frecuencia"] == "mensual"


def test_create_grupo_with_integrantes(client, admin_token, seed_data):
    i3_id = seed_data["i3_id"]
    res = client.post(
        "/api/grupos",
        json={
            "nombre": "Grupo Oeste",
            "frecuencia": "semanal",
            "integrantes": [{"integrante_id": i3_id, "rol_en_grupo": "member"}],
        },
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["nombre"] == "Grupo Oeste"
    assert body["integrantes_count"] >= 1


def test_update_grupo(client, admin_token, seed_data):
    g2_id = seed_data["g2_id"]
    res = client.put(
        f"/api/grupos/{g2_id}",
        json={"nombre": "Grupo Sur Actualizado", "frecuencia": "mensual"},
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["nombre"] == "Grupo Sur Actualizado"
    assert body["frecuencia"] == "mensual"


def test_delete_grupo_soft(client, admin_token, db):
    import models
    temp_grupo = models.Grupo(nombre="Grupo Temporal Delete")
    db.add(temp_grupo)
    db.commit()
    temp_id = temp_grupo.id

    res = client.delete(f"/api/grupos/{temp_id}", headers=auth(admin_token))
    assert res.status_code == 204

    db.expire_all()
    updated = db.query(models.Grupo).filter(models.Grupo.id == temp_id).first()
    assert updated.activo is False


def test_get_grupo_integrantes_with_asistencia(client, admin_token, seed_data):
    g1_id = seed_data["g1_id"]
    res = client.get(f"/api/grupos/{g1_id}/integrantes", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 3
    for member in body:
        assert "asistencia_pct" in member
        assert "rol_en_grupo" in member


def test_add_integrante_to_grupo(client, admin_token, db, seed_data):
    import models
    fresh_i = models.Integrante(nombre="AddToGroup", apellidos="Test")
    fresh_g = models.Grupo(nombre="AddTarget Group")
    db.add_all([fresh_i, fresh_g])
    db.commit()
    fresh_i_id = fresh_i.id
    fresh_g_id = fresh_g.id

    res = client.post(
        f"/api/grupos/{fresh_g_id}/integrantes",
        json={"integrante_id": fresh_i_id, "rol_en_grupo": "member"},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    assert res.json()["ok"] is True


def test_add_duplicate_integrante_fails(client, admin_token, seed_data):
    g1_id = seed_data["g1_id"]
    i1_id = seed_data["i1_id"]
    res = client.post(
        f"/api/grupos/{g1_id}/integrantes",
        json={"integrante_id": i1_id, "rol_en_grupo": "member"},
        headers=auth(admin_token),
    )
    assert res.status_code == 400


def test_remove_integrante_from_grupo(client, admin_token, db, seed_data):
    import models
    fresh_i = models.Integrante(nombre="RemoveFromGroup", apellidos="Test")
    fresh_g = models.Grupo(nombre="Remove Group")
    db.add_all([fresh_i, fresh_g])
    db.flush()
    gi = models.GrupoIntegrante(grupo_id=fresh_g.id, integrante_id=fresh_i.id, rol_en_grupo="member")
    db.add(gi)
    db.commit()
    fresh_i_id = fresh_i.id
    fresh_g_id = fresh_g.id

    res = client.delete(
        f"/api/grupos/{fresh_g_id}/integrantes/{fresh_i_id}",
        headers=auth(admin_token),
    )
    assert res.status_code == 204


def test_supervisor_sees_own_grupos(client, supervisor_token, seed_data):
    # supervisor user is linked to i1 (Juan), who is responsable of g1
    res = client.get("/api/grupos", headers=auth(supervisor_token))
    assert res.status_code == 200
    body = res.json()
    nombres = [g["nombre"] for g in body]
    assert "Grupo Norte" in nombres


def test_responsable_sees_own_grupo(client, responsable_token, seed_data):
    # responsable user is linked to i2 (Maria), who is responsable of g2
    res = client.get("/api/grupos", headers=auth(responsable_token))
    assert res.status_code == 200
    body = res.json()
    assert len(body) >= 1
