from datetime import date


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_list_reuniones(client, admin_token, seed_data):
    res = client.get("/api/reuniones", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 2


def test_list_reuniones_filter_by_grupo(client, admin_token, seed_data):
    g1_id = seed_data["g1_id"]
    res = client.get(f"/api/reuniones?grupo_id={g1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(r["grupo_id"] == g1_id for r in body)
    assert len(body) >= 2


def test_get_reunion_detail(client, admin_token, seed_data):
    r1_id = seed_data["r1_id"]
    g1_id = seed_data["g1_id"]
    res = client.get(f"/api/reuniones/{r1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert body["tipo"] == "periodica"
    assert body["grupo_id"] == g1_id


def test_get_reunion_includes_asistencia(client, admin_token, seed_data):
    r1_id = seed_data["r1_id"]
    res = client.get(f"/api/reuniones/{r1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert "asistencia" in body
    assert isinstance(body["asistencia"], list)
    assert len(body["asistencia"]) >= 2


def test_get_reunion_includes_oraciones(client, admin_token, seed_data):
    r1_id = seed_data["r1_id"]
    res = client.get(f"/api/reuniones/{r1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert "oraciones" in body
    assert len(body["oraciones"]) >= 2


def test_create_reunion_auto_creates_asistencia(client, admin_token, seed_data):
    g1_id = seed_data["g1_id"]
    res = client.post(
        "/api/reuniones",
        json={"grupo_id": g1_id, "fecha": "2026-04-01", "tipo": "evangelistica"},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["tipo"] == "evangelistica"
    assert body["grupo_id"] == g1_id

    r_id = body["id"]
    detail = client.get(f"/api/reuniones/{r_id}", headers=auth(admin_token))
    assert detail.status_code == 200
    assert len(detail.json()["asistencia"]) >= 1


def test_update_reunion(client, admin_token, seed_data):
    r2_id = seed_data["r2_id"]
    res = client.put(
        f"/api/reuniones/{r2_id}",
        json={"notas": "Reunion especial de comunhao", "visitantes_count": 5},
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["notas"] == "Reunion especial de comunhao"
    assert body["visitantes_count"] == 5


def test_delete_reunion(client, admin_token, db, seed_data):
    import models
    g1_id = seed_data["g1_id"]
    temp = models.Reunion(grupo_id=g1_id, fecha=date(2026, 12, 31), tipo="periodica")
    db.add(temp)
    db.commit()
    temp_id = temp.id

    res = client.delete(f"/api/reuniones/{temp_id}", headers=auth(admin_token))
    assert res.status_code == 204

    db.expire_all()
    deleted = db.query(models.Reunion).filter(models.Reunion.id == temp_id).first()
    assert deleted is None


def test_update_asistencia_bulk(client, admin_token, seed_data):
    r1_id = seed_data["r1_id"]
    i1_id = seed_data["i1_id"]
    i2_id = seed_data["i2_id"]

    res = client.post(
        f"/api/reuniones/{r1_id}/asistencia",
        json=[
            {"integrante_id": i1_id, "presente": True},
            {"integrante_id": i2_id, "presente": True},
        ],
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_update_asistencia_updates_count(client, admin_token, seed_data):
    r1_id = seed_data["r1_id"]
    i1_id = seed_data["i1_id"]
    i2_id = seed_data["i2_id"]

    client.post(
        f"/api/reuniones/{r1_id}/asistencia",
        json=[
            {"integrante_id": i1_id, "presente": True},
            {"integrante_id": i2_id, "presente": True},
        ],
        headers=auth(admin_token),
    )

    res = client.get(f"/api/reuniones/{r1_id}", headers=auth(admin_token))
    body = res.json()
    assert body["asistentes_count"] >= 2


def test_add_oracao_to_reunion(client, admin_token, seed_data):
    r2_id = seed_data["r2_id"]
    res = client.post(
        f"/api/reuniones/{r2_id}/oraciones",
        json={"texto": "Oracion por los enfermos", "respondida": False},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["texto"] == "Oracion por los enfermos"
    assert body["reunion_id"] == r2_id


def test_update_oracao(client, admin_token, seed_data):
    r1_id = seed_data["r1_id"]
    o1_id = seed_data["o1_id"]

    res = client.put(
        f"/api/reuniones/{r1_id}/oraciones/{o1_id}",
        json={"texto": "Por la familia Garcia actualizado", "respondida": True},
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["respondida"] is True


def test_delete_oracao(client, admin_token, seed_data, db):
    import models
    r2_id = seed_data["r2_id"]
    fresh_o = models.OracaoReunion(reunion_id=r2_id, texto="Temporal a eliminar", respondida=False)
    db.add(fresh_o)
    db.commit()
    fresh_o_id = fresh_o.id

    res = client.delete(
        f"/api/reuniones/{r2_id}/oraciones/{fresh_o_id}",
        headers=auth(admin_token),
    )
    assert res.status_code == 204
