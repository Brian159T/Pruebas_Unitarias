import pytest
from unittest.mock import patch, MagicMock
from app import app  

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

@patch("requests.get")
def test_descargar_pdfs(mock_get, client):
    # Simular respuesta de la página con un link a PDF
    mock_response = MagicMock()
    mock_response.text = '<a href="reporte.pdf">Reporte</a>'
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    resp = client.post("/api/descargar_pdfs", json={"url": "http://fake-url.com"})
    data = resp.get_json()

    assert resp.status_code == 200
    assert "total" in data
    assert data["total"] == 1
@patch("mensajes_bp.Client")
def test_alertar_usuario(mock_client, client):
    mock_instance = mock_client.return_value
    mock_instance.messages.create.return_value.sid = "fakeSID123"

    payload = {
        "numero": "+59170000000",
        "alerta": {
            "Cuencas": "Taquina",
            "Rios": "Río Taquina",
            "Niveles": 3.5,
            "Condiciones": "Ascenso rápido",
            "Pronosticos": "Roja",
            "Periodos": "Mañana"
        }
    }

    resp = client.post("/api/alertar", json=payload)
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["mensaje"] == "✅ Alerta enviada"
    mock_instance.messages.create.assert_called_once()
    
@patch("mensajes_bp.mysql.connection.cursor")
@patch("mensajes_bp.Client")
def test_alerta_personalizada(mock_client, mock_cursor, client):
    # Simular usuarios en la DB
    mock_cursor_instance = mock_cursor.return_value
    mock_cursor_instance.fetchall.return_value = [
        (1, "Rol", "pass", "+59170000000", "mail@test.com", "Ana", -66.15, -17.38)  # Dentro de radio
    ]
    mock_cursor_instance.fetchone.return_value = (-17.38, -66.15)  # Punto A en mismas coords

    mock_instance = mock_client.return_value
    mock_instance.messages.create.return_value.sid = "fakeSID456"

    payload = {
        "alerta": {
            "Cuencas": "Taquina",
            "Rios": "Río Taquina",
            "Niveles": 4.2,
            "Condiciones": "Desborde inminente",
            "Pronosticos": "Roja",
            "Periodos": "Hoy"
        }
    }

    resp = client.post("/api/alerta_personalizada", json=payload)
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["mensaje"] == "✅ Alertas procesadas correctamente"
    mock_instance.messages.create.assert_called_once()
    
# objetivos

# Validar que tu scraper de PDFs funciona sin depender de SENAMHI real.

# Verificar que tu API formatea y envía alertas correctamente (mockeando Twilio).

# Comprobar que la lógica de distancia y filtro de usuarios para alerta personalizada funciona.
print("Hola, pruebas unitarias")