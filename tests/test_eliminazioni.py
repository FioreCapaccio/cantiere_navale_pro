"""Eliminazioni da elenchi e prenotazioni agenda."""
from conftest import make_client, make_doc


def test_elimina_cliente_con_barche_e_commesse(api):
    c = make_client(api, name="Da eliminare")
    b = api.post("/boats", json={"client_id": c["id"], "name": "Barca"}).json()
    p = api.post("/projects", json={"client_id": c["id"], "boat_id": b["id"], "title": "Lavori"}).json()
    assert api.delete(f"/clients/{c['id']}").status_code == 204
    assert api.get(f"/boats/{b['id']}/detail").status_code == 404
    assert p["id"] not in [x["id"] for x in api.get("/projects").json()]


def test_cliente_con_documenti_non_si_elimina(api):
    c = make_client(api)
    make_doc(api, c["id"], [], kind="DDT")
    r = api.delete(f"/clients/{c['id']}")
    assert r.status_code == 400 and "documenti" in r.json()["detail"]


def test_elimina_imbarcazione_stacca_le_commesse(api):
    c = make_client(api)
    b = api.post("/boats", json={"client_id": c["id"], "name": "B2"}).json()
    p = api.post("/projects", json={"client_id": c["id"], "boat_id": b["id"], "title": "T"}).json()
    assert api.delete(f"/boats/{b['id']}").status_code == 204
    assert [x for x in api.get("/projects").json() if x["id"] == p["id"]][0]["boat_id"] is None


def test_documenti_eliminabili(api):
    c = make_client(api)
    ddt = make_doc(api, c["id"], [{"description": "x", "qty": 1, "price": 10}], kind="DDT")
    api.post(f"/documents/{ddt['id']}/status?status_value=emessa")
    fattura = api.post(f"/documents/{ddt['id']}/convert").json()
    # DDT emesso: eliminabile, la fattura generata resta (scollegata)
    assert api.delete(f"/documents/{ddt['id']}").status_code == 204
    assert api.get(f"/documents/{fattura['id']}").json()["source_document_id"] is None
    # fattura in bozza: eliminabile; emessa: solo annullabile
    bozza = make_doc(api, c["id"], [{"description": "x", "qty": 1, "price": 10}])
    assert api.delete(f"/documents/{bozza['id']}").status_code == 204


def test_fattura_emessa_non_si_elimina(api):
    api.put("/settings", json={"company_name": "X Srl", "company_vat": "00743110157", "company_address": "Via 1",
                               "company_zip": "16100", "company_city": "Genova"})
    c = make_client(api)
    f = make_doc(api, c["id"], [{"description": "x", "qty": 1, "price": 10}])
    assert api.post(f"/documents/{f['id']}/status?status_value=emessa").status_code == 200
    r = api.delete(f"/documents/{f['id']}")
    assert r.status_code == 400 and "annullala" in r.json()["detail"]
    assert api.post(f"/documents/{f['id']}/status?status_value=annullata").status_code == 200


def test_prenotazione_nuova_e_modifica(api):
    res = api.post("/resources", json={"name": "Scalo A"}).json()
    b = api.post("/bookings", json={"resource_id": res["id"], "title": "Carenaggio",
                                     "start_date": "2026-11-02", "end_date": "2026-11-05"})
    assert b.status_code == 201, b.text
    bid = b.json()["id"]
    r = api.put(f"/bookings/{bid}", json={"resource_id": res["id"], "title": "Carenaggio 2",
                                           "start_date": "2026-11-02", "end_date": "2026-11-06"})
    assert r.status_code == 200 and r.json()["title"] == "Carenaggio 2"
    # sovrapposta: rifiutata
    r = api.post("/bookings", json={"resource_id": res["id"], "title": "Altra",
                                     "start_date": "2026-11-04", "end_date": "2026-11-07"})
    assert r.status_code == 400
    assert api.delete(f"/bookings/{bid}").status_code == 204


def test_elimina_commessa_con_tutto_il_collegato(api):
    c = make_client(api)
    p = api.post("/projects", json={"client_id": c["id"], "title": "Pieno"}).json()
    api.post(f"/projects/{p['id']}/jobs", json={"description": "L", "qty": 1})
    api.post(f"/projects/{p['id']}/timesheets", json={"hours": 2})
    make_doc(api, c["id"], [], kind="DDT", project_id=p["id"])
    res = api.post("/resources", json={"name": "Scalo P"}).json()
    api.post("/bookings", json={"resource_id": res["id"], "project_id": p["id"], "title": "B",
                                 "start_date": "2027-01-10", "end_date": "2027-01-12"})
    assert api.delete(f"/projects/{p['id']}").status_code == 204


def test_elimina_anagrafiche_varie(api):
    wh = api.get("/warehouses").json()[0]
    item = api.post("/items", json={"name": "Da togliere"}).json()
    assert api.delete(f"/items/{item['id']}").status_code == 204
    used = api.post("/items", json={"name": "Usato"}).json()
    api.post("/movements", json={"warehouse_id": wh["id"], "item_id": used["id"], "type": "carico", "qty": 1})
    assert api.delete(f"/items/{used['id']}").status_code in (204, 400)  # mai un errore 500
    sup = api.post("/suppliers", json={"name": "Forn eliminabile"}).json()
    assert api.delete(f"/suppliers/{sup['id']}").status_code == 204
    w = api.post("/workers", json={"name": "Mario"}).json()
    assert api.delete(f"/workers/{w['id']}").status_code == 204


def test_articolo_con_giacenza_zero_e_senza_movimenti_si_elimina(api):
    wh = api.get("/warehouses").json()[0]
    item = api.post("/items", json={"name": "Solo riga a zero"}).json()
    # una riga di giacenza a 0 (carico e scarico) non deve bloccare... ma lo storico sì
    api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "carico", "qty": 2})
    api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "scarico", "qty": 2})
    use = api.get(f"/items/{item['id']}/usage").json()
    assert use["stock_qty"] == 0 and use["movements"] == 2
    r = api.delete(f"/items/{item['id']}")
    assert r.status_code == 400 and "2 movimenti" in r.json()["detail"]
    assert api.delete(f"/items/{item['id']}?force=true").status_code == 204
    assert item["id"] not in [i["id"] for i in api.get("/items").json()]


def test_articolo_con_giacenza_richiede_force(api):
    wh = api.get("/warehouses").json()[0]
    item = api.post("/items", json={"name": "In giacenza", "unit": "kg"}).json()
    api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "carico", "qty": 5})
    r = api.delete(f"/items/{item['id']}")
    assert r.status_code == 400 and "giacenza" in r.json()["detail"]
    sup = api.post("/suppliers", json={"name": "F"}).json()
    po = api.post("/purchase-orders", json={"supplier_id": sup["id"], "lines": [
        {"item_id": item["id"], "description": "riga", "qty": 1, "unit_cost": 1}]}).json()
    assert api.delete(f"/items/{item['id']}?force=true").status_code == 204
    line = api.get(f"/purchase-orders/{po['id']}").json()["lines"][0]
    assert line["item_id"] is None and line["description"] == "riga"
