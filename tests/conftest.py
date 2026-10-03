import os
import sys
import tempfile
from pathlib import Path

# database e allegati in una cartella temporanea: i test non toccano i dati veri
_TMP = tempfile.mkdtemp(prefix="cantiere_test_")
os.environ["CANTIERE_DATA_DIR"] = _TMP
os.environ["ADMIN_PASSWORD"] = "admin123"
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture(scope="session")
def client():
    with TestClient(main.app) as c:
        r = c.post("/auth/token", data={"username": "admin", "password": "admin123"})
        assert r.status_code == 200, r.text
        c.headers.update({"Authorization": "Bearer " + r.json()["access_token"]})
        yield c


@pytest.fixture()
def api(client):
    return client


def make_client(api, **extra):
    body = {"name": "Cliente Test", "vat": "00743110157", "address": "Via Roma 1",
            "zip": "20100", "city": "Milano", "province": "MI"}
    body.update(extra)
    r = api.post("/clients", json=body)
    assert r.status_code == 201, r.text
    return r.json()


def make_doc(api, client_id, lines, kind="Fattura", **extra):
    body = {"kind": kind, "client_id": client_id, "lines": lines}
    body.update(extra)
    r = api.post("/documents", json=body)
    assert r.status_code == 201, r.text
    return r.json()
