from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_language_switch_romanian():
    res = client.post("/api/simulate-turn", json={"session_id": "1", "user_text": "Buna, vreau factura"})
    assert res.status_code == 200
    body = res.json()
    assert body["language"] == "ro"


def test_language_switch_english():
    res = client.post("/api/simulate-turn", json={"session_id": "2", "user_text": "Hello, I need my invoice"})
    assert res.status_code == 200
    body = res.json()
    assert body["language"] == "en"


def test_twilio_webhook_xml():
    res = client.post("/twilio/voice", data={"CallSid": "CA123", "SpeechResult": "Buna"})
    assert res.status_code == 200
    assert "<Response><Say" in res.text
