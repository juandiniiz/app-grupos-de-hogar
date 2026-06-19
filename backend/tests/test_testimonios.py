def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_list_testimonios(client, admin_token, seed_data):
    res = client.get("/api/testimonios", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 2
    titulos = [t["titulo"] for t in body]
    assert "Sanidad milagrosa" in titulos
    assert "Provision economica" in titulos


def test_filter_destacado(client, admin_token, seed_data):
    res = client.get("/api/testimonios?destacado=true", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(t["destacado"] is True for t in body)
    assert any(t["titulo"] == "Sanidad milagrosa" for t in body)


def test_filter_by_grupo_id(client, admin_token, seed_data):
    g1_id = seed_data["g1_id"]
    res = client.get(f"/api/testimonios?grupo_id={g1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert all(t["grupo_id"] == g1_id for t in body)
    assert any(t["titulo"] == "Sanidad milagrosa" for t in body)


def test_get_testimonio(client, admin_token, seed_data):
    test1_id = seed_data["test1_id"]
    res = client.get(f"/api/testimonios/{test1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert body["titulo"] == "Sanidad milagrosa"
    assert body["integrante_nombre"] is not None
    assert body["grupo_nombre"] is not None


def test_create_testimonio(client, admin_token, seed_data):
    g1_id = seed_data["g1_id"]
    res = client.post(
        "/api/testimonios",
        json={
            "titulo": "Nuevo testimonio",
            "contenido": "Dios hizo un milagro grande en nuestra familia esta semana.",
            "grupo_id": g1_id,
            "fecha": "2026-03-01",
            "destacado": False,
        },
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["titulo"] == "Nuevo testimonio"
    assert body["grupo_id"] == g1_id


def test_update_testimonio_destacado(client, admin_token, seed_data):
    test2_id = seed_data["test2_id"]
    res = client.put(
        f"/api/testimonios/{test2_id}",
        json={
            "titulo": "Provision economica",
            "contenido": "En el momento mas dificil, Dios proveyó de manera sobrenatural.",
            "fecha": "2026-02-01",
            "destacado": True,
        },
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["destacado"] is True


def test_delete_testimonio(client, admin_token, db, seed_data):
    import models
    from datetime import date
    fresh_t = models.Testimonio(
        titulo="Delete Me",
        contenido="Este testimonio sera eliminado del sistema.",
        fecha=date(2026, 5, 1),
    )
    db.add(fresh_t)
    db.commit()
    fresh_id = fresh_t.id

    res = client.delete(f"/api/testimonios/{fresh_id}", headers=auth(admin_token))
    assert res.status_code == 204

    db.expire_all()
    deleted = db.query(models.Testimonio).filter(models.Testimonio.id == fresh_id).first()
    assert deleted is None
