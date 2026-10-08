import io
import os
from PIL import Image
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def create_mock_leaf_bytes():
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_predict_endpoint_success():
    img_bytes = create_mock_leaf_bytes()
    response = client.post(
        "/api/v1/predict",
        files={"file": ("leaf.jpg", img_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "scan_id" in data
    assert "crop" in data
    assert "disease" in data
    assert "confidence" in data
    assert "treatment" in data
    assert "heatmap_url" in data
    assert isinstance(data["top_predictions"], list)

def test_predict_invalid_file():
    bad_bytes = b"This is plain text and not an image"
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test.txt", bad_bytes, "text/plain")}
    )
    assert response.status_code == 400
