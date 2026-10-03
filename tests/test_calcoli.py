"""Test dei calcoli: totali documento, pagamenti, numerazione, IVA, magazzino, commesse."""
from decimal import Decimal

import pytest

import main
from conftest import make_client, make_doc


# ---------- totali documento ----------

class _L:
    def __init__(self, qty, price):
        self.qty, self.price = qty, price


class _Doc:
    def __init__(self, lines, tax=22, discount=0, pct=0, payments=()):
        self.lines = [_L(*l) for l in lines]
        self.tax_rate, self.discount, self.discount_pct = tax, discount, pct
        self.payments = [type("P", (), {"amount": a}) for a in payments]


def test_totali_semplici():
    t = main.document_totals(_Doc([(2, 50), (1, 10.5)]))
    assert t["subtotal"] == 110.5
    assert t["tax"] == 24.31
    assert t["total"] == 134.81


def test_arrotondamento_riga_per_riga():
    # 3 x 0.335 = 1.005 -> 1.01 (mezzo in su, non l'arrotondamento "del banchiere" dei float)
    t = main.document_totals(_Doc([(3, 0.335)], tax=0))
    assert t["subtotal"] == 1.01
    # 0.1 + 0.2 non deve dare rumore binario
    t = main.document_totals(_Doc([(1, 0.1), (1, 0.2)], tax=0))
    assert t["total"] == 0.3


def test_sconto_percentuale_ed_euro():
    t = main.document_totals(_Doc([(1, 1000)], pct=10, discount=50))
    assert t["discount_amount"] == 150
    assert t["taxable"] == 850
    assert t["tax"] == 187
    assert t["total"] == 1037


def test_sconto_non_supera_subtotale():
    t = main.document_totals(_Doc([(1, 100)], discount=500))
    assert t["taxable"] == 0 and t["total"] == 0


def test_residuo():
    t = main.document_totals(_Doc([(1, 100)], payments=[30, 0.01]))
    assert t["paid"] == 30.01
    assert t["residual"] == 91.99


def test_partita_iva():
    assert main.valid_partita_iva("00743110157")
    assert not main.valid_partita_iva("00743110158")
    assert not main.valid_partita_iva("123")


# ---------- API: documenti e pagamenti ----------

def test_numerazione_senza_duplicati_dopo_eliminazione(api):
    c = make_client(api)
    d1 = make_doc(api, c["id"], [], kind="DDT")
    d2 = make_doc(api, c["id"], [], kind="DDT")
    assert api.delete(f"/documents/{d1['id']}").status_code == 204
    d3 = make_doc(api, c["id"], [], kind="DDT")
    assert d3["number"] != d2["number"]
    assert int(d3["number"][-5:]) == int(d2["number"][-5:]) + 1


def test_sconto_cliente_applicato_in_percentuale(api):
    c = make_client(api, name="Cliente sconto", discount=10)
    d = make_doc(api, c["id"], [{"description": "Lavoro", "qty": 1, "price": 1000}])
    assert d["discount_pct"] == 10
    assert d["total"] == 1098.0  # (1000 - 100) * 1.22


def test_pagamenti_stato_e_limiti(api):
    c = make_client(api)
    d = make_doc(api, c["id"], [{"description": "Lavoro", "qty": 1, "price": 100}])
    assert d["total"] == 122.0
    r = api.post(f"/documents/{d['id']}/payments", json={"amount": 50})
    assert r.status_code == 201
    doc = api.get(f"/documents/{d['id']}").json()
    assert doc["status"] == "emessa" and doc["residual"] == 72.0
    # non si incassa più del dovuto
    assert api.post(f"/documents/{d['id']}/payments", json={"amount": 72.01}).status_code == 400
    # saldo esatto (anche con centesimi) -> pagata
    pid = api.post(f"/documents/{d['id']}/payments", json={"amount": 72}).json()["id"]
    assert api.get(f"/documents/{d['id']}").json()["status"] == "pagata"
    # eliminando un pagamento torna emessa
    assert api.delete(f"/documents/{d['id']}/payments/{pid}").status_code == 204
    assert api.get(f"/documents/{d['id']}").json()["status"] == "emessa"


def test_stato_pagata_solo_con_pagamento(api):
    c = make_client(api)
    d = make_doc(api, c["id"], [{"description": "x", "qty": 1, "price": 10}])
    assert api.post(f"/documents/{d['id']}/status?status_value=pagata").status_code == 400


def test_non_si_riduce_il_totale_sotto_l_incassato(api):
    c = make_client(api)
    d = make_doc(api, c["id"], [{"description": "x", "qty": 1, "price": 100}])
    api.post(f"/documents/{d['id']}/payments", json={"amount": 100})
    line_id = api.get(f"/documents/{d['id']}").json()["lines"][0]["id"]
    # documento ancora "emessa" (non saldato 122): riduzione sotto 100 vietata
    r = api.put(f"/documents/{d['id']}/lines/{line_id}", json={"description": "x", "qty": 1, "price": 50})
    assert r.status_code == 400


def test_valori_negativi_rifiutati(api):
    c = make_client(api)
    r = api.post("/documents", json={"kind": "Fattura", "client_id": c["id"],
                                      "lines": [{"description": "x", "qty": -1, "price": 10}]})
    assert r.status_code == 422
    assert "quantità" in r.json()["detail"]


def test_emissione_fattura_richiede_righe_e_dati(api):
    c = make_client(api, name="Senza indirizzo", address="", city="", zip="")
    d = make_doc(api, c["id"], [])
    r = api.post(f"/documents/{d['id']}/status?status_value=emessa")
    assert r.status_code == 400


def test_dashboard_esclude_bozze(api):
    before = api.get("/dashboard").json()
    c = make_client(api)
    make_doc(api, c["id"], [{"description": "x", "qty": 1, "price": 1000}])  # bozza
    after = api.get("/dashboard").json()
    assert after["invoiced"] == before["invoiced"]


# ---------- fattura elettronica ----------

def _setup_company(api):
    r = api.put("/settings", json={
        "company_name": "Cantiere Test Srl", "company_vat": "00743110157", "company_tax_code": "00743110157",
        "company_address": "Via del Porto 1", "company_zip": "16100", "company_city": "Genova",
        "company_province": "GE", "iban": "IT60X0542811101000000123456",
        "default_tax_rate": 22, "default_payment_days": 30})
    assert r.status_code == 200, r.text


def test_xml_completo_e_coerente(api):
    _setup_company(api)
    c = make_client(api, name="Cliente XML & Co", sdi_code="ABC1234")
    d = make_doc(api, c["id"], [{"description": "Carena", "qty": 2, "price": 100.55, "unit": "ore"}],
                 discount=10)
    r = api.get(f"/documents/{d['id']}/xml")
    assert r.status_code == 200, r.text
    xml = r.text
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    assert "Cliente XML &amp; Co" in xml
    assert "<CodiceDestinatario>ABC1234</CodiceDestinatario>" in xml
    assert "<DatiRiepilogo>" in xml and "<DatiPagamento>" in xml
    # imponibile = 201.10 - 10 = 191.10 ; IVA 42.04 ; totale 233.14
    assert "<ImponibileImporto>191.10</ImponibileImporto>" in xml
    assert "<Imposta>42.04</Imposta>" in xml
    assert "<ImportoTotaleDocumento>233.14</ImportoTotaleDocumento>" in xml
    # le righe (incluso lo sconto) sommano all'imponibile
    totals = [Decimal(e.text) for e in root.iter("PrezzoTotale")]
    assert sum(totals) == Decimal("191.10")


def test_xml_iva_zero_richiede_natura(api):
    _setup_company(api)
    c = make_client(api)
    d = make_doc(api, c["id"], [{"description": "Varo", "qty": 1, "price": 500}], tax_rate=0)
    assert api.get(f"/documents/{d['id']}/xml").status_code == 400
    api.put(f"/documents/{d['id']}", json={"vat_nature": "N3.4"})
    r = api.get(f"/documents/{d['id']}/xml")
    assert r.status_code == 200 and "<Natura>N3.4</Natura>" in r.text


# ---------- magazzino ----------

def _item_wh(api):
    wh = api.get("/warehouses").json()[0]
    item = api.post("/items", json={"name": "Vernice", "cost": 0, "price": 0}).json()
    return wh, item


def test_costo_medio_ponderato(api):
    wh, item = _item_wh(api)
    api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "carico", "qty": 10, "unit_cost": 10})
    api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "carico", "qty": 10, "unit_cost": 20})
    cost = [i for i in api.get("/items").json() if i["id"] == item["id"]][0]["cost"]
    assert cost == 15


def test_scarico_usa_costo_articolo_e_giacenza(api):
    wh, item = _item_wh(api)
    api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "carico", "qty": 5, "unit_cost": 8})
    r = api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "scarico", "qty": 2})
    assert r.status_code == 201 and r.json()["unit_cost"] == 8
    r = api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "scarico", "qty": 4})
    assert r.status_code == 400  # ne restano 3


# ---------- commessa ----------

def test_riepilogo_commessa(api):
    wh, item = _item_wh(api)
    c = make_client(api)
    p = api.post("/projects", json={"client_id": c["id"], "title": "Refit"}).json()
    api.post(f"/projects/{p['id']}/jobs", json={"description": "Manodopera", "category": "Manodopera", "qty": 10, "unit": "ore", "unit_cost": 30, "unit_price": 50})
    api.post(f"/projects/{p['id']}/jobs", json={"description": "Subappalto", "category": "Subappalto", "qty": 1, "unit_cost": 200, "unit_price": 300})
    s = api.get(f"/projects/{p['id']}/summary").json()
    assert s["revenue"] == 800 and s["labor_cost"] == 300 and s["other_cost"] == 200 and s["margin"] == 300
    # con ore registrate usa il consuntivo
    api.post(f"/projects/{p['id']}/timesheets", json={"hours": 4, "hourly_cost": 40, "hourly_price": 60})
    api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "carico", "qty": 5, "unit_cost": 10})
    api.post("/movements", json={"warehouse_id": wh["id"], "item_id": item["id"], "type": "scarico", "qty": 2, "project_id": p["id"]})
    s = api.get(f"/projects/{p['id']}/summary").json()
    assert s["labor_cost"] == 160 and s["material_cost"] == 20 and s["total_cost"] == 380
    assert s["margin"] == 420 and s["margin_pct"] == 52.5


# ---------- IVA ----------

def test_registro_iva(api):
    _setup_company(api)
    c = make_client(api)
    d = make_doc(api, c["id"], [{"description": "x", "qty": 1, "price": 1000}])
    assert api.post(f"/documents/{d['id']}/status?status_value=emessa").status_code == 200
    sup = api.post("/suppliers", json={"name": "Forn"}).json()
    api.post("/purchase-invoices", json={"supplier_id": sup["id"], "amount_net": 100, "vat_rate": 22})
    reg = api.get("/vat-register").json()
    assert reg["summary"]["sales_vat"] >= 220
    assert reg["summary"]["purchases_vat"] >= 22
    assert any(r["rate"] == 22 for r in reg["sales_by_rate"])


# ---------- sicurezza ----------

def test_blocco_dopo_troppi_tentativi(client):
    for _ in range(5):
        r = client.post("/auth/token", data={"username": "ghost", "password": "x"})
        assert r.status_code == 401
    r = client.post("/auth/token", data={"username": "ghost", "password": "x"})
    assert r.status_code == 429


def test_operatore_non_puo_eliminare(api):
    api.post("/users", json={"username": "operaio", "password": "password1", "role": "user"})
    tok = api.post("/auth/token", data={"username": "operaio", "password": "password1"}).json()["access_token"]
    c = make_client(api)
    r = api.delete(f"/clients/{c['id']}", headers={"Authorization": "Bearer " + tok})
    assert r.status_code == 403
