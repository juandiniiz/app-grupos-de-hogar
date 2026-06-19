def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_list_ministerios(client, admin_token, seed_data):
    res = client.get("/api/ministerios", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    assert any(m["nombre"] == "Alabanza" for m in body)


def test_get_ministerio_by_id(client, admin_token, seed_data):
    m1_id = seed_data["m1_id"]
    res = client.get(f"/api/ministerios/{m1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert body["nombre"] == "Alabanza"
    assert body["descripcion"] == "Ministerio de musica"


def test_create_ministerio(client, admin_token):
    res = client.post(
        "/api/ministerios",
        json={"nombre": "Danza", "descripcion": "Ministerio de danza"},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["nombre"] == "Danza"
    assert body["integrantes_count"] == 0


def test_update_ministerio(client, admin_token, seed_data):
    m1_id = seed_data["m1_id"]
    res = client.put(
        f"/api/ministerios/{m1_id}",
        json={"nombre": "Alabanza Actualizado"},
        headers=auth(admin_token),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["nombre"] == "Alabanza Actualizado"


def test_delete_ministerio(client, admin_token, db):
    import models
    fresh_m = models.Ministerio(nombre="Delete Me")
    db.add(fresh_m)
    db.commit()
    fresh_id = fresh_m.id

    res = client.delete(f"/api/ministerios/{fresh_id}", headers=auth(admin_token))
    assert res.status_code == 204

    db.expire_all()
    deleted = db.query(models.Ministerio).filter(models.Ministerio.id == fresh_id).first()
    assert deleted is None


def test_add_integrante_to_ministerio(client, admin_token, seed_data, db):
    import models
    m1_id = seed_data["m1_id"]
    fresh_i = models.Integrante(nombre="AddToMin", apellidos="Test")
    db.add(fresh_i)
    db.commit()
    fresh_i_id = fresh_i.id

    res = client.post(
        f"/api/ministerios/{m1_id}/integrantes",
        json={"integrante_id": fresh_i_id, "es_responsable": False},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    assert res.json()["ok"] is True


def test_add_duplicate_integrante_fails(client, admin_token, seed_data):
    m1_id = seed_data["m1_id"]
    i1_id = seed_data["i1_id"]
    res = client.post(
        f"/api/ministerios/{m1_id}/integrantes",
        json={"integrante_id": i1_id, "es_responsable": False},
        headers=auth(admin_token),
    )
    assert res.status_code == 400


def test_remove_integrante_from_ministerio(client, admin_token, seed_data, db):
    import models
    m1_id = seed_data["m1_id"]
    fresh_i = models.Integrante(nombre="RemoveFromMin", apellidos="Test")
    db.add(fresh_i)
    db.flush()
    mi = models.MinisterioIntegrante(ministerio_id=m1_id, integrante_id=fresh_i.id, es_responsable=False)
    db.add(mi)
    db.commit()
    fresh_i_id = fresh_i.id

    res = client.delete(
        f"/api/ministerios/{m1_id}/integrantes/{fresh_i_id}",
        headers=auth(admin_token),
    )
    assert res.status_code == 204


def test_add_tarefa_to_ministerio(client, admin_token, seed_data):
    m1_id = seed_data["m1_id"]
    res = client.post(
        f"/api/ministerios/{m1_id}/tarefas",
        json={"nombre": "Tocar bateria"},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    body = res.json()
    assert body["nombre"] == "Tocar bateria"
    assert body["ministerio_id"] == m1_id


def test_delete_tarefa(client, admin_token, seed_data, db):
    import models
    m1_id = seed_data["m1_id"]
    fresh_t = models.MinisterioTarefa(ministerio_id=m1_id, nombre="Tarefa Delete")
    db.add(fresh_t)
    db.commit()
    fresh_t_id = fresh_t.id

    res = client.delete(f"/api/ministerios/tarefas/{fresh_t_id}", headers=auth(admin_token))
    assert res.status_code == 204


def test_add_integrante_to_tarefa(client, admin_token, seed_data, db):
    import models
    t1_id = seed_data["t1_id"]
    fresh_i = models.Integrante(nombre="AddToTarefa", apellidos="Test")
    db.add(fresh_i)
    db.commit()
    fresh_i_id = fresh_i.id

    res = client.post(
        f"/api/ministerios/tarefas/{t1_id}/integrantes",
        json={"integrante_id": fresh_i_id},
        headers=auth(admin_token),
    )
    assert res.status_code == 201
    assert res.json()["ok"] is True


def test_remove_integrante_from_tarefa(client, admin_token, seed_data, db):
    import models
    m1_id = seed_data["m1_id"]
    fresh_t = models.MinisterioTarefa(ministerio_id=m1_id, nombre="Tarefa Remove Test")
    fresh_i = models.Integrante(nombre="RemoveFromTarefa", apellidos="Test")
    db.add_all([fresh_t, fresh_i])
    db.flush()
    ti = models.MinisterioTarefaIntegrante(tarefa_id=fresh_t.id, integrante_id=fresh_i.id)
    db.add(ti)
    db.commit()
    fresh_t_id = fresh_t.id
    fresh_i_id = fresh_i.id

    res = client.delete(
        f"/api/ministerios/tarefas/{fresh_t_id}/integrantes/{fresh_i_id}",
        headers=auth(admin_token),
    )
    assert res.status_code == 204


def test_ministerio_includes_responsables(client, admin_token, seed_data):
    m1_id = seed_data["m1_id"]
    res = client.get(f"/api/ministerios/{m1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert "responsables" in body
    assert len(body["responsables"]) >= 1
    assert any(r["nombre"] == "Juan" for r in body["responsables"])


def test_ministerio_includes_tarefas(client, admin_token, seed_data):
    m1_id = seed_data["m1_id"]
    res = client.get(f"/api/ministerios/{m1_id}", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert "tarefas" in body
    assert len(body["tarefas"]) >= 1
