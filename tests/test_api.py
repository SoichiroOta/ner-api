from starlette.testclient import TestClient

from app.api import app


def test_docs_redirect():
    client = TestClient(app)
    response = client.get("/")
    assert response.history[0].status_code == 307
    assert response.status_code == 200
    assert response.url == "http://testserver/docs"


def test_api():
    client = TestClient(app)

    text = """But Google is starting from behind. The company made a late push
 into hardware, and Apple's Siri, available on iPhones, and Amazon's Alexa
 software, which runs on its Echo and Dot devices, have clear leads in
 consumer adoption."""

    request_data = {"values": [{"recordId": "a1", "data": {"text": text, "language": "en"}}]}

    response = client.post("/api/entities", json=request_data)
    assert response.status_code == 200

    first_record = response.json()["values"][0]
    assert first_record["recordId"] == "a1"
    assert first_record["errors"] is None
    assert first_record["warnings"] is None

    print(first_record["data"]["entities"])
    assert first_record["data"]["entities"] == [
        {"name": "Google", "label": "ORG", "matches": [{"start": 4, "end": 10, "text": "Google"}]},
        {"name": "Apple", "label": "ORG", "matches": [{"start": 85, "end": 90, "text": "Apple"}]},
        {"name": "Siri", "label": "ORG", "matches": [{"start": 93, "end": 97, "text": "Siri"}]},
        {"name": "iPhones", "label": "MISC", "matches": [{"start": 112, "end": 119, "text": "iPhones"}]},
        {"name": "Amazon", "label": "ORG", "matches": [{"start": 125, "end": 131, "text": "Amazon"}]},
        {"name": "Alexa", "label": "ORG", "matches": [{"start": 134, "end": 139, "text": "Alexa"}]},
        {"name": "Echo", "label": "MISC", "matches": [{"start": 169, "end": 173, "text": "Echo"}]},
    ]
