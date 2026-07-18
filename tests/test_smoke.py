from app import create_app


def test_app_creates():
    app = create_app()
    assert app is not None
    with app.test_client() as c:
        r = c.get("/login")
        assert r.status_code == 200
