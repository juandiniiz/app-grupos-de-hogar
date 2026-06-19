from datetime import datetime


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_list_servicios(client, admin_token, seed_data):
    res = client.get("/api/servicios", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    assert any(s["titulo"] == "Voluntario Hall" for s in body)


def test_list_servicios_no_auth(client):
    res = client.get("/api/servicios")
    assert res.status_code == 401


def test_filter_servicios_by_integrante(client, admin_token, seed_data):
    i1_id = seed_data["i1_id"]
    res = client.get(f"/api/servicios?integrante_id={i1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert len(body) >= 1
    assert any(s["titulo"] == "Voluntario Hall" for s in body)


def test_get_servicio(client, admin_token, seed_data):
    s1_id = seed_data["s1_id"]
    res = client.get(f"/api/servicios/{s1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert body["titulo"] == "Voluntario Hall"
    assert body["descripcion"] == "Servicio en la entrada"


def test_get_servicio_not_found(client, admin_token):
    res = client.get("/api/servicios/99999", headers=auth(admin_token))
    assert res.status_code == 404


def test_create_servicio(client, admin_token):
    res = client.post(
        "/api/servicios",
        json={"titulo": "Servicio de Limpieza", "fecha": "2026-04-15T09:00:00", "descripcion": "Limpieza del templo"},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["titulo"] == "Servicio de Limpieza"
    assert body["id"] is not None


def test_update_servicio(client, admin_token, seed_data):
    s1_id = seed_data["s1_id"]
    res = client.put(
        f"/api/servicios/{s1_id}",
        json={"titulo": "Voluntario Hall Actualizado", "fecha": "2026-03-01T10:00:00"},
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["titulo"] == "Voluntario Hall Actualizado"


def test_delete_servicio(client, admin_token, db):
    import models
    fresh_s = models.Servicio(titulo="Servicio Temp", fecha=datetime(2026, 6, 1))
    db.add(fresh_s)
    db.commit()
    fresh_id = fresh_s.id

    res = client.delete(f"/api/servicios/{fresh_id}", headers=auth(admin_token))
    assert res.status_code == 204

    db.expire_all()
    deleted = db.query(models.Servicio).filter(models.Servicio.id == fresh_id).first()
    assert deleted is None


def test_add_integrante_to_servicio(client, admin_token, seed_data, db):
    import models
    fresh_i = models.Integrante(nombre="ServicioWorker", apellidos="Test")
    fresh_s = models.Servicio(titulo="Test Servicio Add", fecha=datetime(2026, 7, 1, 8, 0))
    db.add_all([fresh_i, fresh_s])
    db.commit()
    fresh_i_id = fresh_i.id
    fresh_s_id = fresh_s.id

    res = client.post(
        f"/api/servicios/{fresh_s_id}/integrantes",
        json={"integrante_id": fresh_i_id},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    assert res.json()["ok"] is True


def test_remove_integrante_from_servicio(client, admin_token, db):
    import models
    fresh_i = models.Integrante(nombre="ServicioRemove", apellidos="Test")
    fresh_s = models.Servicio(titulo="Test Servicio Remove", fecha=datetime(2026, 7, 2, 8, 0))
    db.add_all([fresh_i, fresh_s])
    db.flush()
    si = models.ServicioIntegrante(servicio_id=fresh_s.id, integrante_id=fresh_i.id)
    db.add(si)
    db.commit()
    fresh_i_id = fresh_i.id
    fresh_s_id = fresh_s.id

    res = client.delete(
        f"/api/servicios/{fresh_s_id}/integrantes/{fresh_i_id}",
        headers=auth(admin_token),
    )
    assert res.status_code == 204
