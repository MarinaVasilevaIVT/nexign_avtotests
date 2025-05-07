import pytest
import requests
import os

CDR_UPLOAD_URL = "http://example.com"
CDR_DIR = "negixn/cdr"

def test_upload_cdr_success():
    files = {"file": open("negixn/cdr/positive_test.csv", "rb")}
    response = requests.post(CDR_UPLOAD_URL, files=files)
    
    assert response.status_code == 200
    assert response.json()["message"] == "CDR processed successfully"

negative_cdr_files = [
    os.path.join(CDR_DIR, f)
    for f in os.listdir(CDR_DIR)
    if f.startswith("negative_test_") and f.endswith(".csv")
]

@pytest.mark.parametrize("cdr_file", negative_cdr_files)
def test_upload_negative_cdr_should_fail(cdr_file):
    files = {"file": open(cdr_file, "rb")}
    response = requests.post(CDR_UPLOAD_URL, files=files)
    
    # Проверяем, что статус 4xx и есть сообщение об ошибке
    assert response.status_code >= 400, (
        f"Ожидалась ошибка 4xx, но получен {response.status_code} "
        f"для файла {cdr_file}"
    )
    assert "error" in response.json(), (
        f"Ожидался JSON с ошибкой, но получено: {response.text}"
    )