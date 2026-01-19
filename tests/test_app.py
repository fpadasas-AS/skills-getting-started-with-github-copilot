import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_get_activities():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_unregister():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Sign up a new participant
        signup_resp = await ac.post("/activities/Chess Club/signup?email=tester@mergington.edu")
        assert signup_resp.status_code == 200
        # Unregister the participant
        unregister_resp = await ac.post("/activities/Chess Club/unregister", json={"email": "tester@mergington.edu"})
        assert unregister_resp.status_code == 200
        # Try to unregister again (should fail)
        unregister_resp2 = await ac.post("/activities/Chess Club/unregister", json={"email": "tester@mergington.edu"})
        assert unregister_resp2.status_code == 400

@pytest.mark.asyncio
async def test_signup_duplicate():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Sign up an existing participant
        resp = await ac.post("/activities/Chess Club/signup?email=michael@mergington.edu")
        assert resp.status_code == 400
        assert "already signed up" in resp.json()["detail"]

@pytest.mark.asyncio
async def test_unregister_not_found():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/activities/Chess Club/unregister", json={"email": "notfound@mergington.edu"})
        assert resp.status_code == 400
        assert "not registered" in resp.json()["detail"]
