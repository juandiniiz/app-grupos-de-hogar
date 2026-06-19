from datetime import date


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_list_oraciones(client, admin_token, seed_data):
    res = client.get("/api/oraciones", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 1


def test_list_oraciones_no_auth(client):
    res = client.get("/api/oraciones")
    assert res.status_code == 401


def test_filter_oraciones_by_integrante(client, admin_token, seed_data):
    i1_id = seed_data["i1_id"]
    res = client.get(f"/api/oraciones?integrante_id={i1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert len(body) >= 1
    assert any(o["titulo"] == "Por mi familia" for o in body)


def test_filter_oraciones_respondida(client, admin_token, seed_data):
    res = client.get("/api/oraciones?respondida=false", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(o["respondida"] is False for o in body)


def test_create_oracion(client, admin_token, seed_data):
    i1_id = seed_data["i1_id"]
    res = client.post(
        "/api/oraciones",
        json={
            "titulo": "Oracion por sanidad",
            "descripcion": "Por sanidad completa",
            "integrante_id": i1_id,
            "fecha": "2026-03-01",
            "respondida": False,
        },
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["titulo"] == "Oracion por sanidad"
    assert body["integrante_id"] == i1_id


def test_update_oracion(client, admin_token, db):
    import models
    fresh_o = models.Oracion(titulo="Update Oracion Test", fecha=date(2026, 1, 10), respondida=False)
    db.add(fresh_o)
    db.commit()
    fresh_id = fresh_o.id

    res = client.put(
        f"/api/oraciones/{fresh_id}",
        json={"titulo": "Update Oracion Test", "fecha": "2026-01-10", "respondida": True},
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["respondida"] is True


def test_delete_oracion(client, admin_token, db):
    import models
    fresh_o = models.Oracion(titulo="Delete Oracion", fecha=date(2026, 2, 1))
    db.add(fresh_o)
    db.commit()
    fresh_id = fresh_o.id

    res = client.delete(f"/api/oraciones/{fresh_id}", headers=auth(admin_token))
    assert res.status_code == 204

    db.expire_all()
    deleted = db.query(models.Oracion).filter(models.Oracion.id == fresh_id).first()
    assert deleted is None


def test_oracion_not_found_update_returns_404(client, admin_token):
    res = client.put(
        "/api/oraciones/99999",
        json={"titulo": "Test", "fecha": "2026-01-01", "respondida": False},
        headers=auth(admin_token),
    )
    assert res.status_code == 404
