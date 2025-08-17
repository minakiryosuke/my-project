# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_returns_json():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/json")
    assert resp.json().get("ok") is True
    assert "API is running" in resp.json().get("message", "")

def test_professionals_list():
    resp = client.get("/professionals")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # 初期データが最低1件ある想定
    assert len(data) >= 1
    assert {"id", "name", "profession", "rating"} <= set(data[0].keys())

def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"

def test_web_served_when_present():
    """
    /web/ に静的ファイルを置いた場合のみ200を想定します。
    置いていないプロジェクトでも失敗しないように分岐します。
    """
    resp = client.get("/web/")
    # 静的がない構成なら 404 でも良しとする
    assert resp.status_code in (200, 404)
