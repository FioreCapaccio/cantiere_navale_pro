"""Archivio: cancellazione selettiva di file e cartelle."""
import io


def _upload(api, folder_id, name):
    r = api.post(f"/archive/files?folder_id={folder_id}", files={"file": (name, io.BytesIO(b"contenuto " + name.encode()))})
    assert r.status_code == 201, r.text
    return r.json()


def test_cancellazione_selettiva(api):
    folder = api.post("/archive/folders", json={"name": "Test selettivo"}).json()
    files = [_upload(api, folder["id"], f"doc{i}.txt") for i in range(4)]
    ids = [f["id"] for f in files]
    r = api.post("/archive/files/bulk-delete", json={"ids": ids[:2] + [999999]})
    assert r.status_code == 200 and r.json()["deleted"] == 2
    rest = api.get(f"/archive/files?folder_id={folder['id']}").json()
    assert sorted(f["id"] for f in rest) == sorted(ids[2:])
    # lista vuota rifiutata
    assert api.post("/archive/files/bulk-delete", json={"ids": []}).status_code == 422


def test_cartella_con_file_serve_conferma(api):
    folder = api.post("/archive/folders", json={"name": "Con file"}).json()
    f = _upload(api, folder["id"], "a.txt")
    assert api.delete(f"/archive/folders/{folder['id']}").status_code == 400
    assert api.delete(f"/archive/folders/{folder['id']}?with_files=true").status_code == 204
    assert api.get(f"/archive/files/{f['id']}/download").status_code == 404


def test_operatore_non_cancella_dall_archivio(api):
    api.post("/users", json={"username": "operaio2", "password": "password2", "role": "user"})
    tok = api.post("/auth/token", data={"username": "operaio2", "password": "password2"}).json()["access_token"]
    folder = api.post("/archive/folders", json={"name": "Protetta"}).json()
    f = _upload(api, folder["id"], "b.txt")
    h = {"Authorization": "Bearer " + tok}
    assert api.post("/archive/files/bulk-delete", json={"ids": [f["id"]]}, headers=h).status_code == 403
    assert api.delete(f"/archive/files/{f['id']}", headers=h).status_code == 403
