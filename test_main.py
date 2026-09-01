from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Testa se a rota de verificação de saúde está respondendo corretamente."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_laudo_valido():
    """Testa se a rota de predição funciona com um texto válido."""
    payload = {"texto": "Paciente apresenta quadro febril e tosse seca."}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "classificacao" in data
    assert "tempo_processamento_ms" in data

def test_predict_laudo_invalido():
    """Testa se a API barra envios de laudos vazios."""
    payload = {"texto": "   "}
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "O texto do laudo não pode ser vazio."