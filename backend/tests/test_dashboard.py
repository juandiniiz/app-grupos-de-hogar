def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_dashboard_stats_returns_all_fields(client, admin_token, seed_data):
    res = client.get("/api/stats/dashboard", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert "total_grupos" in body
    assert "total_integrantes" in body
    assert "total_membros" in body
    assert "integrantes_sin_grupo" in body
    assert "integrantes_sin_grupo_pct" in body
    assert "membros_sin_grupo" in body
    assert "membros_sin_grupo_pct" in body
    assert "total_en_ministerio" in body
    assert "supervisores_count" in body
    assert "responsables_count" in body
    assert "ayudantes_count" in body
    assert "total_visitantes" in body
    assert "avg_visitantes_por_grupo" in body
    assert "total_novos_crentes" in body
    assert "total_batizados" in body
    assert "total_de_outra_igreja" in body
    assert "reuniones_periodicas" in body
    assert "reuniones_comunhao" in body
    assert "reuniones_evangelisticas" in body
    assert "asistencia_ultimo_mes" in body
    assert "asistencia_ultimo_ano" in body
    assert "asistencia_total" in body
    assert "discipulado_no_iniciado" in body
    assert "discipulado_cursando" in body
    assert "discipulado_terminado" in body
    assert "pre_batismo_no_iniciado" in body
    assert "pre_batismo_cursando" in body
    assert "pre_batismo_terminado" in body
    assert "total_oraciones" in body
    assert "oraciones_respondidas" in body
    assert "testimonios_destacados" in body


def test_dashboard_counts_are_positive(client, admin_token, seed_data):
    res = client.get("/api/stats/dashboard", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    assert body["total_grupos"] >= 2
    assert body["total_integrantes"] >= 4
    assert body["total_membros"] >= 3
    assert body["total_batizados"] >= 2
    assert body["total_de_outra_igreja"] >= 1
    assert body["reuniones_periodicas"] >= 1
    assert body["reuniones_comunhao"] >= 1
    assert body["total_oraciones"] >= 1


def test_dashboard_testimonios_destacados(client, admin_token, seed_data):
    res = client.get("/api/stats/dashboard", headers=auth(admin_token))
    assert res.status_code == 200
    body = res.json()
    destacados = body["testimonios_destacados"]
    assert isinstance(destacados, list)
    titulos = [t["titulo"] for t in destacados]
    assert "Sanidad milagrosa" in titulos


def test_dashboard_no_auth(client):
    res = client.get("/api/stats/dashboard")
    assert res.status_code == 401


def test_dashboard_supervisor_sees_own_data(client, supervisor_token, seed_data):
    res = client.get("/api/stats/dashboard", headers=auth(supervisor_token))
    assert res.status_code == 200
    body = res.json()
    assert "total_grupos" in body
    assert body["total_grupos"] >= 1


def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
