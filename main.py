import os
import sys
import re
import uuid
import shutil
import socket
import secrets
import hashlib
import logging
import threading
import webbrowser
from datetime import datetime, timedelta, timezone, date as Date
from pathlib import Path
from typing import List, Optional
from xml.sax.saxutils import escape

import uvicorn
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Percorsi (funzionano sia in sviluppo sia dentro un eseguibile pacchettizzato)
# ---------------------------------------------------------------------------


FROZEN = getattr(sys, "frozen", False)


def _resolve_base_dir() -> Path:
    """Cartella dei file di programma (static inclusi)."""
    if FROZEN:
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent)).resolve()
    return Path(__file__).resolve().parent


def _ensure_writable(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".write_test"
        probe.write_text("ok")
        probe.unlink()
        return True
    except OSError:
        return False


def _default_data_dir() -> Path:
    """Dati (db, upload, log): accanto all'app quando è scrivibile (es. disco,
    chiavetta, Applicazioni). Se il volume è di sola lettura (es. app lanciata
    direttamente dal DMG montato) usa la cartella dati dell'utente."""
    candidates = []
    if not FROZEN:
        candidates.append(Path(__file__).resolve().parent / "data")
    else:
        exe_dir = Path(sys.executable).resolve().parent
        if sys.platform == "darwin":
            p = exe_dir
            while p != p.parent:
                if p.suffix == ".app":
                    candidates.append(p.parent / "CantiereNavaleData")
                    break
                p = p.parent
            candidates.append(exe_dir / "CantiereNavaleData")
        else:
            candidates.append(exe_dir / "data")
    # Cartella dati standard dell'utente: sempre scrivibile
    if os.name == "nt":
        base = Path(os.getenv("APPDATA") or Path.home())
    else:
        base = Path.home() / "Library" / "Application Support"
    candidates.append(base / "CantiereNavalePro")

    for cand in candidates:
        if _ensure_writable(cand):
            if cand != candidates[0]:
                logging.getLogger().info(
                    "La cartella accanto all'app non è scrivibile: uso %s", cand
                )
            return cand
    raise RuntimeError("Nessuna cartella dati scrivibile disponibile")


BASE_DIR = _resolve_base_dir()
_data_dir_env = os.getenv("CANTIERE_DATA_DIR")
DATA_DIR = Path(_data_dir_env) if _data_dir_env else _default_data_dir()
DATA_DIR.mkdir(parents=True, exist_ok=True)

# In modalità windowed (senza console) stdout/stderr non esistono: reindirizzali al log
if FROZEN:
    _log_file = open(DATA_DIR / "app.log", "a", encoding="utf-8")
    if sys.stdout is None:
        sys.stdout = _log_file
    if sys.stderr is None:
        sys.stderr = _log_file

UPLOAD_DIR = DATA_DIR / "uploads"
os.makedirs(UPLOAD_DIR / "projects", exist_ok=True)
os.makedirs(UPLOAD_DIR / "einvoice", exist_ok=True)

load_dotenv(BASE_DIR / ".env")
load_dotenv(DATA_DIR / ".env")

# Chiave JWT: variabile d'ambiente oppure chiave casuale persistente
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    _key_file = DATA_DIR / "secret_key"
    if _key_file.exists():
        SECRET_KEY = _key_file.read_text().strip()
    else:
        SECRET_KEY = secrets.token_hex(32)
        _key_file.write_text(SECRET_KEY)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8765"))
OPEN_BROWSER = os.getenv("OPEN_BROWSER", "1" if getattr(sys, "frozen", False) else "0") == "1"

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

DEFAULT_COMPANY = {
    "company_name": os.getenv("COMPANY_NAME", "Cantiere Navale SRL"),
    "company_vat": os.getenv("COMPANY_VAT", "00000000000"),
    "company_tax_code": os.getenv("COMPANY_TAX_CODE", "00000000000"),
    "company_address": os.getenv("COMPANY_ADDRESS", ""),
    "company_zip": os.getenv("COMPANY_ZIP", ""),
    "company_city": os.getenv("COMPANY_CITY", ""),
    "company_email": os.getenv("COMPANY_EMAIL", ""),
    "company_phone": os.getenv("COMPANY_PHONE", ""),
    "iban": os.getenv("COMPANY_IBAN", ""),
}

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'shipyard.db'}")

# ---------------------------------------------------------------------------
# Logging: quando l'app gira come eseguibile "windowed" il console non esiste,
# quindi logghiamo su file.
# ---------------------------------------------------------------------------

if getattr(sys, "frozen", False):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[logging.FileHandler(DATA_DIR / "app.log", encoding="utf-8")],
    )

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean,
    Date as SQLDate, DateTime, ForeignKey, UniqueConstraint, func as SQLFunc
)
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 30})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Importi: i calcoli usano Decimal con arrotondamento commerciale (mezzo in su)
# al centesimo, riga per riga, come fa una fattura elettronica.
# ---------------------------------------------------------------------------

from decimal import Decimal, ROUND_HALF_UP

_CENT = Decimal("0.01")


def D(value) -> Decimal:
    return Decimal(str(value if value is not None else 0))


def r2(value) -> Decimal:
    return D(value).quantize(_CENT, rounding=ROUND_HALF_UP)


def money(value) -> float:
    return float(r2(value))


# =========================
# MODELS
# =========================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, default="")
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # admin, manager, user
    active = Column(Boolean, default=True)


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, default="")           # codice cliente automatico
    name = Column(String, nullable=False)
    client_type = Column(String, default="Privato")  # Privato, Azienda, P.A.
    vat = Column(String, default="")
    tax_code = Column(String, default="")
    referente = Column(String, default="")      # persona di riferimento
    email = Column(String, default="")
    pec = Column(String, default="")
    phone = Column(String, default="")
    mobile = Column(String, default="")
    address = Column(String, default="")        # via
    zip = Column(String, default="")
    city = Column(String, default="")
    province = Column(String, default="")
    country = Column(String, default="Italia")
    ship_to = Column(String, default="")        # indirizzo di spedizione (DDT)
    iban = Column(String, default="")
    payment_terms = Column(String, default="")  # condizioni di pagamento
    discount = Column(Float, default=0)         # sconto abituale %
    website = Column(String, default="")
    secondary_phone = Column(String, default="")  # secondo telefono
    sdi_code = Column(String, default="")       # codice destinatario SdI (7 caratteri)
    active = Column(Boolean, default=True)
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)

    boats = relationship("Boat", back_populates="client")
    projects = relationship("Project", back_populates="client")
    documents = relationship("Document", back_populates="client")


class Boat(Base):
    __tablename__ = "boats"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    name = Column(String, nullable=False)
    registration = Column(String, default="")
    boat_type = Column(String, default="")
    length = Column(Float, nullable=True)       # metri
    engine = Column(String, default="")
    build_year = Column(Integer, nullable=True)
    hull_id = Column(String, default="")        # numero di scafo / HIN
    insurance_expiry = Column(SQLDate, nullable=True)
    notes = Column(String, default="")
    # Scheda tecnica completa
    builder = Column(String, default="")        # cantiere / costruttore
    model = Column(String, default="")
    hull_material = Column(String, default="")  # VTR, alluminio, acciaio…
    beam = Column(Float, nullable=True)         # baglio (m)
    draft = Column(Float, nullable=True)        # pescaggio (m)
    displacement = Column(Float, nullable=True) # stazza (t)
    engine_make = Column(String, default="")
    engine_model = Column(String, default="")
    engine_power_hp = Column(Float, nullable=True)
    engine_hours = Column(Float, nullable=True)
    fuel_type = Column(String, default="")      # benzina, diesel…
    flag = Column(String, default="")
    home_port = Column(String, default="")
    insurance_company = Column(String, default="")
    last_haul_out = Column(SQLDate, nullable=True)   # ultimo varo/settimo
    next_service_date = Column(SQLDate, nullable=True)  # prossimo tagliando
    yard_position = Column(String, default="")  # posizione nello scalo

    client = relationship("Client", back_populates="boats")


class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, default="")
    name = Column(String, nullable=False)
    category = Column(String, default="")
    unit = Column(String, default="pz")
    cost = Column(Float, default=0)
    price = Column(Float, default=0)
    min_stock = Column(Float, default=0)  # sotto questa quantità l'app segnala l'alert


class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    qty = Column(Float, default=0)

    __table_args__ = (UniqueConstraint("warehouse_id", "item_id", name="uq_stock_warehouse_item"),)


class Movement(Base):
    __tablename__ = "movements"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(SQLDate, default=Date.today)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    type = Column(String, nullable=False)  # carico, scarico, reso
    qty = Column(Float, nullable=False)
    unit_cost = Column(Float, default=0)
    note = Column(String, default="")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)  # commessa di riferimento


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    boat_id = Column(Integer, ForeignKey("boats.id"), nullable=True)
    title = Column(String, nullable=False)
    status = Column(String, default="aperta")  # aperta, in_lavorazione, completata, annullata
    start_date = Column(SQLDate, nullable=True)
    due_date = Column(SQLDate, nullable=True)
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)

    client = relationship("Client", back_populates="projects")
    boat = relationship("Boat")
    jobs = relationship("Job", back_populates="project", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, default="Manodopera")
    status = Column(String, default="Da fare")  # Da fare, In corso, Completata
    priority = Column(String, default="normale")  # bassa, normale, alta, urgente
    qty = Column(Float, default=1)
    unit = Column(String, default="pz")
    unit_cost = Column(Float, default=0)
    unit_price = Column(Float, default=0)
    assigned_to = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)

    project = relationship("Project", back_populates="jobs")


class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)
    content_type = Column(String, default="application/octet-stream")
    file_size = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    project = relationship("Project", back_populates="attachments")


class ArchiveFolder(Base):
    """Cartella dell'archivio documentale (contratti, certificati, …)."""
    __tablename__ = "archive_folders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)


class ArchiveFile(Base):
    """File generico conservato in archivio, indipendente dalle commesse."""
    __tablename__ = "archive_files"
    id = Column(Integer, primary_key=True, index=True)
    folder_id = Column(Integer, ForeignKey("archive_folders.id"), nullable=False)
    filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)
    content_type = Column(String, default="application/octet-stream")
    file_size = Column(Integer, default=0)
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    folder = relationship("ArchiveFolder")


# =========================
# ACQUISTI: fornitori, fatture di acquisto, ordini
# =========================

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    vat = Column(String, default="")
    email = Column(String, default="")
    phone = Column(String, default="")
    address = Column(String, default="")
    notes = Column(String, default="")

    invoices = relationship("PurchaseInvoice", back_populates="supplier")
    orders = relationship("PurchaseOrder", back_populates="supplier")


class PurchaseInvoice(Base):
    """Fattura ricevuta da un fornitore (registro IVA acquisti)."""
    __tablename__ = "purchase_invoices"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    number = Column(String, default="")
    date = Column(SQLDate, default=Date.today)
    due_date = Column(SQLDate, nullable=True)
    amount_net = Column(Float, default=0)
    vat_rate = Column(Float, default=22)
    status = Column(String, default="da_pagare")  # da_pagare, pagata
    paid_date = Column(SQLDate, nullable=True)
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)

    supplier = relationship("Supplier", back_populates="invoices")


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    date = Column(SQLDate, default=Date.today)
    expected_date = Column(SQLDate, nullable=True)
    status = Column(String, default="bozza")  # bozza, inviato, ricevuto, annullato
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)

    supplier = relationship("Supplier", back_populates="orders")
    lines = relationship("PurchaseOrderLine", back_populates="order", cascade="all, delete-orphan")


class PurchaseOrderLine(Base):
    __tablename__ = "purchase_order_lines"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=True)
    description = Column(String, nullable=False)
    qty = Column(Float, default=1)
    unit_cost = Column(Float, default=0)

    order = relationship("PurchaseOrder", back_populates="lines")
    item_ref = relationship("Item")


# =========================
# AGENDA SCALI: postazioni e prenotazioni
# =========================

class Resource(Base):
    """Postazione dello scalo: viaggio, bottega, seul, molo…"""
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rtype = Column(String, default="Postazione")  # Viaggio, Bottega, Seul, Postazione, Molo, Altro
    notes = Column(String, default="")

    bookings = relationship("Booking", back_populates="resource")


class Booking(Base):
    """Prenotazione di una postazione per un periodo (scalo, lavori a secco…)."""
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    boat_id = Column(Integer, ForeignKey("boats.id"), nullable=True)
    title = Column(String, nullable=False)
    start_date = Column(SQLDate, nullable=False)
    end_date = Column(SQLDate, nullable=False)
    status = Column(String, default="pianificato")  # pianificato, in_corso, completato, annullato
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)

    resource = relationship("Resource", back_populates="bookings")
    project = relationship("Project")
    boat = relationship("Boat")


# =========================
# TIMESHEET: ore lavorative per commessa
# =========================

class Worker(Base):
    """Lavoratore dello scalo, con le tariffe orarie."""
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, default="")          # es. Meccanico, Carpentiere
    hourly_cost = Column(Float, default=0)     # costo orario interno (€/h)
    hourly_price = Column(Float, default=0)    # prezzo orario di fatturazione (€/h)
    active = Column(Boolean, default=True)
    notes = Column(String, default="")
    # Anagrafica e scadenze amministrative
    employee_code = Column(String, default="")
    birth_date = Column(SQLDate, nullable=True)
    phone = Column(String, default="")
    email = Column(String, default="")
    iban = Column(String, default="")
    hire_date = Column(SQLDate, nullable=True)
    contract_type = Column(String, default="")  # es. CCNL Metalmeccanici, a tempo…
    weekly_hours = Column(Float, nullable=True)
    vacation_days = Column(Float, nullable=True)  # giorni ferie annui
    license = Column(String, default="")        # patente: B, C, nautica, carrello…
    license_expiry = Column(SQLDate, nullable=True)
    medical_exam_expiry = Column(SQLDate, nullable=True)   # visita medica
    safety_training_expiry = Column(SQLDate, nullable=True)  # corso sicurezza
    skills = Column(String, default="")
    certifications = Column(String, default="")
    emergency_contact = Column(String, default="")
    emergency_phone = Column(String, default="")

    entries = relationship("TimeEntry", back_populates="worker_ref")


class TimeEntry(Base):
    __tablename__ = "time_entries"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    worker = Column(String, default="")        # testo libero (vecchi inserimenti / occasionale)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)
    hourly_cost = Column(Float, default=0)     # tariffa registrata al momento (storicizzata)
    hourly_price = Column(Float, default=0)
    date = Column(SQLDate, default=Date.today)
    hours = Column(Float, nullable=False)
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)

    project = relationship("Project")
    job = relationship("Job")
    worker_ref = relationship("Worker", back_populates="entries")


class LookupOption(Base):
    """Valori configurabili delle tendine (es. categorie lavoro, tipi cliente).
    L'utente li gestisce da Impostazioni senza toccare il codice."""
    __tablename__ = "lookup_options"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)  # es. "categoria_lavoro"
    value = Column(String, nullable=False)
    sort_order = Column(Integer, default=0)

    __table_args__ = (UniqueConstraint("category", "value", name="uq_lookup_cat_val"),)


# Valori iniziali delle tendine: inseriti al primo avvio (tabella vuota),
# poi modificabili liberamente da Impostazioni.
DEFAULT_LOOKUPS = {
    "tipo_cliente": ["Privato", "Azienda", "P.A."],
    "categoria_lavoro": ["Manodopera", "Ricambi", "Materiali", "Noleggio", "Subappalto", "Altro"],
    "tipo_imbarcazione": ["Vela", "Motore", "Gommone", "Multiscafo", "Deriva"],
    "materiale_scafo": ["VTR", "Alluminio", "Acciaio", "Legno", "Cemento"],
    "alimentazione": ["Diesel", "Benzina", "Elettrico", "Ibrido", "GPL"],
    "ruolo_lavoratore": ["Meccanico", "Carpentiere", "Verniciatore", "Elettricista", "Velaio", "Manovale"],
}


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)

    kind = Column(String, nullable=False)  # DDT, Proforma, Fattura
    number = Column(String, unique=True, index=True)
    date = Column(SQLDate, default=Date.today)
    due_date = Column(SQLDate, nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    source_document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)

    status = Column(String, default="bozza")  # bozza, emessa, pagata, annullata
    tax_rate = Column(Float, default=22)
    vat_nature = Column(String, default="")     # natura IVA (N1…N7): obbligatoria se aliquota 0
    discount = Column(Float, default=0)         # sconto in euro
    discount_pct = Column(Float, default=0)     # sconto in percentuale (si somma a quello in euro)
    notes = Column(String, default="")

    # Campi DDT
    ddt_reason = Column(String, default="")
    ddt_carrier = Column(String, default="")
    ddt_destination = Column(String, default="")
    ddt_parcels = Column(Integer, nullable=True)
    ddt_weight = Column(Float, nullable=True)

    xml_path = Column(String, default="")
    created_by = Column(String, default="")     # username dell'utente che l'ha creato
    created_at = Column(DateTime, default=datetime.now)

    lines = relationship("DocumentLine", back_populates="document", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="document", cascade="all, delete-orphan")
    client = relationship("Client", back_populates="documents")
    project = relationship("Project", back_populates="documents")

    @property
    def total(self) -> float:
        return document_totals(self)["total"]

    @property
    def paid(self) -> float:
        return document_totals(self)["paid"]

    @property
    def residual(self) -> float:
        return document_totals(self)["residual"]


class DocumentLine(Base):
    __tablename__ = "document_lines"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    description = Column(String, nullable=False)
    qty = Column(Float, default=1)
    price = Column(Float, default=0)
    unit = Column(String, default="")  # es. "ore" per la manodopera: prezzo = €/ora

    document = relationship("Document", back_populates="lines")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    date = Column(SQLDate, default=Date.today)
    amount = Column(Float, nullable=False)
    method = Column(String, default="bonifico")
    note = Column(String, default="")

    document = relationship("Document", back_populates="payments")


class AppSettings(Base):
    """Dati azienda usati nei documenti e nella fattura elettronica."""
    __tablename__ = "app_settings"
    id = Column(Integer, primary_key=True)
    company_name = Column(String, default="")
    company_vat = Column(String, default="")
    company_tax_code = Column(String, default="")
    company_address = Column(String, default="")
    company_zip = Column(String, default="")
    company_city = Column(String, default="")
    company_email = Column(String, default="")
    company_phone = Column(String, default="")
    iban = Column(String, default="")
    company_province = Column(String, default="")
    company_regime = Column(String, default="RF01")  # regime fiscale FatturaPA
    default_tax_rate = Column(Float, default=22)
    default_payment_days = Column(Integer, default=30)  # scadenza predefinita dei documenti


# =========================
# SCHEMAS
# =========================

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(ORMModel):
    id: int
    username: str
    email: str
    role: str
    active: bool


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class ClientCreate(BaseModel):
    name: str
    code: Optional[str] = ""
    client_type: Optional[str] = "Privato"
    vat: Optional[str] = ""
    tax_code: Optional[str] = ""
    referente: Optional[str] = ""
    email: Optional[str] = ""
    pec: Optional[str] = ""
    phone: Optional[str] = ""
    mobile: Optional[str] = ""
    address: Optional[str] = ""
    zip: Optional[str] = ""
    city: Optional[str] = ""
    province: Optional[str] = ""
    country: Optional[str] = "Italia"
    ship_to: Optional[str] = ""
    iban: Optional[str] = ""
    payment_terms: Optional[str] = ""
    discount: float = Field(0, ge=0, le=100)
    website: Optional[str] = ""
    secondary_phone: Optional[str] = ""
    sdi_code: Optional[str] = ""
    active: Optional[bool] = True
    notes: Optional[str] = ""


class ClientUpdate(ClientCreate):
    pass


class ClientOut(ORMModel):
    id: int
    code: str
    name: str
    client_type: str
    vat: str
    tax_code: str
    referente: str
    email: str
    pec: str
    phone: str
    mobile: str
    address: str
    zip: str
    city: str
    province: str
    country: str
    ship_to: str
    iban: str
    payment_terms: str
    discount: float
    website: str
    secondary_phone: str
    sdi_code: str
    active: bool
    notes: str


class BoatCreate(BaseModel):
    client_id: int
    name: str
    registration: Optional[str] = ""
    boat_type: Optional[str] = ""
    length: Optional[float] = None
    engine: Optional[str] = ""
    build_year: Optional[int] = None
    hull_id: Optional[str] = ""
    insurance_expiry: Optional[Date] = None
    notes: Optional[str] = ""
    builder: Optional[str] = ""
    model: Optional[str] = ""
    hull_material: Optional[str] = ""
    beam: Optional[float] = None
    draft: Optional[float] = None
    displacement: Optional[float] = None
    engine_make: Optional[str] = ""
    engine_model: Optional[str] = ""
    engine_power_hp: Optional[float] = None
    engine_hours: Optional[float] = None
    fuel_type: Optional[str] = ""
    flag: Optional[str] = ""
    home_port: Optional[str] = ""
    insurance_company: Optional[str] = ""
    last_haul_out: Optional[Date] = None
    next_service_date: Optional[Date] = None
    yard_position: Optional[str] = ""


class BoatUpdate(BoatCreate):
    pass


class BoatOut(ORMModel):
    id: int
    client_id: int
    name: str
    registration: str
    boat_type: str
    length: Optional[float]
    engine: str
    build_year: Optional[int]
    hull_id: str
    insurance_expiry: Optional[Date]
    notes: str
    builder: str
    model: str
    hull_material: str
    beam: Optional[float]
    draft: Optional[float]
    displacement: Optional[float]
    engine_make: str
    engine_model: str
    engine_power_hp: Optional[float]
    engine_hours: Optional[float]
    fuel_type: str
    flag: str
    home_port: str
    insurance_company: str
    last_haul_out: Optional[Date]
    next_service_date: Optional[Date]
    yard_position: str


class WarehouseCreate(BaseModel):
    code: str
    name: str


class WarehouseOut(ORMModel):
    id: int
    code: str
    name: str


class ItemCreate(BaseModel):
    sku: Optional[str] = ""
    name: str
    category: Optional[str] = ""
    unit: Optional[str] = "pz"
    cost: float = Field(0, ge=0)
    price: float = Field(0, ge=0)
    min_stock: float = Field(0, ge=0)


class ItemUpdate(ItemCreate):
    pass


class ItemOut(ORMModel):
    id: int
    sku: str
    name: str
    category: str
    unit: str
    cost: float
    price: float
    min_stock: float


class MovementCreate(BaseModel):
    warehouse_id: int
    item_id: int
    type: str  # carico, scarico, reso
    qty: float = Field(gt=0)
    unit_cost: Optional[float] = Field(None, ge=0)  # vuoto = costo medio dell'articolo
    note: Optional[str] = ""
    project_id: Optional[int] = None  # commessa di riferimento (opzionale)


class MovementOut(ORMModel):
    id: int
    date: Date
    warehouse_id: int
    item_id: int
    type: str
    qty: float
    unit_cost: float
    note: str


class ProjectCreate(BaseModel):
    client_id: int
    boat_id: Optional[int] = None
    title: str
    status: Optional[str] = "aperta"
    start_date: Optional[Date] = None
    due_date: Optional[Date] = None
    notes: Optional[str] = ""


class ProjectUpdate(ProjectCreate):
    pass


class ProjectOut(ORMModel):
    id: int
    number: str
    client_id: int
    boat_id: Optional[int]
    title: str
    status: str
    start_date: Optional[Date]
    due_date: Optional[Date]
    notes: str


class JobCreate(BaseModel):
    description: str
    category: Optional[str] = "Manodopera"
    status: Optional[str] = "Da fare"
    priority: Optional[str] = "normale"
    qty: float = Field(1, ge=0)
    unit: Optional[str] = "pz"
    unit_cost: float = Field(0, ge=0)
    unit_price: float = Field(0, ge=0)
    assigned_to: Optional[str] = ""


class JobUpdate(JobCreate):
    pass


class JobOut(ORMModel):
    id: int
    project_id: int
    description: str
    category: str
    status: str
    priority: str
    qty: float
    unit: str
    unit_cost: float
    unit_price: float
    assigned_to: str


class AttachmentOut(ORMModel):
    id: int
    project_id: int
    filename: str
    content_type: str
    file_size: int
    created_at: datetime


class DocumentLineCreate(BaseModel):
    description: str = Field(min_length=1)
    qty: float = Field(1, ge=0)
    price: float = Field(0, ge=0)
    unit: Optional[str] = ""


class DocumentLineOut(ORMModel):
    id: int
    description: str
    qty: float
    price: float
    unit: str


class DocumentCreate(BaseModel):
    kind: str  # DDT, Proforma, Fattura
    client_id: int
    project_id: Optional[int] = None
    date: Optional[Date] = None
    due_date: Optional[Date] = None
    status: Optional[str] = "bozza"
    tax_rate: Optional[float] = Field(None, ge=0, le=100)  # vuoto = aliquota predefinita
    vat_nature: Optional[str] = ""
    discount: float = Field(0, ge=0)
    discount_pct: Optional[float] = Field(None, ge=0, le=100)  # vuoto = sconto abituale del cliente
    due_date_auto: bool = True
    notes: Optional[str] = ""

    ddt_reason: Optional[str] = ""
    ddt_carrier: Optional[str] = ""
    ddt_destination: Optional[str] = ""
    ddt_parcels: Optional[int] = None
    ddt_weight: Optional[float] = None

    lines: List[DocumentLineCreate] = []


class DocumentOut(ORMModel):
    id: int
    kind: str
    number: str
    date: Date
    due_date: Optional[Date]
    client_id: int
    project_id: Optional[int]
    source_document_id: Optional[int]
    status: str
    tax_rate: float
    vat_nature: str = ""
    discount: float
    discount_pct: float = 0
    total: float = 0
    paid: float = 0
    residual: float = 0
    notes: str
    ddt_reason: str
    ddt_carrier: str
    ddt_destination: str
    ddt_parcels: Optional[int]
    ddt_weight: Optional[float]
    xml_path: str
    created_by: str
    created_at: datetime
    lines: List[DocumentLineOut] = []


class DocumentUpdate(BaseModel):
    """Modifica intestazione documento: None = campo non toccato."""
    client_id: Optional[int] = None
    project_id: Optional[int] = None
    date: Optional[Date] = None
    due_date: Optional[Date] = None
    discount: Optional[float] = Field(None, ge=0)
    discount_pct: Optional[float] = Field(None, ge=0, le=100)
    tax_rate: Optional[float] = Field(None, ge=0, le=100)
    vat_nature: Optional[str] = None
    notes: Optional[str] = None

    ddt_reason: Optional[str] = None
    ddt_carrier: Optional[str] = None
    ddt_destination: Optional[str] = None
    ddt_parcels: Optional[int] = None
    ddt_weight: Optional[float] = None


class PaymentCreate(BaseModel):
    amount: float = Field(gt=0)
    date: Optional[Date] = None
    method: Optional[str] = "bonifico"
    note: Optional[str] = ""


class PaymentOut(ORMModel):
    id: int
    document_id: int
    date: Date
    amount: float
    method: str
    note: str


class SettingsUpdate(BaseModel):
    company_name: Optional[str] = ""
    company_vat: Optional[str] = ""
    company_tax_code: Optional[str] = ""
    company_address: Optional[str] = ""
    company_zip: Optional[str] = ""
    company_city: Optional[str] = ""
    company_email: Optional[str] = ""
    company_phone: Optional[str] = ""
    iban: Optional[str] = ""
    company_province: Optional[str] = ""
    company_regime: Optional[str] = "RF01"
    default_tax_rate: float = Field(22, ge=0, le=100)
    default_payment_days: int = Field(30, ge=0, le=365)


class SettingsOut(ORMModel):
    id: int
    company_name: str
    company_vat: str
    company_tax_code: str
    company_address: str
    company_zip: str
    company_city: str
    company_email: str
    company_phone: str
    iban: str
    company_province: str = ""
    company_regime: str = "RF01"
    default_tax_rate: float = 22
    default_payment_days: int = 30


class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"
    email: Optional[str] = ""


class UserUpdate(BaseModel):
    role: Optional[str] = None
    active: Optional[bool] = None
    email: Optional[str] = None


class UserSetPassword(BaseModel):
    new_password: str


class ArchiveFolderCreate(BaseModel):
    name: str
    description: Optional[str] = ""


class ArchiveFolderOut(ORMModel):
    id: int
    name: str
    description: str
    file_count: int = 0


class ArchiveFileCreate(BaseModel):
    folder_id: int
    notes: Optional[str] = ""


class ArchiveFileOut(ORMModel):
    id: int
    folder_id: int
    filename: str
    content_type: str
    file_size: int
    notes: str
    created_at: datetime


class SupplierCreate(BaseModel):
    name: str
    vat: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    address: Optional[str] = ""
    notes: Optional[str] = ""


class SupplierOut(ORMModel):
    id: int
    name: str
    vat: str
    email: str
    phone: str
    address: str
    notes: str


class PurchaseInvoiceCreate(BaseModel):
    supplier_id: int
    number: Optional[str] = ""
    date: Optional[Date] = None
    due_date: Optional[Date] = None
    amount_net: float = Field(gt=0)
    vat_rate: float = Field(22, ge=0, le=100)
    status: Optional[str] = "da_pagare"
    paid_date: Optional[Date] = None
    notes: Optional[str] = ""


class PurchaseInvoiceOut(ORMModel):
    id: int
    supplier_id: int
    supplier_name: str = ""
    number: str
    date: Date
    due_date: Optional[Date]
    amount_net: float
    vat_rate: float
    status: str
    paid_date: Optional[Date]
    notes: str
    vat: float = 0
    total: float = 0


class ResourceCreate(BaseModel):
    name: str
    rtype: Optional[str] = "Postazione"
    notes: Optional[str] = ""


class ResourceOut(ORMModel):
    id: int
    name: str
    rtype: str
    notes: str


class BookingCreate(BaseModel):
    resource_id: int
    project_id: Optional[int] = None
    boat_id: Optional[int] = None
    title: str
    start_date: Date
    end_date: Date
    status: Optional[str] = "pianificato"
    notes: Optional[str] = ""


class BookingOut(ORMModel):
    id: int
    resource_id: int
    resource_name: str = ""
    project_id: Optional[int]
    project_number: str = ""
    boat_id: Optional[int]
    boat_name: str = ""
    title: str
    start_date: Date
    end_date: Date
    status: str
    notes: str


class TimeEntryCreate(BaseModel):
    job_id: Optional[int] = None
    worker: Optional[str] = ""
    worker_id: Optional[int] = None
    hourly_cost: Optional[float] = Field(None, ge=0)   # se non dato, tariffa del lavoratore
    hourly_price: Optional[float] = Field(None, ge=0)
    date: Optional[Date] = None
    hours: float = Field(gt=0, le=24)
    notes: Optional[str] = ""


class TimeEntryOut(ORMModel):
    id: int
    project_id: int
    job_id: Optional[int]
    job_description: str = ""
    worker: str
    worker_id: Optional[int]
    worker_name: str = ""
    hourly_cost: float
    hourly_price: float
    date: Date
    hours: float
    notes: str


class WorkerCreate(BaseModel):
    name: str
    role: Optional[str] = ""
    hourly_cost: float = Field(0, ge=0)
    hourly_price: float = Field(0, ge=0)
    active: Optional[bool] = True
    notes: Optional[str] = ""
    employee_code: Optional[str] = ""
    birth_date: Optional[Date] = None
    phone: Optional[str] = ""
    email: Optional[str] = ""
    iban: Optional[str] = ""
    hire_date: Optional[Date] = None
    contract_type: Optional[str] = ""
    weekly_hours: Optional[float] = None
    vacation_days: Optional[float] = None
    license: Optional[str] = ""
    license_expiry: Optional[Date] = None
    medical_exam_expiry: Optional[Date] = None
    safety_training_expiry: Optional[Date] = None
    skills: Optional[str] = ""
    certifications: Optional[str] = ""
    emergency_contact: Optional[str] = ""
    emergency_phone: Optional[str] = ""


class WorkerOut(ORMModel):
    id: int
    name: str
    role: str
    hourly_cost: float
    hourly_price: float
    active: bool
    notes: str
    employee_code: str
    birth_date: Optional[Date]
    phone: str
    email: str
    iban: str
    hire_date: Optional[Date]
    contract_type: str
    weekly_hours: Optional[float]
    vacation_days: Optional[float]
    license: str
    license_expiry: Optional[Date]
    medical_exam_expiry: Optional[Date]
    safety_training_expiry: Optional[Date]
    skills: str
    certifications: str
    emergency_contact: str
    emergency_phone: str


class LookupCreate(BaseModel):
    category: str
    value: str


class LookupOut(ORMModel):
    id: int
    category: str
    value: str
    sort_order: int


class PurchaseOrderLineCreate(BaseModel):
    item_id: Optional[int] = None
    description: str
    qty: float = Field(1, gt=0)
    unit_cost: float = Field(0, ge=0)


class PurchaseOrderLineOut(ORMModel):
    id: int
    item_id: Optional[int]
    item_name: str = ""
    description: str
    qty: float
    unit_cost: float


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    date: Optional[Date] = None
    expected_date: Optional[Date] = None
    status: Optional[str] = "bozza"
    notes: Optional[str] = ""
    lines: List[PurchaseOrderLineCreate] = []


class PurchaseOrderOut(ORMModel):
    id: int
    number: str
    supplier_id: int
    supplier_name: str = ""
    date: Date
    expected_date: Optional[Date]
    status: str
    notes: str
    lines: List[PurchaseOrderLineOut] = []


# =========================
# AUTH (hash PBKDF2 della libreria standard: nessuna dipendenza binaria)
# =========================

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import Response, FileResponse
from jose import jwt, JWTError

PBKDF2_ITERATIONS = 390_000
MIN_PASSWORD = 8


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${digest.hex()}"


def verify_password(plain: str, hashed: str) -> bool:
    try:
        scheme, iterations, salt, expected = hashed.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt.encode("utf-8"), int(iterations))
        return secrets.compare_digest(digest.hex(), expected)
    except (ValueError, AttributeError):
        return False


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenziali non valide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None or not user.active:
        raise credentials_exception
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permesso richiesto: admin")
    return current_user


def require_manager(current_user: User = Depends(get_current_user)) -> User:
    """Operazioni distruttive o amministrative: admin e manager (non gli operatori)."""
    if current_user.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Operazione riservata a manager e amministratori")
    return current_user


# =========================
# HELPERS
# =========================


def get_settings(db: Session) -> AppSettings:
    settings = db.get(AppSettings, 1)
    if not settings:
        settings = AppSettings(id=1, **DEFAULT_COMPANY)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


def get_or_create_stock(db: Session, warehouse_id: int, item_id: int) -> Stock:
    stock = db.query(Stock).filter(
        Stock.warehouse_id == warehouse_id,
        Stock.item_id == item_id
    ).first()

    if not stock:
        stock = Stock(warehouse_id=warehouse_id, item_id=item_id, qty=0)
        db.add(stock)
        db.flush()

    return stock


def apply_average_cost(db: Session, item: Item, qty, unit_cost):
    """Costo medio ponderato dell'articolo: a ogni carico con costo noto si
    ricalcola in base alla giacenza totale (tutti i magazzini) già presente."""
    unit_cost = D(unit_cost)
    if unit_cost <= 0 or D(qty) <= 0:
        return
    on_hand = D(db.query(SQLFunc.sum(Stock.qty)).filter(Stock.item_id == item.id).scalar() or 0)
    on_hand = max(on_hand, Decimal(0))
    new_total = on_hand + D(qty)
    item.cost = float(((on_hand * D(item.cost) + D(qty) * unit_cost) / new_total).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def next_project_number(db: Session) -> str:
    return _next_number(db, Project, f"COMM-{Date.today().year}-")


def next_document_number(db: Session, kind: str) -> str:
    prefixes = {
        "DDT": "DDT",
        "Proforma": "PRO",
        "Fattura": "FT",
    }
    if kind not in prefixes:
        raise HTTPException(status_code=400, detail="Tipo documento non valido")

    return _next_number(db, Document, f"{prefixes[kind]}-{Date.today().year}-")


def document_totals(doc: Document) -> dict:
    """Totali del documento. Ogni riga è arrotondata al centesimo; lo sconto
    (percentuale + euro) non può superare il subtotale; l'IVA è calcolata
    sull'imponibile e arrotondata una sola volta."""
    subtotal = sum((r2(D(l.qty) * D(l.price)) for l in doc.lines), Decimal(0))
    pct = min(max(D(doc.discount_pct), Decimal(0)), Decimal(100))
    discount = min(r2(subtotal * pct / 100) + r2(doc.discount), subtotal)
    taxable = subtotal - discount
    tax = r2(taxable * D(doc.tax_rate) / 100)
    total = taxable + tax
    paid = sum((r2(p.amount) for p in doc.payments), Decimal(0))
    return {
        "subtotal": float(subtotal),
        "discount_amount": float(discount),
        "taxable": float(taxable),
        "tax": float(tax),
        "total": float(total),
        "paid": float(paid),
        "residual": float(total - paid),
    }


def _next_number(db: Session, model, prefix: str) -> str:
    """Prossimo numero progressivo per prefisso (es. FT-2026-): parte dal
    massimo esistente, così eliminare un documento non genera mai duplicati."""
    last = 0
    for (number,) in db.query(model.number).filter(model.number.like(f"{prefix}%")).all():
        tail = (number or "")[len(prefix):]
        if tail.isdigit():
            last = max(last, int(tail))
    return f"{prefix}{last + 1:05d}"


def valid_partita_iva(vat: str) -> bool:
    """Controlla formato e cifra di controllo di una partita IVA italiana."""
    vat = (vat or "").strip()
    if len(vat) != 11 or not vat.isdigit() or vat == "0" * 11:
        return False
    total = 0
    for i, ch in enumerate(vat[:10]):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return (10 - total % 10) % 10 == int(vat[10])


VAT_NATURES = {
    "N1": "Escluse ex art. 15",
    "N2.1": "Non soggette ad IVA - artt. da 7 a 7-septies",
    "N2.2": "Non soggette - altri casi",
    "N3.1": "Non imponibili - esportazioni",
    "N3.2": "Non imponibili - cessioni intracomunitarie",
    "N3.4": "Non imponibili - operazioni assimilate alle cessioni all'esportazione (art. 8-bis)",
    "N3.5": "Non imponibili - a seguito di dichiarazioni d'intento",
    "N4": "Esenti",
    "N6.9": "Inversione contabile - altri casi",
    "N7": "IVA assolta in altro stato UE",
}


def _xml_text(value, limit: int = 1000) -> str:
    """Testo sicuro per XML: niente caratteri di controllo, lunghezza limitata."""
    clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", str(value or "")).strip()
    return escape(clean[:limit])


def _num_xml(value, min_dec: int = 2, max_dec: int = 8) -> str:
    text = f"{D(value):.{max_dec}f}".rstrip("0")
    whole, _, frac = text.partition(".")
    return f"{whole}.{frac.ljust(min_dec, '0')}"


def check_invoice_ready(db: Session, doc: Document) -> List[str]:
    """Elenco dei dati mancanti per poter emettere/esportare la fattura elettronica."""
    problems = []
    settings = get_settings(db)
    client = db.get(Client, doc.client_id)
    company_vat = (settings.company_vat or "").replace(" ", "").upper().removeprefix("IT")
    if not valid_partita_iva(company_vat):
        problems.append("P.IVA dell'azienda mancante o non valida (Impostazioni)")
    if not (settings.company_address and settings.company_zip and settings.company_city):
        problems.append("Indirizzo, CAP e città dell'azienda (Impostazioni)")
    if not client:
        problems.append("Cliente non trovato")
    else:
        vat = (client.vat or "").replace(" ", "").upper().removeprefix("IT")
        if not vat and not (client.tax_code or "").strip():
            problems.append(f"{client.name}: serve partita IVA o codice fiscale")
        if vat and not valid_partita_iva(vat):
            problems.append(f"{client.name}: partita IVA non valida")
        if not (client.address and client.zip and client.city):
            problems.append(f"{client.name}: indirizzo, CAP e città")
    if not doc.lines:
        problems.append("Il documento non ha righe")
    elif document_totals(doc)["total"] <= 0:
        problems.append("Il totale del documento deve essere maggiore di zero")
    if not doc.tax_rate and doc.vat_nature not in VAT_NATURES:
        problems.append("IVA 0%: indica la natura dell'operazione (es. N3.4)")
    return problems


def generate_fattura_xml(db: Session, doc: Document) -> str:
    client = db.get(Client, doc.client_id)
    if not client:
        raise HTTPException(status_code=400, detail="Cliente non trovato")
    problems = check_invoice_ready(db, doc)
    if problems:
        raise HTTPException(status_code=400, detail="Fattura elettronica incompleta: " + "; ".join(problems))

    settings = get_settings(db)
    totals = document_totals(doc)
    rate = D(doc.tax_rate)
    nature = "" if rate else f"<Natura>{doc.vat_nature}</Natura>"

    company_vat = (settings.company_vat or "").replace(" ", "").upper().removeprefix("IT")
    client_vat = (client.vat or "").replace(" ", "").upper().removeprefix("IT")
    client_tax_code = (client.tax_code or "").replace(" ", "").upper()

    fiscale = ""
    if client_vat:
        fiscale += f"<IdFiscaleIVA><IdPaese>IT</IdPaese><IdCodice>{escape(client_vat)}</IdCodice></IdFiscaleIVA>"
    if client_tax_code:
        fiscale += f"<CodiceFiscale>{escape(client_tax_code)}</CodiceFiscale>"

    # Codice destinatario: SdI a 7 caratteri; P.A. a 6; altrimenti 0000000 (+ PEC)
    sdi = (client.sdi_code or "").strip().upper()
    pa = client.client_type == "P.A."
    if pa and len(sdi) == 6:
        formato, dest = "FPA12", sdi
    else:
        formato, dest = "FPR12", sdi if len(sdi) == 7 else "0000000"
    pec = f"<PECDestinatario>{_xml_text(client.pec, 256)}</PECDestinatario>" if dest == "0000000" and client.pec else ""

    lines = []
    num = 0
    for line in doc.lines:
        num += 1
        lines.append(f"""
      <DettaglioLinee>
        <NumeroLinea>{num}</NumeroLinea>
        <Descrizione>{_xml_text(line.description)}</Descrizione>
        <Quantita>{_num_xml(line.qty)}</Quantita>{f"<UnitaMisura>{_xml_text(line.unit, 10)}</UnitaMisura>" if line.unit else ""}
        <PrezzoUnitario>{_num_xml(line.price)}</PrezzoUnitario>
        <PrezzoTotale>{r2(D(line.qty) * D(line.price))}</PrezzoTotale>
        <AliquotaIVA>{rate:.2f}</AliquotaIVA>{nature}
      </DettaglioLinee>""")
    if totals["discount_amount"]:
        num += 1
        lines.append(f"""
      <DettaglioLinee>
        <NumeroLinea>{num}</NumeroLinea>
        <Descrizione>Sconto</Descrizione>
        <Quantita>1.00</Quantita>
        <PrezzoUnitario>-{r2(totals['discount_amount'])}</PrezzoUnitario>
        <PrezzoTotale>-{r2(totals['discount_amount'])}</PrezzoTotale>
        <AliquotaIVA>{rate:.2f}</AliquotaIVA>{nature}
      </DettaglioLinee>""")

    riepilogo = f"""
      <DatiRiepilogo>
        <AliquotaIVA>{rate:.2f}</AliquotaIVA>{nature}
        <ImponibileImporto>{r2(totals['taxable'])}</ImponibileImporto>
        <Imposta>{r2(totals['tax'])}</Imposta>
        <EsigibilitaIVA>I</EsigibilitaIVA>
      </DatiRiepilogo>"""

    iban = (settings.iban or "").replace(" ", "").upper()
    due = doc.due_date
    pagamento = f"""
    <DatiPagamento>
      <CondizioniPagamento>TP02</CondizioniPagamento>
      <DettaglioPagamento>
        <ModalitaPagamento>{"MP05" if iban else "MP01"}</ModalitaPagamento>{f"<DataScadenzaPagamento>{due.isoformat()}</DataScadenzaPagamento>" if due else ""}
        <ImportoPagamento>{r2(totals['total'])}</ImportoPagamento>{f"<IBAN>{escape(iban)}</IBAN>" if iban else ""}
      </DettaglioPagamento>
    </DatiPagamento>"""

    causale = f"<Causale>{_xml_text(doc.notes, 200)}</Causale>" if doc.notes else ""
    c_prov = (client.province or "").strip().upper()[:2]
    s_prov = (settings.company_province or "").strip().upper()[:2]

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<p:FatturaElettronica
  xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
  xmlns:p="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  versione="{formato}">
  <FatturaElettronicaHeader>
    <DatiTrasmissione>
      <IdTrasmittente><IdPaese>IT</IdPaese><IdCodice>{escape(company_vat)}</IdCodice></IdTrasmittente>
      <ProgressivoInvio>{doc.id}</ProgressivoInvio>
      <FormatoTrasmissione>{formato}</FormatoTrasmissione>
      <CodiceDestinatario>{dest}</CodiceDestinatario>{pec}
    </DatiTrasmissione>
    <CedentePrestatore>
      <DatiAnagrafici>
        <IdFiscaleIVA><IdPaese>IT</IdPaese><IdCodice>{escape(company_vat)}</IdCodice></IdFiscaleIVA>{f"<CodiceFiscale>{_xml_text(settings.company_tax_code, 16)}</CodiceFiscale>" if settings.company_tax_code else ""}
        <Anagrafica><Denominazione>{_xml_text(settings.company_name, 80)}</Denominazione></Anagrafica>
        <RegimeFiscale>{_xml_text(settings.company_regime or "RF01", 4)}</RegimeFiscale>
      </DatiAnagrafici>
      <Sede>
        <Indirizzo>{_xml_text(settings.company_address, 60)}</Indirizzo>
        <CAP>{_xml_text(settings.company_zip, 5)}</CAP>
        <Comune>{_xml_text(settings.company_city, 60)}</Comune>{f"<Provincia>{s_prov}</Provincia>" if len(s_prov) == 2 else ""}
        <Nazione>IT</Nazione>
      </Sede>
    </CedentePrestatore>
    <CessionarioCommittente>
      <DatiAnagrafici>
        {fiscale}
        <Anagrafica><Denominazione>{_xml_text(client.name, 80)}</Denominazione></Anagrafica>
      </DatiAnagrafici>
      <Sede>
        <Indirizzo>{_xml_text(client.address, 60)}</Indirizzo>
        <CAP>{_xml_text(client.zip, 5)}</CAP>
        <Comune>{_xml_text(client.city, 60)}</Comune>{f"<Provincia>{c_prov}</Provincia>" if len(c_prov) == 2 else ""}
        <Nazione>IT</Nazione>
      </Sede>
    </CessionarioCommittente>
  </FatturaElettronicaHeader>
  <FatturaElettronicaBody>
    <DatiGenerali>
      <DatiGeneraliDocumento>
        <TipoDocumento>TD01</TipoDocumento>
        <Divisa>EUR</Divisa>
        <Data>{doc.date.isoformat()}</Data>
        <Numero>{_xml_text(doc.number, 20)}</Numero>
        <ImportoTotaleDocumento>{r2(totals['total'])}</ImportoTotaleDocumento>{causale}
      </DatiGeneraliDocumento>
    </DatiGenerali>
    <DatiBeniServizi>{"".join(lines)}{riepilogo}
    </DatiBeniServizi>{pagamento}
  </FatturaElettronicaBody>
</p:FatturaElettronica>
"""


MAX_UPLOAD_MB = 100


def save_upload(upload: UploadFile, dest: str) -> int:
    """Salva un file caricato a blocchi, con limite di dimensione. Ritorna i byte scritti."""
    limit = MAX_UPLOAD_MB * 1024 * 1024
    size = 0
    try:
        with open(dest, "wb") as out:
            while True:
                chunk = upload.file.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > limit:
                    raise HTTPException(status_code=413, detail=f"File troppo grande (massimo {MAX_UPLOAD_MB} MB)")
                out.write(chunk)
    except Exception:
        try:
            os.remove(dest)
        except OSError:
            pass
        raise
    return size


def resolve_stored_path(stored: str) -> str:
    """Percorso reale di un file caricato. Se la cartella dati è stata spostata
    (copia dell'app su un altro disco) ricostruisce il percorso da `uploads/`."""
    if stored and os.path.exists(stored):
        return stored
    norm = (stored or "").replace("\\", "/")
    if "/uploads/" in norm:
        candidate = os.path.join(UPLOAD_DIR, norm.split("/uploads/", 1)[1])
        if os.path.exists(candidate):
            return candidate
    return stored


def sanitize_filename(name: str) -> str:
    name = os.path.basename(name or "").strip()
    name = name.replace("\\", "_")
    return re.sub(r"[^\w.\- ()]", "_", name) or "allegato"


# =========================
# APP
# =========================

from sqlalchemy import text as SQLText

app = FastAPI(title="Cantiere Navale Pro", version="2.4")

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "same-origin")
    if request.url.path.startswith("/static/") or request.url.path == "/":
        response.headers.setdefault("Cache-Control", "no-cache")
    return response


_FIELD_LABELS = {
    "qty": "quantità", "price": "prezzo", "amount": "importo", "hours": "ore",
    "tax_rate": "IVA", "discount": "sconto", "discount_pct": "sconto %", "unit_cost": "costo unitario",
    "cost": "costo", "amount_net": "imponibile", "name": "nome", "description": "descrizione",
}


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request, exc: RequestValidationError):
    """Errori di validazione leggibili (il frontend mostra `detail` come testo)."""
    messages = []
    for err in exc.errors():
        field = str(err["loc"][-1]) if err.get("loc") else "campo"
        label = _FIELD_LABELS.get(field, field)
        kind = err.get("type", "")
        if kind == "missing":
            messages.append(f"{label}: campo obbligatorio")
        elif kind in ("greater_than", "greater_than_equal"):
            messages.append(f"{label}: valore troppo basso (minimo {err.get('ctx', {}).get('ge', err.get('ctx', {}).get('gt', 0))})")
        elif kind in ("less_than", "less_than_equal"):
            messages.append(f"{label}: valore troppo alto (massimo {err.get('ctx', {}).get('le', err.get('ctx', {}).get('lt', ''))})")
        elif kind == "string_too_short":
            messages.append(f"{label}: campo obbligatorio")
        else:
            messages.append(f"{label}: valore non valido")
    return JSONResponse(status_code=422, content={"detail": "; ".join(messages) or "Dati non validi"})


# Colonne aggiunte nelle versioni recenti: chi apre un vecchio database
# lo aggiorna automaticamente senza perdere dati.
_MIGRATIONS = {
    "clients": [
        ("code", "VARCHAR DEFAULT ''"),
        ("client_type", "VARCHAR DEFAULT 'Privato'"),
        ("referente", "VARCHAR DEFAULT ''"),
        ("pec", "VARCHAR DEFAULT ''"),
        ("mobile", "VARCHAR DEFAULT ''"),
        ("zip", "VARCHAR DEFAULT ''"),
        ("city", "VARCHAR DEFAULT ''"),
        ("province", "VARCHAR DEFAULT ''"),
        ("country", "VARCHAR DEFAULT 'Italia'"),
        ("ship_to", "VARCHAR DEFAULT ''"),
        ("iban", "VARCHAR DEFAULT ''"),
        ("payment_terms", "VARCHAR DEFAULT ''"),
        ("discount", "FLOAT DEFAULT 0"),
        ("active", "BOOLEAN DEFAULT 1"),
        ("notes", "VARCHAR DEFAULT ''"),
        ("created_at", "DATETIME"),
        ("website", "VARCHAR DEFAULT ''"),
        ("secondary_phone", "VARCHAR DEFAULT ''"),
        ("sdi_code", "VARCHAR DEFAULT ''"),
    ],
    "boats": [
        ("length", "FLOAT"),
        ("engine", "VARCHAR DEFAULT ''"),
        ("build_year", "INTEGER"),
        ("hull_id", "VARCHAR DEFAULT ''"),
        ("insurance_expiry", "DATE"),
        ("notes", "VARCHAR DEFAULT ''"),
        ("builder", "VARCHAR DEFAULT ''"),
        ("model", "VARCHAR DEFAULT ''"),
        ("hull_material", "VARCHAR DEFAULT ''"),
        ("beam", "FLOAT"),
        ("draft", "FLOAT"),
        ("displacement", "FLOAT"),
        ("engine_make", "VARCHAR DEFAULT ''"),
        ("engine_model", "VARCHAR DEFAULT ''"),
        ("engine_power_hp", "FLOAT"),
        ("engine_hours", "FLOAT"),
        ("fuel_type", "VARCHAR DEFAULT ''"),
        ("flag", "VARCHAR DEFAULT ''"),
        ("home_port", "VARCHAR DEFAULT ''"),
        ("insurance_company", "VARCHAR DEFAULT ''"),
        ("last_haul_out", "DATE"),
        ("next_service_date", "DATE"),
        ("yard_position", "VARCHAR DEFAULT ''"),
    ],
    "workers": [
        ("employee_code", "VARCHAR DEFAULT ''"),
        ("birth_date", "DATE"),
        ("phone", "VARCHAR DEFAULT ''"),
        ("email", "VARCHAR DEFAULT ''"),
        ("iban", "VARCHAR DEFAULT ''"),
        ("hire_date", "DATE"),
        ("contract_type", "VARCHAR DEFAULT ''"),
        ("weekly_hours", "FLOAT"),
        ("vacation_days", "FLOAT"),
        ("license", "VARCHAR DEFAULT ''"),
        ("license_expiry", "DATE"),
        ("medical_exam_expiry", "DATE"),
        ("safety_training_expiry", "DATE"),
        ("skills", "VARCHAR DEFAULT ''"),
        ("certifications", "VARCHAR DEFAULT ''"),
        ("emergency_contact", "VARCHAR DEFAULT ''"),
        ("emergency_phone", "VARCHAR DEFAULT ''"),
    ],
    "jobs": [
        ("priority", "VARCHAR DEFAULT 'normale'"),
    ],
    "documents": [
        ("created_by", "VARCHAR DEFAULT ''"),
        ("discount_pct", "FLOAT DEFAULT 0"),
        ("vat_nature", "VARCHAR DEFAULT ''"),
    ],
    "app_settings": [
        ("company_province", "VARCHAR DEFAULT ''"),
        ("company_regime", "VARCHAR DEFAULT 'RF01'"),
        ("default_tax_rate", "FLOAT DEFAULT 22"),
        ("default_payment_days", "INTEGER DEFAULT 30"),
    ],
    "document_lines": [
        ("unit", "VARCHAR DEFAULT ''"),
    ],
    "movements": [
        ("project_id", "INTEGER"),
    ],
    "items": [
        ("min_stock", "FLOAT DEFAULT 0"),
    ],
    "time_entries": [
        ("worker_id", "INTEGER"),
        ("hourly_cost", "FLOAT DEFAULT 0"),
        ("hourly_price", "FLOAT DEFAULT 0"),
    ],
}


def migrate_schema():
    if not DATABASE_URL.startswith("sqlite"):
        return
    with engine.begin() as conn:
        for table, columns in _MIGRATIONS.items():
            rows = conn.execute(SQLText(f"PRAGMA table_info({table})")).fetchall()
            if not rows:
                continue  # tabella creata ex novo da create_all
            existing = {r[1] for r in rows}
            for col, ddl in columns:
                if col not in existing:
                    conn.execute(SQLText(f"ALTER TABLE {table} ADD COLUMN {col} {ddl}"))


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    migrate_schema()
    db = SessionLocal()

    try:
        if not db.query(User).filter(User.username == ADMIN_USERNAME).first():
            db.add(User(
                username=ADMIN_USERNAME,
                email="",
                hashed_password=hash_password(ADMIN_PASSWORD),
                role="admin",
                active=True
            ))

        if not db.query(Warehouse).first():
            db.add(Warehouse(code="MAIN", name="Magazzino principale"))

        if not db.query(ArchiveFolder).first():
            for name, desc in [
                ("Contratti", "Contratti con clienti e fornitori"),
                ("Certificati", "Certificati di conformità e navigabilità"),
                ("Assicurazioni", "Polizze di imbarcazioni e responsabilità civile"),
                ("Pratiche", "Pratiche portuali e amministrative"),
                ("Fatture ricevute", "Documenti dei fornitori"),
                ("Varie", ""),
            ]:
                db.add(ArchiveFolder(name=name, description=desc))

        # tendine configurabili: seed solo alla prima apertura (tabella vuota)
        if not db.query(LookupOption).first():
            for cat, values in DEFAULT_LOOKUPS.items():
                for i, v in enumerate(values):
                    db.add(LookupOption(category=cat, value=v, sort_order=i))

        get_settings(db)
        db.commit()

        if DATABASE_URL.startswith("sqlite"):
            threading.Thread(target=_backup_loop, daemon=True).start()

        if OPEN_BROWSER:
            url = f"http://127.0.0.1:{PORT}"
            threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    finally:
        db.close()


# =========================
# AUTH ROUTES
# =========================

_LOGIN_FAILS: dict = {}
_LOGIN_MAX_FAILS = 5
_LOGIN_WINDOW = 300  # secondi


def _login_blocked(key: str) -> int:
    """Secondi residui di blocco per questo utente (0 = libero)."""
    now = datetime.now().timestamp()
    fails = [t for t in _LOGIN_FAILS.get(key, []) if now - t < _LOGIN_WINDOW]
    _LOGIN_FAILS[key] = fails
    if len(fails) >= _LOGIN_MAX_FAILS:
        return int(_LOGIN_WINDOW - (now - fails[0])) + 1
    return 0


@app.post("/auth/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    key = (form_data.username or "").strip().lower()
    wait = _login_blocked(key)
    if wait:
        raise HTTPException(
            status_code=429,
            detail=f"Troppi tentativi falliti: riprova tra {max(1, wait // 60 + (1 if wait % 60 else 0))} minuti",
        )
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not user.active or not verify_password(form_data.password, user.hashed_password):
        _LOGIN_FAILS.setdefault(key, []).append(datetime.now().timestamp())
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o password errati",
            headers={"WWW-Authenticate": "Bearer"},
        )

    _LOGIN_FAILS.pop(key, None)
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me")
def me(current_user: User = Depends(get_current_user)):
    out = UserOut.model_validate(current_user).model_dump()
    # avvisa se l'account usa ancora la password predefinita del primo avvio
    out["default_password"] = verify_password(ADMIN_PASSWORD, current_user.hashed_password)
    return out


@app.post("/auth/change-password")
def change_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password attuale non corretta")
    if len(payload.new_password) < MIN_PASSWORD:
        raise HTTPException(status_code=400, detail=f"La nuova password deve avere almeno {MIN_PASSWORD} caratteri")
    if payload.new_password == ADMIN_PASSWORD:
        raise HTTPException(status_code=400, detail="Scegli una password diversa da quella predefinita")

    current_user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return {"ok": True}


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    year = Date.today().year
    today = Date.today()

    # Fatturato e incassi: solo fatture emesse o pagate (le bozze non contano)
    invoices = db.query(Document).filter(
        Document.kind == "Fattura",
        Document.status.in_(["emessa", "pagata"])
    ).all()
    invoiced = Decimal(0)
    collected = Decimal(0)
    to_collect = Decimal(0)
    invoiced_year = Decimal(0)
    for inv in invoices:
        t = document_totals(inv)
        invoiced += D(t["total"])
        collected += D(t["paid"])
        to_collect += D(t["residual"])
        if inv.date and inv.date.year == year:
            invoiced_year += D(t["total"])

    payables = db.query(PurchaseInvoice).filter(PurchaseInvoice.status == "da_pagare").all()
    to_pay = sum((D(_invoice_out(db, i)["total"]) for i in payables), Decimal(0))
    payables_overdue = [i for i in payables if i.due_date and i.due_date < today]
    payables_overdue_total = sum((D(_invoice_out(db, i)["total"]) for i in payables_overdue), Decimal(0))

    clients_map = {c.id: c.name for c in db.query(Client).all()}

    # Commesse con scadenza vicina (entro 15 giorni, non completate)
    horizon = today + timedelta(days=15)
    upcoming = db.query(Project).filter(
        Project.due_date.isnot(None),
        Project.due_date <= horizon,
        Project.status.in_(["aperta", "in_lavorazione"]),
    ).order_by(Project.due_date).limit(8).all()

    # Fatture non saldate oltre la scadenza
    overdue_rows = []
    for inv in invoices:
        residual = document_totals(inv)["residual"]
        if residual > 0 and inv.due_date and inv.due_date < today:
            overdue_rows.append({
                "id": inv.id, "number": inv.number, "client_id": inv.client_id,
                "client_name": clients_map.get(inv.client_id, ""),
                "due_date": inv.due_date, "residual": residual,
                "days_overdue": (today - inv.due_date).days,
            })
    overdue_rows.sort(key=lambda r: r["days_overdue"], reverse=True)

    inventory_value = db.query(SQLFunc.sum(Stock.qty * Item.cost)).join(
        Item, Stock.item_id == Item.id).scalar() or 0

    recent_docs = []
    for d in db.query(Document).order_by(Document.id.desc()).limit(6).all():
        recent_docs.append({
            **DocumentOut.model_validate(d).model_dump(),
            "client_name": clients_map.get(d.client_id, ""),
            "total": d.total,
        })

    # articoli sotto scorta minima
    stock_totals = dict(db.query(Stock.item_id, SQLFunc.sum(Stock.qty)).group_by(Stock.item_id).all())
    low_stock = []
    for item in db.query(Item).filter(Item.min_stock > 0).all():
        total = round(stock_totals.get(item.id, 0) or 0, 2)
        if total <= (item.min_stock or 0):
            low_stock.append({
                "item_id": item.id, "name": item.name, "unit": item.unit,
                "total_qty": total, "min_stock": item.min_stock,
            })
    low_stock.sort(key=lambda r: r["total_qty"] - r["min_stock"])
    low_stock = low_stock[:5]

    # prenotazioni scalo in corso o in arrivo (prossimi 7 giorni)
    agenda_alerts = []
    for b in db.query(Booking).filter(
        Booking.status.in_(["pianificato", "in_corso"]),
        Booking.end_date >= today,
        Booking.start_date <= horizon,
    ).order_by(Booking.start_date).limit(6).all():
        agenda_alerts.append({
            "id": b.id, "title": b.title,
            "resource_name": b.resource.name if b.resource else "",
            "start_date": b.start_date, "end_date": b.end_date, "status": b.status,
        })

    # Scadenze in arrivo (60 gg, incluse le già scadute): assicurazioni e
    # servizi delle barche, patenti/visite/corsi dei lavoratori
    horizon = today + timedelta(days=60)
    expiries = []
    for b in db.query(Boat).all():
        if b.insurance_expiry and b.insurance_expiry <= horizon:
            expiries.append({"kind": "barca", "label": f"Assicurazione {b.name}",
                             "date": b.insurance_expiry, "ref": f"/imbarcazioni/{b.id}"})
        if b.next_service_date and b.next_service_date <= horizon:
            expiries.append({"kind": "barca", "label": f"Servizio {b.name}",
                             "date": b.next_service_date, "ref": f"/imbarcazioni/{b.id}"})
    for w in db.query(Worker).filter(Worker.active == True).all():  # noqa: E712
        for fld, label in [("license_expiry", "Patente"), ("medical_exam_expiry", "Visita medica"),
                           ("safety_training_expiry", "Corso sicurezza")]:
            d = getattr(w, fld)
            if d and d <= horizon:
                expiries.append({"kind": "lavoratore", "label": f"{label} {w.name}",
                                 "date": d, "ref": "/lavoratori"})
    expiries.sort(key=lambda e: e["date"])

    return {
        "clients": db.query(Client).filter(Client.active == True).count(),  # noqa: E712
        "inactive_clients": db.query(Client).filter(Client.active == False).count(),  # noqa: E712
        "boats": db.query(Boat).count(),
        "open_projects": db.query(Project).filter(Project.status.in_(["aperta", "in_lavorazione"])).count(),
        "total_projects": db.query(Project).count(),
        "documents_this_year": db.query(Document).filter(
            Document.date >= Date(year, 1, 1), Document.date <= Date(year, 12, 31)).count(),
        "invoiced": money(invoiced),
        "invoiced_year": money(invoiced_year),
        "collected": money(collected),
        "to_collect": money(to_collect),
        "to_pay": money(to_pay),
        "payables_overdue_count": len(payables_overdue),
        "payables_overdue_total": money(payables_overdue_total),
        "inventory_value": money(inventory_value),
        "overdue_count": len(overdue_rows),
        "overdue_total": money(sum((D(r["residual"]) for r in overdue_rows), Decimal(0))),
        "overdue": overdue_rows[:5],
        "low_stock": low_stock,
        "agenda_alerts": agenda_alerts,
        "expiries": expiries[:8],
        "upcoming": [
            {
                "id": p.id, "number": p.number, "title": p.title,
                "client_id": p.client_id, "client_name": clients_map.get(p.client_id, ""),
                "due_date": p.due_date, "days_left": (p.due_date - today).days,
            } for p in upcoming
        ],
        "recent_projects": [
            {
                **ProjectOut.model_validate(p).model_dump(),
                "client_name": clients_map.get(p.client_id, ""),
            } for p in db.query(Project).order_by(Project.id.desc()).limit(8).all()
        ],
        "recent_documents": recent_docs,
    }


# =========================
# CLIENTS / BOATS
# =========================

@app.get("/clients", response_model=List[ClientOut])
def list_clients(
    q: Optional[str] = None,
    active: Optional[int] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    query = db.query(Client)
    if q:
        like = f"%{q}%"
        query = query.filter(
            Client.name.like(like) | Client.code.like(like) | Client.vat.like(like) |
            Client.tax_code.like(like) | Client.email.like(like) | Client.city.like(like) |
            Client.phone.like(like)
        )
    if active is not None:
        query = query.filter(Client.active == bool(active))
    return query.order_by(Client.name).all()


def next_client_code(db: Session) -> str:
    count = db.query(Client).count()
    code = f"CLI-{count + 1:04d}"
    while db.query(Client).filter(Client.code == code).first():
        count += 1
        code = f"CLI-{count + 1:04d}"
    return code


@app.post("/clients", response_model=ClientOut, status_code=201)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = payload.model_dump()
    if not data.get("code"):
        data["code"] = next_client_code(db)
    client = Client(**data)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@app.put("/clients/{client_id}", response_model=ClientOut)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    data = payload.model_dump()
    # un form che non gestisce il codice non deve cancellarlo
    if not data.get("code") and client.code:
        data["code"] = client.code
    for key, value in data.items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client


@app.get("/clients/{client_id}/detail")
def client_detail(client_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente non trovato")

    boats = db.query(Boat).filter(Boat.client_id == client_id).all()
    projects = db.query(Project).filter(Project.client_id == client_id).order_by(Project.id.desc()).all()
    docs = db.query(Document).filter(Document.client_id == client_id).order_by(Document.id.desc()).all()

    invoiced = Decimal(0)
    to_collect = Decimal(0)
    doc_rows = []
    for d in docs:
        totals = document_totals(d)
        if d.kind == "Fattura" and d.status in ("emessa", "pagata"):
            invoiced += D(totals["total"])
            to_collect += D(totals["residual"])
        doc_rows.append({
            **DocumentOut.model_validate(d).model_dump(),
            "client_name": client.name,
        })

    return {
        **ClientOut.model_validate(client).model_dump(),
        "boats": [BoatOut.model_validate(b).model_dump() for b in boats],
        "projects": [ProjectOut.model_validate(p).model_dump() for p in projects],
        "documents": doc_rows,
        "stats": {
            "boats": len(boats),
            "projects": len(projects),
            "documents": len(docs),
            "invoiced": money(invoiced),
            "to_collect": money(to_collect),
        },
    }


@app.delete("/clients/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente non trovato")

    if db.query(Document).filter(Document.client_id == client_id).count():
        raise HTTPException(status_code=400, detail="Il cliente ha documenti collegati: eliminarli prima")

    # prima le commesse (con lavori, ore, allegati), poi le imbarcazioni
    for project in db.query(Project).filter(Project.client_id == client_id).all():
        delete_project_objects(db, project)
        db.delete(project)
    db.flush()
    for boat in db.query(Boat).filter(Boat.client_id == client_id).all():
        db.query(Project).filter(Project.boat_id == boat.id).update({Project.boat_id: None})
        db.query(Booking).filter(Booking.boat_id == boat.id).update({Booking.boat_id: None})
        db.delete(boat)
    db.delete(client)
    db.commit()
    return Response(status_code=204)


@app.get("/boats", response_model=List[BoatOut])
def list_boats(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Boat).order_by(Boat.name).all()


@app.post("/boats", response_model=BoatOut, status_code=201)
def create_boat(payload: BoatCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Client, payload.client_id):
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    boat = Boat(**payload.model_dump())
    db.add(boat)
    db.commit()
    db.refresh(boat)
    return boat


@app.put("/boats/{boat_id}", response_model=BoatOut)
def update_boat(boat_id: int, payload: BoatUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    boat = db.get(Boat, boat_id)
    if not boat:
        raise HTTPException(status_code=404, detail="Imbarcazione non trovata")
    if not db.get(Client, payload.client_id):
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    for key, value in payload.model_dump().items():
        setattr(boat, key, value)
    db.commit()
    db.refresh(boat)
    return boat


@app.delete("/boats/{boat_id}", status_code=204)
def delete_boat(boat_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    boat = db.get(Boat, boat_id)
    if not boat:
        raise HTTPException(status_code=404, detail="Imbarcazione non trovata")
    db.query(Project).filter(Project.boat_id == boat_id).update({Project.boat_id: None})
    db.query(Booking).filter(Booking.boat_id == boat_id).update({Booking.boat_id: None})
    db.delete(boat)
    db.commit()
    return Response(status_code=204)


@app.get("/boats/{boat_id}/detail")
def boat_detail(boat_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    boat = db.get(Boat, boat_id)
    if not boat:
        raise HTTPException(status_code=404, detail="Imbarcazione non trovata")

    projects = db.query(Project).filter(Project.boat_id == boat_id).order_by(Project.id.desc()).all()
    project_ids = [p.id for p in projects]
    docs = db.query(Document).filter(Document.project_id.in_(project_ids)).order_by(Document.id.desc()).all() \
        if project_ids else []

    doc_rows = []
    invoiced = Decimal(0)
    for d in docs:
        if d.kind == "Fattura" and d.status in ("emessa", "pagata"):
            invoiced += D(d.total)
        doc_rows.append({
            **DocumentOut.model_validate(d).model_dump(),
            "client_name": boat.client.name if boat.client else "",
        })

    return {
        **BoatOut.model_validate(boat).model_dump(),
        "client_name": boat.client.name if boat.client else "",
        "projects": [ProjectOut.model_validate(p).model_dump() for p in projects],
        "documents": doc_rows,
        "stats": {
            "projects": len(projects),
            "documents": len(docs),
            "invoiced": money(invoiced),
        },
    }


# =========================
# WAREHOUSE / ITEMS / STOCK
# =========================

@app.get("/warehouses", response_model=List[WarehouseOut])
def list_warehouses(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Warehouse).all()


@app.post("/warehouses", response_model=WarehouseOut, status_code=201)
def create_warehouse(payload: WarehouseCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if db.query(Warehouse).filter(Warehouse.code == payload.code).first():
        raise HTTPException(status_code=400, detail="Codice magazzino già esistente")
    warehouse = Warehouse(**payload.model_dump())
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


@app.put("/warehouses/{warehouse_id}", response_model=WarehouseOut)
def update_warehouse(warehouse_id: int, payload: WarehouseCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    warehouse = db.get(Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Magazzino non trovato")
    if db.query(Warehouse).filter(Warehouse.code == payload.code, Warehouse.id != warehouse_id).first():
        raise HTTPException(status_code=400, detail="Codice magazzino già esistente")
    warehouse.code = payload.code
    warehouse.name = payload.name
    db.commit()
    db.refresh(warehouse)
    return warehouse


@app.delete("/warehouses/{warehouse_id}", status_code=204)
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    warehouse = db.get(Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Magazzino non trovato")
    if db.query(Stock).filter(Stock.warehouse_id == warehouse_id).count() or \
       db.query(Movement).filter(Movement.warehouse_id == warehouse_id).count():
        raise HTTPException(status_code=400, detail="Il magazzino ha giacenze o movimenti: non eliminabile")
    db.delete(warehouse)
    db.commit()
    return Response(status_code=204)


@app.get("/items", response_model=List[ItemOut])
def list_items(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Item).order_by(Item.name).all()


@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Articolo non trovato")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Articolo non trovato")

    has_movements = db.query(Movement).filter(Movement.item_id == item_id).count()
    has_po_lines = db.query(PurchaseOrderLine).filter(PurchaseOrderLine.item_id == item_id).count()
    if has_movements or db.query(Stock).filter(Stock.item_id == item_id).count() or has_po_lines:
        raise HTTPException(status_code=400, detail="L'articolo ha movimenti, giacenze o ordini: non eliminabile")

    db.delete(item)
    db.commit()
    return Response(status_code=204)


@app.get("/stock")
def list_stock(
    warehouse_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    query = db.query(Stock, Item.name, Warehouse.name).join(
        Item, Stock.item_id == Item.id
    ).join(
        Warehouse, Stock.warehouse_id == Warehouse.id
    )

    if warehouse_id:
        query = query.filter(Stock.warehouse_id == warehouse_id)

    result = []
    for stock, item_name, warehouse_name in query.all():
        result.append({
            "warehouse_id": stock.warehouse_id,
            "warehouse": warehouse_name,
            "item_id": stock.item_id,
            "item": item_name,
            "qty": stock.qty,
        })

    return result


@app.get("/movements")
def list_movements(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(Movement, Item.name, Warehouse.name, Project).join(
        Item, Movement.item_id == Item.id
    ).join(
        Warehouse, Movement.warehouse_id == Warehouse.id
    ).outerjoin(
        Project, Movement.project_id == Project.id
    ).order_by(Movement.id.desc()).limit(300)

    result = []
    for movement, item_name, warehouse_name, project in query.all():
        result.append({
            "id": movement.id,
            "date": movement.date,
            "type": movement.type,
            "qty": movement.qty,
            "unit_cost": movement.unit_cost,
            "item": item_name,
            "warehouse": warehouse_name,
            "warehouse_id": movement.warehouse_id,
            "item_id": movement.item_id,
            "project_id": movement.project_id,
            "project": project.number if project else "",
            "note": movement.note,
        })

    return result


@app.post("/movements", response_model=MovementOut, status_code=201)
def create_movement(
    payload: MovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.qty <= 0:
        raise HTTPException(status_code=400, detail="La quantità deve essere maggiore di zero")

    if payload.type not in ["carico", "scarico", "reso"]:
        raise HTTPException(status_code=400, detail="Tipo movimento non valido")

    warehouse = db.get(Warehouse, payload.warehouse_id)
    item = db.get(Item, payload.item_id)

    if not warehouse:
        raise HTTPException(status_code=404, detail="Magazzino non trovato")
    if not item:
        raise HTTPException(status_code=404, detail="Articolo non trovato")
    if payload.project_id and not db.get(Project, payload.project_id):
        raise HTTPException(status_code=404, detail="Commessa non trovata")

    stock = get_or_create_stock(db, payload.warehouse_id, payload.item_id)
    # costo non indicato: usa il costo medio dell'articolo (così la commessa lo contabilizza)
    unit_cost = payload.unit_cost if payload.unit_cost is not None else (item.cost or 0)

    if payload.type == "scarico":
        if stock.qty < payload.qty:
            raise HTTPException(status_code=400, detail=f"Giacenza insufficiente: disponibile {stock.qty}")
        stock.qty = float(D(stock.qty) - D(payload.qty))
    else:
        if payload.type == "carico":
            apply_average_cost(db, item, payload.qty, unit_cost)
        stock.qty = float(D(stock.qty) + D(payload.qty))

    movement = Movement(
        warehouse_id=payload.warehouse_id,
        item_id=payload.item_id,
        type=payload.type,
        qty=payload.qty,
        unit_cost=unit_cost,
        note=payload.note or "",
        user_id=current_user.id,
        project_id=payload.project_id,
        date=Date.today()
    )

    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement


def _movement_effect(m_type: str, qty: float) -> float:
    """Effetto di un movimento sulla giacenza."""
    return -qty if m_type == "scarico" else qty


def _remove_movement_effect(db: Session, movement: Movement) -> float:
    """Toglie l'effetto del movimento dalle giacenze (per modifica o elimina).
    Ritorna la giacenza di origine dopo la rimozione; errore se negativa."""
    old_stock = get_or_create_stock(db, movement.warehouse_id, movement.item_id)
    old_after = old_stock.qty - _movement_effect(movement.type, movement.qty)
    if old_after < 0:
        raise HTTPException(
            status_code=400,
            detail=f"Impossibile: la giacenza di origine diventerebbe negativa ({old_stock.qty} pz disponibili)"
        )
    return old_after


def _apply_movement_change(db: Session, movement: Movement, new_type: str, new_qty: float,
                           new_warehouse_id: int, new_item_id: int):
    """Ricalcola le giacenze quando un movimento viene modificato.
    Alza HTTPException senza toccare i dati se il risultato sarebbe negativo."""
    if new_qty <= 0:
        raise HTTPException(status_code=400, detail="La quantità deve essere maggiore di zero")

    old_after = _remove_movement_effect(db, movement)

    if (new_warehouse_id, new_item_id) == (movement.warehouse_id, movement.item_id):
        final_qty = old_after + _movement_effect(new_type, new_qty)
        if final_qty < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Giacenza insufficiente: dopo la modifica sarebbe {final_qty}"
            )
        get_or_create_stock(db, movement.warehouse_id, movement.item_id).qty = final_qty
    else:
        new_stock = get_or_create_stock(db, new_warehouse_id, new_item_id)
        target_after = new_stock.qty + _movement_effect(new_type, new_qty)
        if target_after < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Giacenza insufficiente nel magazzino di destinazione: disponibile {new_stock.qty}"
            )
        get_or_create_stock(db, movement.warehouse_id, movement.item_id).qty = old_after
        new_stock.qty = target_after


@app.put("/movements/{movement_id}", response_model=MovementOut)
def update_movement(
    movement_id: int,
    payload: MovementCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    movement = db.get(Movement, movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movimento non trovato")

    data = payload.model_dump()
    if data["type"] not in ["carico", "scarico", "reso"]:
        raise HTTPException(status_code=400, detail="Tipo movimento non valido")
    if not db.get(Warehouse, data["warehouse_id"]):
        raise HTTPException(status_code=404, detail="Magazzino non trovato")
    if not db.get(Item, data["item_id"]):
        raise HTTPException(status_code=404, detail="Articolo non trovato")
    if data.get("project_id") and not db.get(Project, data["project_id"]):
        raise HTTPException(status_code=404, detail="Commessa non trovata")

    _apply_movement_change(
        db, movement, data["type"], data["qty"], data["warehouse_id"], data["item_id"]
    )

    movement.type = data["type"]
    movement.qty = data["qty"]
    movement.warehouse_id = data["warehouse_id"]
    movement.item_id = data["item_id"]
    if data.get("unit_cost") is not None:
        movement.unit_cost = data["unit_cost"]
    movement.note = data.get("note") or ""
    movement.project_id = data.get("project_id")

    db.commit()
    db.refresh(movement)
    return movement


@app.delete("/movements/{movement_id}", status_code=204)
def delete_movement(movement_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    movement = db.get(Movement, movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movimento non trovato")

    old_stock = get_or_create_stock(db, movement.warehouse_id, movement.item_id)
    old_stock.qty = _remove_movement_effect(db, movement)
    db.delete(movement)
    db.commit()
    return Response(status_code=204)


@app.get("/projects/{project_id}/movements")
def project_movements(project_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Movimenti di magazzino collegati a una commessa (materiali scaricati ecc.)."""
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Commessa non trovata")

    query = db.query(Movement, Item.name, Warehouse.name).join(
        Item, Movement.item_id == Item.id
    ).join(
        Warehouse, Movement.warehouse_id == Warehouse.id
    ).filter(
        Movement.project_id == project_id
    ).order_by(Movement.id.desc())

    result = []
    for movement, item_name, warehouse_name in query.all():
        result.append({
            "id": movement.id,
            "date": movement.date,
            "type": movement.type,
            "qty": movement.qty,
            "unit_cost": movement.unit_cost,
            "item": item_name,
            "warehouse": warehouse_name,
            "warehouse_id": movement.warehouse_id,
            "item_id": movement.item_id,
            "project_id": movement.project_id,
            "note": movement.note,
        })

    return result


# =========================
# PROJECTS / JOBS / ATTACHMENTS
# =========================

def delete_project_objects(db: Session, project: Project):
    """Cancella dati collegati a una commessa (allegati su disco inclusi)."""
    for attachment in list(project.attachments):
        try:
            os.remove(resolve_stored_path(attachment.stored_path))
        except OSError:
            pass
        db.delete(attachment)
    for entry in db.query(TimeEntry).filter(TimeEntry.project_id == project.id).all():
        db.delete(entry)
    for job in list(project.jobs):
        db.delete(job)
    # prenotazioni agenda e movimenti: si stacca solo il riferimento
    db.query(Booking).filter(Booking.project_id == project.id).update({Booking.project_id: None})
    db.query(Movement).filter(Movement.project_id == project.id).update({Movement.project_id: None})
    db.query(Document).filter(Document.project_id == project.id).update({Document.project_id: None})


@app.get("/projects", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Project).order_by(Project.id.desc()).all()


@app.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    client = db.get(Client, payload.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente non trovato")

    if payload.boat_id:
        boat = db.get(Boat, payload.boat_id)
        if not boat:
            raise HTTPException(status_code=404, detail="Imbarcazione non trovata")

    project = Project(**payload.model_dump(), number=next_project_number(db))
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@app.put("/projects/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    if not db.get(Client, payload.client_id):
        raise HTTPException(status_code=404, detail="Cliente non trovato")

    data = payload.model_dump()
    if data.get("boat_id"):
        boat = db.get(Boat, data["boat_id"])
        if not boat:
            raise HTTPException(status_code=404, detail="Imbarcazione non trovata")

    for key, value in data.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


@app.post("/projects/{project_id}/status", response_model=ProjectOut)
def set_project_status(
    project_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    if status_value not in ["aperta", "in_lavorazione", "completata", "annullata"]:
        raise HTTPException(status_code=400, detail="Stato non valido")
    project.status = status_value
    db.commit()
    db.refresh(project)
    return project


@app.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    delete_project_objects(db, project)
    db.delete(project)
    db.commit()
    return Response(status_code=204)


@app.get("/projects/{project_id}/jobs", response_model=List[JobOut])
def list_jobs(project_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    return db.query(Job).filter(Job.project_id == project_id).order_by(Job.id).all()


@app.post("/projects/{project_id}/jobs", response_model=JobOut, status_code=201)
def create_job(project_id: int, payload: JobCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    job = Job(project_id=project_id, **payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@app.put("/jobs/{job_id}", response_model=JobOut)
def update_job(job_id: int, payload: JobUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Lavoro non trovato")
    for key, value in payload.model_dump().items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job


@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Lavoro non trovato")
    db.query(TimeEntry).filter(TimeEntry.job_id == job_id).update({TimeEntry.job_id: None})
    db.delete(job)
    db.commit()
    return Response(status_code=204)


@app.post("/projects/{project_id}/attachments", response_model=AttachmentOut, status_code=201)
def upload_attachment(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Commessa non trovata")

    folder = os.path.join(UPLOAD_DIR, "projects", str(project_id))
    os.makedirs(folder, exist_ok=True)

    safe_name = sanitize_filename(file.filename)
    stored_filename = f"{uuid.uuid4().hex}_{safe_name}"
    path = os.path.join(folder, stored_filename)

    size = save_upload(file, path)

    attachment = Attachment(
        project_id=project_id,
        filename=safe_name,
        stored_path=path,
        content_type=file.content_type or "application/octet-stream",
        file_size=size,
        user_id=current_user.id
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment


@app.get("/projects/{project_id}/attachments", response_model=List[AttachmentOut])
def list_attachments(project_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    return db.query(Attachment).filter(Attachment.project_id == project_id).order_by(Attachment.id.desc()).all()


@app.get("/attachments/{attachment_id}/download")
def download_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    attachment = db.get(Attachment, attachment_id)
    path = resolve_stored_path(attachment.stored_path) if attachment else ""
    if not attachment or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Allegato non trovato")

    return FileResponse(
        path,
        filename=attachment.filename,
        media_type=attachment.content_type
    )


@app.delete("/attachments/{attachment_id}", status_code=204)
def delete_attachment(attachment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    attachment = db.get(Attachment, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Allegato non trovato")
    try:
        os.remove(resolve_stored_path(attachment.stored_path))
    except OSError:
        pass
    db.delete(attachment)
    db.commit()
    return Response(status_code=204)


@app.post("/projects/{project_id}/create-document", response_model=DocumentOut, status_code=201)
def create_document_from_project(
    project_id: int,
    kind: str = "Proforma",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    """Genera un Proforma/DDT/Fattura dai lavori della commessa."""
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    if kind not in ["DDT", "Proforma", "Fattura"]:
        raise HTTPException(status_code=400, detail="Tipo documento non valido")

    jobs = db.query(Job).filter(Job.project_id == project_id).all()
    if not jobs:
        raise HTTPException(status_code=400, detail="La commessa non ha lavori: aggiungi almeno un lavoro prima")

    client = db.get(Client, project.client_id)
    settings = get_settings(db)
    doc = Document(
        kind=kind,
        number=next_document_number(db, kind),
        date=Date.today(),
        due_date=_default_due_date(db, client, Date.today()) if kind != "DDT" else None,
        client_id=project.client_id,
        project_id=project.id,
        status="bozza",
        tax_rate=settings.default_tax_rate,
        discount_pct=client.discount or 0,
        notes=f"Generato da commessa {project.number}",
        lines=[
            DocumentLine(
                description=job.description,
                qty=job.qty or 1,
                price=job.unit_price or 0,
                unit=(job.unit or "").strip(),
            )
            for job in jobs
        ],
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


# =========================
# DOCUMENTS / DDT / FATTURE
# =========================

@app.get("/documents", response_model=List[DocumentOut])
def list_documents(
    kind: Optional[str] = None,
    status: Optional[str] = None,
    client_id: Optional[int] = None,
    year: Optional[int] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    query = db.query(Document)
    if kind:
        query = query.filter(Document.kind == kind)
    if status:
        query = query.filter(Document.status == status)
    if client_id:
        query = query.filter(Document.client_id == client_id)
    if year:
        query = query.filter(Document.date >= Date(year, 1, 1), Document.date <= Date(year, 12, 31))
    if q:
        query = query.filter(Document.number.like(f"%{q}%"))
    return query.order_by(Document.id.desc()).all()


@app.get("/clients/export")
def export_clients_csv(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    import csv as csv_mod
    import io as io_mod
    from urllib.parse import quote

    out = io_mod.StringIO()
    writer = csv_mod.writer(out, delimiter=";", quoting=csv_mod.QUOTE_MINIMAL)
    writer.writerow(["Codice", "Nome", "Tipo", "P.IVA", "Codice fiscale", "Referente",
                     "Email", "PEC", "Telefono", "Cellulare", "Via", "CAP", "Città",
                     "Provincia", "Nazione", "Spedizione", "IBAN", "Pagamento",
                     "Sconto %", "Attivo", "Note"])
    for c in db.query(Client).order_by(Client.code, Client.name).all():
        writer.writerow([
            c.code, c.name, c.client_type, c.vat, c.tax_code, c.referente,
            c.email, c.pec, c.phone, c.mobile, c.address, c.zip, c.city,
            c.province, c.country, c.ship_to, c.iban, c.payment_terms,
            f"{(c.discount or 0):.2f}".replace(".", ","), "Sì" if c.active else "No", c.notes or "",
        ])
    content = out.getvalue().encode("utf-8-sig")
    filename = quote(f"clienti_{Date.today()}.csv")
    return Response(
        content=content, media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"}
    )


@app.get("/documents/export")
def export_documents_csv(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    import csv as csv_mod
    import io as io_mod
    from urllib.parse import quote

    clients_map = {c.id: c.name for c in db.query(Client).all()}
    out = io_mod.StringIO()
    writer = csv_mod.writer(out, delimiter=";", quoting=csv_mod.QUOTE_MINIMAL)
    writer.writerow(["Numero", "Tipo", "Data", "Scadenza", "Cliente", "Stato", "Imponibile", "IVA", "Totale", "Pagato", "Residuo"])
    for d in db.query(Document).order_by(Document.id).all():
        totals = document_totals(d)
        writer.writerow([
            d.number, d.kind, d.date.isoformat() if d.date else "",
            d.due_date.isoformat() if d.due_date else "",
            clients_map.get(d.client_id, ""), d.status,
            f"{totals['taxable']:.2f}".replace(".", ","), f"{totals['tax']:.2f}".replace(".", ","),
            f"{totals['total']:.2f}".replace(".", ","), f"{totals['paid']:.2f}".replace(".", ","),
            f"{totals['residual']:.2f}".replace(".", ","),
        ])
    content = out.getvalue().encode("utf-8-sig")
    filename = quote(f"documenti_{Date.today()}.csv")
    return Response(
        content=content, media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"}
    )


def _default_due_date(db: Session, client: Client, base: Date) -> Optional[Date]:
    """Scadenza: giorni indicati nelle condizioni di pagamento del cliente
    (es. "30 gg", "RIBA 60"), altrimenti il valore predefinito di Impostazioni."""
    m = re.search(r"\d+", client.payment_terms or "")
    days = int(m.group()) if m else (get_settings(db).default_payment_days or 0)
    return base + timedelta(days=days) if days else None


@app.post("/documents", response_model=DocumentOut, status_code=201)
def create_document(
    payload: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.kind not in ["DDT", "Proforma", "Fattura"]:
        raise HTTPException(status_code=400, detail="Tipo documento non valido")

    client = db.get(Client, payload.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente non trovato")

    if payload.project_id:
        project = db.get(Project, payload.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Commessa non trovata")

    doc_data = payload.model_dump(exclude={"lines", "due_date_auto"})
    # senza data esplicita il default SQL non scatta: impostala qui
    if not doc_data.get("date"):
        doc_data["date"] = Date.today()
    # valori non indicati: aliquota predefinita e sconto abituale del cliente
    if doc_data.get("tax_rate") is None:
        doc_data["tax_rate"] = get_settings(db).default_tax_rate
    if doc_data.get("discount_pct") is None:
        doc_data["discount_pct"] = client.discount or 0
    if payload.kind != "DDT" and not doc_data.get("due_date") and payload.due_date_auto:
        doc_data["due_date"] = _default_due_date(db, client, doc_data["date"])

    doc = Document(**doc_data, number=next_document_number(db, payload.kind), created_by=current_user.username)

    doc.lines = [
        DocumentLine(**line.model_dump())
        for line in payload.lines
    ]

    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@app.get("/documents/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento non trovato")

    totals = document_totals(doc)
    payments = db.query(Payment).filter(Payment.document_id == document_id).all()

    result = DocumentOut.model_validate(doc).model_dump()
    result.update(totals)
    result["payments"] = [PaymentOut.model_validate(p).model_dump() for p in payments]

    return result


@app.put("/documents/{document_id}", response_model=DocumentOut)
def update_document(
    document_id: int,
    payload: DocumentUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento non trovato")
    if doc.status in ("annullata", "archiviata"):
        raise HTTPException(status_code=400, detail="Documento annullato o archiviato: non modificabile")

    data = payload.model_dump(exclude_unset=True)
    # su un documento già pagato si correggono solo note e scadenza
    if doc.status == "pagata":
        data = {k: v for k, v in data.items() if k in ("notes", "due_date")}
        if not data:
            raise HTTPException(status_code=400, detail="Documento pagato: modificabili solo note e scadenza")

    if data.get("client_id") is not None and not db.get(Client, data["client_id"]):
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    if "project_id" in data and data["project_id"] is not None and not db.get(Project, data["project_id"]):
        raise HTTPException(status_code=404, detail="Commessa non trovata")

    if data.get("date") is None:
        data.pop("date", None)  # la data non si cancella
    for key, value in data.items():
        setattr(doc, key, value)
    _check_not_below_paid(db, doc)
    db.commit()
    db.refresh(doc)
    return doc


def _check_not_below_paid(db: Session, doc: Document):
    """Dopo una modifica agli importi il totale non può scendere sotto l'incassato."""
    db.flush()
    db.refresh(doc)
    t = document_totals(doc)
    if t["residual"] < 0:
        raise HTTPException(
            status_code=400,
            detail=f"Modifica non consentita: il totale ({t['total']:.2f} €) sarebbe inferiore a quanto già incassato ({t['paid']:.2f} €)".replace(".", ","),
        )
    _sync_payment_status(doc)


@app.post("/documents/{document_id}/lines", response_model=DocumentOut)
def add_document_line(
    document_id: int,
    payload: DocumentLineCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento non trovato")
    if doc.status not in ("bozza", "emessa"):
        raise HTTPException(status_code=400, detail="Non è possibile modificare un documento pagato o annullato")

    line = DocumentLine(document_id=document_id, **payload.model_dump())
    db.add(line)
    _check_not_below_paid(db, doc)
    db.commit()
    db.refresh(doc)
    return doc


@app.delete("/documents/{document_id}/lines/{line_id}", response_model=DocumentOut)
def delete_document_line(
    document_id: int,
    line_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento non trovato")
    if doc.status not in ("bozza", "emessa"):
        raise HTTPException(status_code=400, detail="Non è possibile modificare un documento pagato o annullato")

    line = db.get(DocumentLine, line_id)
    if not line or line.document_id != document_id:
        raise HTTPException(status_code=404, detail="Riga non trovata")
    db.delete(line)
    _check_not_below_paid(db, doc)
    db.commit()
    db.refresh(doc)
    return doc


@app.put("/documents/{document_id}/lines/{line_id}", response_model=DocumentOut)
def update_document_line(
    document_id: int,
    line_id: int,
    payload: DocumentLineCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento non trovato")
    if doc.status not in ("bozza", "emessa"):
        raise HTTPException(status_code=400, detail="Non è possibile modificare un documento pagato o annullato")

    line = db.get(DocumentLine, line_id)
    if not line or line.document_id != document_id:
        raise HTTPException(status_code=404, detail="Riga non trovata")

    for key, value in payload.model_dump().items():
        setattr(line, key, value)
    _check_not_below_paid(db, doc)
    db.commit()
    db.refresh(doc)
    return doc


def _sync_payment_status(doc: Document):
    """Allinea lo stato ai pagamenti: saldato -> pagata; non più saldato -> emessa."""
    if doc.status in ("annullata", "archiviata", "bozza"):
        return
    t = document_totals(doc)
    if t["total"] > 0 and t["residual"] <= 0:
        doc.status = "pagata"
    elif doc.status == "pagata":
        doc.status = "emessa"


@app.post("/documents/{document_id}/payments", response_model=PaymentOut, status_code=201)
def add_payment(
    document_id: int,
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento non trovato")
    if doc.kind == "DDT":
        raise HTTPException(status_code=400, detail="Un DDT non ha pagamenti: convertilo in fattura")
    if doc.status in ("annullata", "archiviata"):
        raise HTTPException(status_code=400, detail="Documento annullato o archiviato")

    amount = r2(payload.amount)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Importo pagamento non valido")
    residual = D(document_totals(doc)["residual"])
    if amount > residual:
        raise HTTPException(
            status_code=400,
            detail=f"L'importo supera il residuo da incassare ({residual:.2f} €)".replace(".", ","),
        )

    payment = Payment(
        document_id=document_id,
        date=payload.date or Date.today(),
        amount=float(amount),
        method=payload.method or "bonifico",
        note=payload.note or ""
    )
    db.add(payment)
    db.flush()
    db.refresh(doc)

    if doc.status == "bozza":
        doc.status = "emessa"  # un incasso presuppone un documento emesso
    _sync_payment_status(doc)

    db.commit()
    db.refresh(payment)
    return payment


@app.delete("/documents/{document_id}/payments/{payment_id}", status_code=204)
def delete_payment(
    document_id: int,
    payment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_manager)
):
    payment = db.get(Payment, payment_id)
    if not payment or payment.document_id != document_id:
        raise HTTPException(status_code=404, detail="Pagamento non trovato")
    doc = db.get(Document, document_id)
    db.delete(payment)
    db.flush()
    db.refresh(doc)
    _sync_payment_status(doc)
    db.commit()
    return Response(status_code=204)


# stati raggiungibili a mano: "pagata" si ottiene solo registrando i pagamenti
_DOC_TRANSITIONS = {
    "bozza": {"emessa", "annullata"},
    "emessa": {"bozza", "annullata", "archiviata"},
    "pagata": {"archiviata"},
    "annullata": {"bozza"},
    "archiviata": {"emessa"},
}


@app.post("/documents/{document_id}/status", response_model=DocumentOut)
def set_document_status(
    document_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento non trovato")
    if status_value not in ["bozza", "emessa", "pagata", "annullata", "archiviata"]:
        raise HTTPException(status_code=400, detail="Stato non valido")
    if status_value == doc.status:
        return doc
    if status_value == "pagata":
        raise HTTPException(status_code=400, detail="Lo stato “Pagata” si imposta registrando il pagamento")
    if status_value not in _DOC_TRANSITIONS.get(doc.status, set()):
        raise HTTPException(status_code=400, detail=f"Non si può passare da “{doc.status}” a “{status_value}”")

    totals = document_totals(doc)
    if status_value == "emessa" and doc.status == "bozza":
        if not doc.lines:
            raise HTTPException(status_code=400, detail="Aggiungi almeno una riga prima di emettere il documento")
        if doc.kind != "DDT" and totals["total"] <= 0:
            raise HTTPException(status_code=400, detail="Il totale del documento deve essere maggiore di zero")
        if doc.kind == "Fattura":
            problems = check_invoice_ready(db, doc)
            if problems:
                raise HTTPException(status_code=400, detail="Prima di emettere la fattura completa: " + "; ".join(problems))
    if status_value == "bozza" and doc.payments:
        raise HTTPException(status_code=400, detail="Il documento ha pagamenti registrati: eliminali prima")
    if status_value == "annullata" and doc.payments:
        raise HTTPException(status_code=400, detail="Il documento ha pagamenti registrati: eliminali prima di annullarlo")

    doc.status = status_value
    if status_value == "emessa":
        _sync_payment_status(doc)  # es. riattivazione di un documento già saldato
    db.commit()
    db.refresh(doc)
    return doc


@app.delete("/documents/{document_id}", status_code=204)
def delete_document(document_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    """Le fatture si eliminano solo in bozza (poi si annullano: la numerazione
    deve restare continua). DDT e proforma si possono eliminare se non incassati."""
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento non trovato")
    if doc.kind == "Fattura" and doc.status != "bozza":
        raise HTTPException(
            status_code=400,
            detail="Una fattura già emessa non si elimina: annullala (resta in archivio per la numerazione)")
    if doc.payments:
        raise HTTPException(status_code=400, detail="Il documento ha pagamenti registrati: eliminali prima")
    # i documenti generati da questo (es. la fattura nata da un DDT) restano, scollegati
    db.query(Document).filter(Document.source_document_id == doc.id).update({Document.source_document_id: None})
    db.delete(doc)
    db.commit()
    return Response(status_code=204)


@app.post("/documents/{document_id}/convert", response_model=DocumentOut, status_code=201)
def convert_document_to_invoice(
    document_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    source = db.get(Document, document_id)
    if not source:
        raise HTTPException(status_code=404, detail="Documento non trovato")

    if source.kind not in ["DDT", "Proforma"]:
        raise HTTPException(status_code=400, detail="Solo DDT o Proforma possono essere convertiti in fattura")

    if db.query(Document).filter(Document.source_document_id == source.id, Document.kind == "Fattura").first():
        raise HTTPException(status_code=400, detail="Questo documento è già stato convertito in fattura")

    new_doc = Document(
        kind="Fattura",
        number=next_document_number(db, "Fattura"),
        date=Date.today(),
        due_date=source.due_date,
        client_id=source.client_id,
        project_id=source.project_id,
        source_document_id=source.id,
        status="bozza",
        tax_rate=source.tax_rate,
        vat_nature=source.vat_nature,
        discount=source.discount,
        discount_pct=source.discount_pct,
        notes=f"Generata da {source.kind} {source.number}",
        lines=[
            DocumentLine(
                description=line.description,
                qty=line.qty,
                price=line.price,
                unit=line.unit or "",
            )
            for line in source.lines
        ]
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


@app.get("/documents/{document_id}/xml")
def download_einvoice_xml(
    document_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento non trovato")

    if doc.kind != "Fattura":
        raise HTTPException(status_code=400, detail="L'XML è disponibile solo per le fatture")

    xml = generate_fattura_xml(db, doc)

    filename = f"{doc.number.replace('/', '-').replace(' ', '_')}.xml"
    path = os.path.join(UPLOAD_DIR, "einvoice", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)

    doc.xml_path = path
    db.commit()

    return Response(
        content=xml,
        media_type="application/xml",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# =========================
# SCADENZARIO / RICERCA GLOBALE
# =========================

@app.get("/scadenzario")
def scadenzario(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Fatture non saldate, ordinate per ritardo di pagamento."""
    today = Date.today()
    clients_map = {c.id: c.name for c in db.query(Client).all()}
    rows = []
    for inv in db.query(Document).filter(
        Document.kind == "Fattura",
        Document.status == "emessa"
    ).order_by(Document.due_date.is_(None), Document.due_date, Document.id).all():
        totals = document_totals(inv)
        paid = totals["paid"]
        residual = totals["residual"]
        if residual <= 0:
            continue
        rows.append({
            "id": inv.id,
            "number": inv.number,
            "date": inv.date,
            "due_date": inv.due_date,
            "client_id": inv.client_id,
            "client_name": clients_map.get(inv.client_id, ""),
            "total": totals["total"],
            "paid": paid,
            "residual": residual,
            "days_overdue": (today - inv.due_date).days if inv.due_date and inv.due_date < today else 0,
        })
    return rows


@app.get("/search")
def global_search(q: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    like = f"%{q}%"
    clients = db.query(Client).filter(
        Client.name.like(like) | Client.code.like(like) | Client.vat.like(like) | Client.city.like(like)
    ).limit(5).all()
    boats = db.query(Boat).filter(
        Boat.name.like(like) | Boat.registration.like(like) | Boat.hull_id.like(like)
    ).limit(5).all()
    projects = db.query(Project).filter(
        Project.title.like(like) | Project.number.like(like)
    ).limit(5).all()
    documents = db.query(Document).filter(Document.number.like(like)).limit(5).all()

    boat_clients = {b.id: b.client.name if b.client else "" for b in boats}

    return {
        "clients": [{"id": c.id, "label": f"{c.code} - {c.name}" if c.code else c.name} for c in clients],
        "boats": [{"id": b.id, "label": f"{b.name} ({boat_clients.get(b.id, '')})"} for b in boats],
        "projects": [{"id": p.id, "label": f"{p.number} - {p.title}"} for p in projects],
        "documents": [{"id": d.id, "label": f"{d.kind} {d.number}"} for d in documents],
    }


# =========================
# GESTIONE UTENTI (admin)
# =========================

class UserAdminOut(ORMModel):
    id: int
    username: str
    email: str
    role: str
    active: bool


def _require_last_admin_guard(db: Session, target: User, new_active: bool, new_role: Optional[str]):
    """Impedisce di spegnere l'ultimo admin attivo."""
    becoming_inactive = (new_active is False and target.active)
    losing_role = (new_role is not None and new_role != "admin" and target.role == "admin")
    if (becoming_inactive or losing_role) and target.role == "admin":
        other_admins = db.query(User).filter(
            User.role == "admin", User.active == True, User.id != target.id  # noqa: E712
        ).count()
        if other_admins == 0:
            raise HTTPException(status_code=400, detail="Deve rimanere almeno un amministratore attivo")


@app.get("/users", response_model=List[UserAdminOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.query(User).order_by(User.id).all()


@app.post("/users", response_model=UserAdminOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not payload.username or len(payload.username) < 3:
        raise HTTPException(status_code=400, detail="Username di almeno 3 caratteri")
    if len(payload.password) < MIN_PASSWORD:
        raise HTTPException(status_code=400, detail=f"Password di almeno {MIN_PASSWORD} caratteri")
    if payload.role not in ("admin", "manager", "user"):
        raise HTTPException(status_code=400, detail="Ruolo non valido")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username già esistente")
    user = User(
        username=payload.username,
        email=payload.email or "",
        role=payload.role,
        hashed_password=hash_password(payload.password),
        active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.put("/users/{user_id}", response_model=UserAdminOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    _require_last_admin_guard(db, user, payload.active if payload.active is not None else user.active, payload.role)
    if payload.role is not None:
        if payload.role not in ("admin", "manager", "user"):
            raise HTTPException(status_code=400, detail="Ruolo non valido")
        user.role = payload.role
    if payload.active is not None:
        if not payload.active and user.id == current_user.id:
            raise HTTPException(status_code=400, detail="Non puoi disattivare te stesso")
        user.active = payload.active
    if payload.email is not None:
        user.email = payload.email
    db.commit()
    db.refresh(user)
    return user


@app.post("/users/{user_id}/set-password")
def set_user_password(user_id: int, payload: UserSetPassword, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    if len(payload.new_password) < MIN_PASSWORD:
        raise HTTPException(status_code=400, detail=f"Password di almeno {MIN_PASSWORD} caratteri")
    user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return {"ok": True}


# =========================
# ARCHIVIO DOCUMENTALE
# =========================

@app.get("/archive/folders", response_model=List[ArchiveFolderOut])
def archive_folders(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    folders = db.query(ArchiveFolder).order_by(ArchiveFolder.name).all()
    counts = dict(db.query(ArchiveFile.folder_id, SQLFunc.count(ArchiveFile.id)).group_by(ArchiveFile.folder_id).all())
    result = []
    for f in folders:
        row = ArchiveFolderOut.model_validate(f).model_dump()
        row["file_count"] = counts.get(f.id, 0)
        result.append(row)
    return result


@app.post("/archive/folders", response_model=ArchiveFolderOut, status_code=201)
def create_archive_folder(payload: ArchiveFolderCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if db.query(ArchiveFolder).filter(ArchiveFolder.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Esiste già una cartella con questo nome")
    folder = ArchiveFolder(name=payload.name, description=payload.description or "")
    db.add(folder)
    db.commit()
    db.refresh(folder)
    row = ArchiveFolderOut.model_validate(folder).model_dump()
    row["file_count"] = 0
    return row


@app.put("/archive/folders/{folder_id}", response_model=ArchiveFolderOut)
def update_archive_folder(folder_id: int, payload: ArchiveFolderCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    folder = db.get(ArchiveFolder, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Cartella non trovata")
    if db.query(ArchiveFolder).filter(ArchiveFolder.name == payload.name, ArchiveFolder.id != folder_id).first():
        raise HTTPException(status_code=400, detail="Esiste già una cartella con questo nome")
    folder.name = payload.name
    folder.description = payload.description or ""
    db.commit()
    db.refresh(folder)
    row = ArchiveFolderOut.model_validate(folder).model_dump()
    row["file_count"] = db.query(ArchiveFile).filter(ArchiveFile.folder_id == folder_id).count()
    return row


def _remove_archive_file(db: Session, att: ArchiveFile):
    try:
        os.remove(resolve_stored_path(att.stored_path))
    except OSError:
        pass
    db.delete(att)


@app.delete("/archive/folders/{folder_id}", status_code=204)
def delete_archive_folder(
    folder_id: int,
    with_files: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(require_manager)
):
    """Elimina una cartella. Se contiene file serve with_files=true (li cancella con lei)."""
    folder = db.get(ArchiveFolder, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Cartella non trovata")
    files = db.query(ArchiveFile).filter(ArchiveFile.folder_id == folder_id).all()
    if files and not with_files:
        raise HTTPException(status_code=400, detail="La cartella contiene file: svuotala prima")
    for att in files:
        _remove_archive_file(db, att)
    db.delete(folder)
    db.commit()
    return Response(status_code=204)


@app.get("/archive/files", response_model=List[ArchiveFileOut])
def archive_files(
    folder_id: Optional[int] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    query = db.query(ArchiveFile)
    if folder_id:
        query = query.filter(ArchiveFile.folder_id == folder_id)
    if q:
        query = query.filter(ArchiveFile.filename.like(f"%{q}%") | ArchiveFile.notes.like(f"%{q}%"))
    return query.order_by(ArchiveFile.id.desc()).limit(500).all()


@app.post("/archive/files", response_model=ArchiveFileOut, status_code=201)
def upload_archive_file(
    file: UploadFile = File(...),
    folder_id: int = 0,
    notes: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    folder = db.get(ArchiveFolder, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Cartella non trovata")

    target = os.path.join(UPLOAD_DIR, "archive", str(folder_id))
    os.makedirs(target, exist_ok=True)
    safe_name = sanitize_filename(file.filename)
    stored = os.path.join(target, f"{uuid.uuid4().hex}_{safe_name}")
    size = save_upload(file, stored)

    att = ArchiveFile(
        folder_id=folder_id,
        filename=safe_name,
        stored_path=stored,
        content_type=file.content_type or "application/octet-stream",
        file_size=size,
        notes=notes or "",
        user_id=current_user.id,
    )
    db.add(att)
    db.commit()
    db.refresh(att)
    return att


@app.get("/archive/files/{file_id}/download")
def download_archive_file(file_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    att = db.get(ArchiveFile, file_id)
    path = resolve_stored_path(att.stored_path) if att else ""
    if not att or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File non trovato")
    return FileResponse(path, filename=att.filename, media_type=att.content_type)


class BulkDelete(BaseModel):
    ids: List[int] = Field(min_length=1, max_length=1000)


@app.post("/archive/files/bulk-delete")
def bulk_delete_archive_files(payload: BulkDelete, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    """Cancellazione selettiva: elimina solo i file indicati (anche da cartelle diverse)."""
    files = db.query(ArchiveFile).filter(ArchiveFile.id.in_(set(payload.ids))).all()
    for att in files:
        _remove_archive_file(db, att)
    db.commit()
    return {"deleted": len(files), "requested": len(set(payload.ids))}


@app.delete("/archive/files/{file_id}", status_code=204)
def delete_archive_file(file_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    att = db.get(ArchiveFile, file_id)
    if not att:
        raise HTTPException(status_code=404, detail="File non trovato")
    _remove_archive_file(db, att)
    db.commit()
    return Response(status_code=204)


# =========================
# BACKUP DATI (admin)
# =========================

BACKUP_DIR = DATA_DIR / "backups"
BACKUP_KEEP = 14


def make_backup(target: Path) -> Path:
    """Copia consistente del database (anche se l'app lo sta usando)."""
    import sqlite3
    target.parent.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(engine.url.database)
    try:
        dst = sqlite3.connect(str(target))
        try:
            src.backup(dst)
        finally:
            dst.close()
    finally:
        src.close()
    return target


def daily_backup():
    """Un backup al giorno in data/backups, conservando gli ultimi BACKUP_KEEP."""
    if not DATABASE_URL.startswith("sqlite"):
        return
    target = BACKUP_DIR / f"shipyard_{Date.today():%Y%m%d}.db"
    if not target.exists():
        make_backup(target)
        logging.getLogger().info("Backup automatico creato: %s", target)
    old = sorted(BACKUP_DIR.glob("shipyard_*.db"))
    for f in old[:-BACKUP_KEEP]:
        try:
            f.unlink()
        except OSError:
            pass


def _backup_loop():
    import time
    while True:
        try:
            daily_backup()
        except Exception:  # un backup fallito non deve fermare l'app
            logging.getLogger().exception("Backup automatico non riuscito")
        time.sleep(3600)


@app.get("/admin/backup")
def backup_database(_: User = Depends(require_admin)):
    if not DATABASE_URL.startswith("sqlite") or not engine.url.database or not os.path.exists(engine.url.database):
        raise HTTPException(status_code=400, detail="Backup non disponibile")
    filename = f"cantiere_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.db"
    snapshot = make_backup(Path(UPLOAD_DIR).parent / f".snapshot_{uuid.uuid4().hex}.db")
    from starlette.background import BackgroundTask
    return FileResponse(
        snapshot, filename=filename, media_type="application/octet-stream",
        background=BackgroundTask(lambda: snapshot.unlink(missing_ok=True)),
    )


@app.get("/admin/backup/info")
def backup_info(_: User = Depends(require_admin)):
    files = sorted(BACKUP_DIR.glob("shipyard_*.db")) if BACKUP_DIR.exists() else []
    return {
        "folder": str(BACKUP_DIR),
        "count": len(files),
        "last": datetime.fromtimestamp(files[-1].stat().st_mtime).isoformat() if files else None,
        "keep": BACKUP_KEEP,
    }


# =========================
# SETTINGS
# =========================

@app.get("/lookups")
def list_lookups(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Tendine configurabili: {categoria: [valori ordinati]}"""
    rows = db.query(LookupOption).order_by(
        LookupOption.category, LookupOption.sort_order, LookupOption.value
    ).all()
    grouped: dict = {}
    for r in rows:
        grouped.setdefault(r.category, []).append(r.value)
    return grouped


@app.get("/lookups/full", response_model=List[LookupOut])
def list_lookups_full(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Elenco completo con id (serve alla pagina Impostazioni per eliminare le voci)."""
    return db.query(LookupOption).order_by(
        LookupOption.category, LookupOption.sort_order, LookupOption.value
    ).all()


@app.post("/lookups", response_model=LookupOut, status_code=201)
def create_lookup(payload: LookupCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo gli amministratori possono modificare le liste")
    cat = payload.category.strip()
    val = payload.value.strip()
    if not cat or not val:
        raise HTTPException(status_code=400, detail="Categoria e valore sono obbligatori")
    existing = db.query(LookupOption).filter(
        LookupOption.category == cat, LookupOption.value == val
    ).first()
    if existing:
        return existing  # già presente: nessun duplicato
    max_order = db.query(SQLFunc.max(LookupOption.sort_order)).filter(
        LookupOption.category == cat
    ).scalar() or 0
    opt = LookupOption(category=cat, value=val, sort_order=max_order + 1)
    db.add(opt)
    db.commit()
    db.refresh(opt)
    return opt


@app.delete("/lookups/{option_id}", status_code=204)
def delete_lookup(option_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo gli amministratori possono modificare le liste")
    opt = db.get(LookupOption, option_id)
    if not opt:
        raise HTTPException(status_code=404, detail="Opzione non trovata")
    db.delete(opt)
    db.commit()


@app.get("/settings", response_model=SettingsOut)
def read_settings(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_settings(db)


@app.put("/settings", response_model=SettingsOut)
def update_settings(
    payload: SettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo gli amministratori possono modificare le impostazioni")
    settings = get_settings(db)
    for key, value in payload.model_dump().items():
        setattr(settings, key, value)
    db.commit()
    db.refresh(settings)
    return settings


# =========================
# ACQUISTI: FORNITORI
# =========================

@app.get("/suppliers", response_model=List[SupplierOut])
def list_suppliers(q: Optional[str] = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(Supplier)
    if q:
        like = f"%{q}%"
        query = query.filter(Supplier.name.like(like) | Supplier.vat.like(like) | Supplier.email.like(like))
    return query.order_by(Supplier.name).all()


@app.post("/suppliers", response_model=SupplierOut, status_code=201)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@app.put("/suppliers/{supplier_id}", response_model=SupplierOut)
def update_supplier(supplier_id: int, payload: SupplierCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    for key, value in payload.model_dump().items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier


@app.delete("/suppliers/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    if db.query(PurchaseInvoice).filter(PurchaseInvoice.supplier_id == supplier_id).count() or \
       db.query(PurchaseOrder).filter(PurchaseOrder.supplier_id == supplier_id).count():
        raise HTTPException(status_code=400, detail="Il fornitore ha fatture o ordini collegati: non eliminabile")
    db.delete(supplier)
    db.commit()
    return Response(status_code=204)


# =========================
# ACQUISTI: FATTURE DI ACQUISTO
# =========================

def _normalize_purchase_invoice(data: dict, fallback_date: Optional[Date] = None):
    if data.get("status") not in ("da_pagare", "pagata"):
        raise HTTPException(status_code=400, detail="Stato non valido")
    if not data.get("date"):
        data["date"] = fallback_date or Date.today()
    if data["status"] == "pagata":
        data["paid_date"] = data.get("paid_date") or Date.today()
    else:
        data["paid_date"] = None
    data["amount_net"] = float(r2(data["amount_net"]))


def _invoice_out(db: Session, inv: PurchaseInvoice) -> dict:
    data = PurchaseInvoiceOut.model_validate(inv).model_dump()
    net = r2(inv.amount_net)
    vat = r2(net * D(inv.vat_rate) / 100)
    data["amount_net"] = float(net)
    data["vat"] = float(vat)
    data["total"] = float(net + vat)
    if inv.supplier:
        data["supplier_name"] = inv.supplier.name
    return data


@app.get("/purchase-invoices")
def list_purchase_invoices(
    year: Optional[int] = None,
    status: Optional[str] = None,
    supplier_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    query = db.query(PurchaseInvoice)
    if year:
        query = query.filter(PurchaseInvoice.date.like(f"{year}-%"))
    if status:
        query = query.filter(PurchaseInvoice.status == status)
    if supplier_id:
        query = query.filter(PurchaseInvoice.supplier_id == supplier_id)
    rows = query.order_by(PurchaseInvoice.date.desc(), PurchaseInvoice.id.desc()).all()
    return [_invoice_out(db, inv) for inv in rows]


@app.post("/purchase-invoices", status_code=201)
def create_purchase_invoice(payload: PurchaseInvoiceCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Supplier, payload.supplier_id):
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    data = payload.model_dump()
    _normalize_purchase_invoice(data)
    inv = PurchaseInvoice(**data)
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return _invoice_out(db, inv)


@app.put("/purchase-invoices/{invoice_id}")
def update_purchase_invoice(invoice_id: int, payload: PurchaseInvoiceCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    inv = db.get(PurchaseInvoice, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Fattura non trovata")
    if not db.get(Supplier, payload.supplier_id):
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    data = payload.model_dump()
    _normalize_purchase_invoice(data, inv.date)
    for key, value in data.items():
        setattr(inv, key, value)
    db.commit()
    db.refresh(inv)
    return _invoice_out(db, inv)


@app.delete("/purchase-invoices/{invoice_id}", status_code=204)
def delete_purchase_invoice(invoice_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    inv = db.get(PurchaseInvoice, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Fattura non trovata")
    db.delete(inv)
    db.commit()
    return Response(status_code=204)


@app.get("/vat-register")
def vat_register(year: Optional[int] = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Registro IVA base: IVA a debito (vendite) e a credito (acquisti) dell'anno,
    con il dettaglio per aliquota. Le vendite sono le fatture emesse o pagate
    dell'anno di emissione (le bozze e le annullate non entrano)."""
    year = year or Date.today().year
    first, last = Date(year, 1, 1), Date(year, 12, 31)
    clients_map = {c.id: c.name for c in db.query(Client).all()}

    sales = []
    sales_taxable = sales_vat = Decimal(0)
    sales_rates: dict = {}
    for d in db.query(Document).filter(
        Document.kind == "Fattura",
        Document.status.in_(["emessa", "pagata"]),
        Document.date >= first, Document.date <= last,
    ).order_by(Document.date, Document.id).all():
        totals = document_totals(d)
        sales.append({
            "number": d.number, "date": d.date, "client_name": clients_map.get(d.client_id, ""),
            "tax_rate": d.tax_rate, "taxable": totals["taxable"], "vat": totals["tax"], "total": totals["total"],
        })
        sales_taxable += D(totals["taxable"])
        sales_vat += D(totals["tax"])
        agg = sales_rates.setdefault(d.tax_rate or 0, [Decimal(0), Decimal(0)])
        agg[0] += D(totals["taxable"])
        agg[1] += D(totals["tax"])

    purchases = []
    purchases_net = purchases_vat = Decimal(0)
    purchase_rates: dict = {}
    for inv in db.query(PurchaseInvoice).filter(
        PurchaseInvoice.date >= first, PurchaseInvoice.date <= last
    ).order_by(PurchaseInvoice.date, PurchaseInvoice.id).all():
        out = _invoice_out(db, inv)
        purchases.append(out)
        purchases_net += D(out["amount_net"])
        purchases_vat += D(out["vat"])
        agg = purchase_rates.setdefault(inv.vat_rate or 0, [Decimal(0), Decimal(0)])
        agg[0] += D(out["amount_net"])
        agg[1] += D(out["vat"])

    def by_rate(rates):
        return [{"rate": r, "taxable": money(v[0]), "vat": money(v[1])} for r, v in sorted(rates.items())]

    return {
        "year": year,
        "sales": sales,
        "purchases": purchases,
        "sales_by_rate": by_rate(sales_rates),
        "purchases_by_rate": by_rate(purchase_rates),
        "summary": {
            "sales_taxable": money(sales_taxable),
            "sales_vat": money(sales_vat),
            "purchases_net": money(purchases_net),
            "purchases_vat": money(purchases_vat),
            "balance": money(sales_vat - purchases_vat),  # positivo = IVA a debito
        },
    }


@app.get("/purchase-invoices/export")
def export_purchase_invoices_csv(year: Optional[int] = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    import csv as csv_mod
    import io as io_mod
    from urllib.parse import quote

    year = year or Date.today().year
    out = io_mod.StringIO()
    writer = csv_mod.writer(out, delimiter=";", quoting=csv_mod.QUOTE_MINIMAL)
    writer.writerow(["Numero", "Fornitore", "Data", "Scadenza", "Imponibile", "IVA", "Totale", "Stato"])
    for inv in db.query(PurchaseInvoice).filter(PurchaseInvoice.date.like(f"{year}-%")).order_by(PurchaseInvoice.date).all():
        o = _invoice_out(db, inv)
        writer.writerow([o["number"], o["supplier_name"], o["date"], o["due_date"] or "",
                         f"{o['amount_net']:.2f}".replace(".", ","), f"{o['vat']:.2f}".replace(".", ","),
                         f"{o['total']:.2f}".replace(".", ","), o["status"]])
    content = out.getvalue().encode("utf-8-sig")
    filename = quote(f"registro_iva_acquisti_{year}.csv")
    return Response(
        content=content, media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"}
    )


# =========================
# AGENDA SCALI: POSTAZIONI E PRENOTAZIONI
# =========================

@app.get("/resources", response_model=List[ResourceOut])
def list_resources(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Resource).order_by(Resource.rtype, Resource.name).all()


@app.post("/resources", response_model=ResourceOut, status_code=201)
def create_resource(payload: ResourceCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    resource = Resource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


@app.put("/resources/{resource_id}", response_model=ResourceOut)
def update_resource(resource_id: int, payload: ResourceCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Postazione non trovata")
    for key, value in payload.model_dump().items():
        setattr(resource, key, value)
    db.commit()
    db.refresh(resource)
    return resource


@app.delete("/resources/{resource_id}", status_code=204)
def delete_resource(resource_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Postazione non trovata")
    if db.query(Booking).filter(Booking.resource_id == resource_id).count():
        raise HTTPException(status_code=400, detail="La postazione ha prenotazioni: eliminarle prima")
    db.delete(resource)
    db.commit()
    return Response(status_code=204)


BOOKING_STATUSES = ["pianificato", "in_corso", "completato", "annullato"]


def _booking_out(b: Booking) -> dict:
    data = BookingOut.model_validate(b).model_dump()
    data["resource_name"] = b.resource.name if b.resource else ""
    data["project_number"] = b.project.number if b.project else ""
    data["boat_name"] = b.boat.name if b.boat else ""
    return data


def _check_booking_conflict(db: Session, booking: Booking, resource_id: int, start: Date, end: Date, exclude_id: Optional[int] = None):
    """Una postazione non può avere due prenotazioni attive sovrapposte."""
    if end < start:
        raise HTTPException(status_code=400, detail="La data di fine è precedente all'inizio")
    q = db.query(Booking).filter(
        Booking.resource_id == resource_id,
        Booking.status.in_(["pianificato", "in_corso"]),
        Booking.start_date <= end,
        Booking.end_date >= start,
    )
    if exclude_id:
        q = q.filter(Booking.id != exclude_id)
    other = q.first()
    if other:
        raise HTTPException(
            status_code=400,
            detail=f"La postazione è già occupata dal {other.start_date} al {other.end_date}: “{other.title}”"
        )


@app.get("/bookings")
def list_bookings(
    year: Optional[int] = None,
    month: Optional[int] = None,
    resource_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    query = db.query(Booking)
    if year and month:
        first = Date(year, month, 1)
        last_day = (Date(year + int(month == 12), month % 12 + 1, 1) - timedelta(days=1))
        query = query.filter(Booking.start_date <= last_day, Booking.end_date >= first)
    elif year:
        query = query.filter(Booking.start_date.like(f"{year}-%"))
    if resource_id:
        query = query.filter(Booking.resource_id == resource_id)
    if status:
        query = query.filter(Booking.status == status)
    rows = query.order_by(Booking.start_date).all()
    return [_booking_out(b) for b in rows]


@app.post("/bookings", status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Resource, payload.resource_id):
        raise HTTPException(status_code=404, detail="Postazione non trovata")
    if payload.project_id and not db.get(Project, payload.project_id):
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    if payload.boat_id and not db.get(Boat, payload.boat_id):
        raise HTTPException(status_code=404, detail="Imbarcazione non trovata")
    _check_booking_conflict(db, None, payload.resource_id, payload.start_date, payload.end_date)
    booking = Booking(**payload.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return _booking_out(booking)


@app.put("/bookings/{booking_id}")
def update_booking(booking_id: int, payload: BookingCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    if not db.get(Resource, payload.resource_id):
        raise HTTPException(status_code=404, detail="Postazione non trovata")
    _check_booking_conflict(db, booking, payload.resource_id, payload.start_date, payload.end_date, exclude_id=booking_id)
    for key, value in payload.model_dump().items():
        setattr(booking, key, value)
    db.commit()
    db.refresh(booking)
    return _booking_out(booking)


@app.post("/bookings/{booking_id}/status")
def set_booking_status(booking_id: int, status_value: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    if status_value not in BOOKING_STATUSES:
        raise HTTPException(status_code=400, detail="Stato non valido")
    booking.status = status_value
    db.commit()
    db.refresh(booking)
    return _booking_out(booking)


@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    db.delete(booking)
    db.commit()
    return Response(status_code=204)


# =========================
# TIMESHEET: ORE PER COMMESSA + LAVORATORI
# =========================

def _time_entry_out(e: TimeEntry) -> dict:
    data = TimeEntryOut.model_validate(e).model_dump()
    data["job_description"] = e.job.description if e.job else ""
    data["worker_name"] = e.worker_ref.name if e.worker_ref else e.worker
    return data


@app.get("/workers", response_model=List[WorkerOut])
def list_workers(active: Optional[int] = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(Worker)
    if active is not None:
        query = query.filter(Worker.active == bool(active))
    return query.order_by(Worker.name).all()


@app.post("/workers", response_model=WorkerOut, status_code=201)
def create_worker(payload: WorkerCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    worker = Worker(**payload.model_dump())
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker


@app.put("/workers/{worker_id}", response_model=WorkerOut)
def update_worker(worker_id: int, payload: WorkerCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    worker = db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Lavoratore non trovato")
    for key, value in payload.model_dump().items():
        setattr(worker, key, value)
    db.commit()
    db.refresh(worker)
    return worker


@app.delete("/workers/{worker_id}", status_code=204)
def delete_worker(worker_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    worker = db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Lavoratore non trovato")
    # le ore restano: si stacca solo il riferimento (i costi storici restano invarati)
    db.query(TimeEntry).filter(TimeEntry.worker_id == worker_id).update({TimeEntry.worker_id: None})
    db.delete(worker)
    db.commit()
    return Response(status_code=204)


def _resolve_rates(db: Session, payload: TimeEntryCreate) -> dict:
    """Determina lavoratore e tariffe: se non date, usa quelle della scheda."""
    worker_ref = None
    if payload.worker_id:
        worker_ref = db.get(Worker, payload.worker_id)
        if not worker_ref:
            raise HTTPException(status_code=404, detail="Lavoratore non trovato")
    hourly_cost = payload.hourly_cost if payload.hourly_cost is not None else (worker_ref.hourly_cost if worker_ref else 0)
    hourly_price = payload.hourly_price if payload.hourly_price is not None else (worker_ref.hourly_price if worker_ref else 0)
    return {
        "worker_ref": worker_ref,
        "worker": worker_ref.name if worker_ref else (payload.worker or ""),
        "hourly_cost": hourly_cost or 0,
        "hourly_price": hourly_price or 0,
    }


@app.get("/projects/{project_id}/timesheets")
def project_timesheets(project_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    entries = db.query(TimeEntry).filter(TimeEntry.project_id == project_id).order_by(TimeEntry.date.desc(), TimeEntry.id.desc()).all()
    total_hours = sum((D(e.hours) for e in entries), Decimal(0))
    total_labor_cost = sum((r2(D(e.hours) * D(e.hourly_cost)) for e in entries), Decimal(0))
    total_labor_price = sum((r2(D(e.hours) * D(e.hourly_price)) for e in entries), Decimal(0))
    # ore preventivate: lavori di manodopera espressi in ore
    budget_hours = sum(j.qty for j in db.query(Job).filter(
        Job.project_id == project_id, Job.unit == "ore").all())
    by_worker = {}
    for e in entries:
        name = e.worker_ref.name if e.worker_ref else (e.worker or "—")
        agg = by_worker.setdefault(name, {"hours": 0, "cost": 0})
        agg["hours"] = money(D(agg["hours"]) + D(e.hours))
        agg["cost"] = money(D(agg["cost"]) + r2(D(e.hours) * D(e.hourly_cost)))
    return {
        "entries": [_time_entry_out(e) for e in entries],
        "total_hours": money(total_hours),
        "total_labor_cost": money(total_labor_cost),
        "total_labor_price": money(total_labor_price),
        "budget_hours": round(budget_hours, 2),
        "by_worker": by_worker,
    }


_LABOR_CATEGORIES = {"manodopera"}
_MATERIAL_CATEGORIES = {"ricambi", "materiali"}


@app.get("/projects/{project_id}/summary")
def project_summary(project_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Redditività della commessa. Ricavo = valore dei lavori a prezzo di listino.
    Per ogni voce di costo si usa il consuntivo se esiste (ore registrate, materiali
    scaricati dal magazzino), altrimenti il preventivo dei lavori; i costi di
    noleggi, subappalti e altro vengono sempre dai lavori."""
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Commessa non trovata")

    jobs = db.query(Job).filter(Job.project_id == project_id).all()
    revenue = Decimal(0)
    est = {"labor": Decimal(0), "material": Decimal(0), "other": Decimal(0)}
    budget_hours = Decimal(0)
    for j in jobs:
        revenue += r2(D(j.qty) * D(j.unit_price))
        cost = r2(D(j.qty) * D(j.unit_cost))
        cat = (j.category or "").strip().lower()
        bucket = "labor" if cat in _LABOR_CATEGORIES else "material" if cat in _MATERIAL_CATEGORIES else "other"
        est[bucket] += cost
        if (j.unit or "").strip().lower() == "ore":
            budget_hours += D(j.qty)

    movs = db.query(Movement).filter(Movement.project_id == project_id, Movement.type.in_(["scarico", "reso"])).all()
    material_actual = sum(
        ((1 if m.type == "scarico" else -1) * r2(D(m.qty) * D(m.unit_cost)) for m in movs), Decimal(0))

    entries = db.query(TimeEntry).filter(TimeEntry.project_id == project_id).all()
    hours = sum((D(e.hours) for e in entries), Decimal(0))
    labor_actual = sum((r2(D(e.hours) * D(e.hourly_cost)) for e in entries), Decimal(0))
    labor_billable = sum((r2(D(e.hours) * D(e.hourly_price)) for e in entries), Decimal(0))

    labor_cost = labor_actual if hours > 0 else est["labor"]
    material_cost = material_actual if movs else est["material"]
    total_cost = labor_cost + material_cost + est["other"]
    estimated_cost = est["labor"] + est["material"] + est["other"]
    margin = revenue - total_cost

    invoices = db.query(Document).filter(
        Document.project_id == project_id, Document.kind == "Fattura",
        Document.status.in_(["emessa", "pagata"])).all()
    invoiced = sum((D(document_totals(i)["taxable"]) for i in invoices), Decimal(0))

    return {
        "revenue": money(revenue),
        "estimated_cost": money(estimated_cost),
        "labor_cost": money(labor_cost),
        "labor_source": "ore registrate" if hours > 0 else "preventivo",
        "material_cost": money(material_cost),
        "material_source": "scarichi di magazzino" if movs else "preventivo",
        "other_cost": money(est["other"]),
        "total_cost": money(total_cost),
        "margin": money(margin),
        "margin_pct": round(float(margin / revenue * 100), 1) if revenue > 0 else None,
        "hours": float(r2(hours)),
        "budget_hours": float(r2(budget_hours)),
        "labor_billable": money(labor_billable),
        "invoiced": money(invoiced),
        "to_invoice": money(max(Decimal(0), revenue - invoiced)),
        "jobs": len(jobs),
    }


@app.post("/projects/{project_id}/timesheets", status_code=201)
def create_time_entry(project_id: int, payload: TimeEntryCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Commessa non trovata")
    if payload.hours <= 0 or payload.hours > 24:
        raise HTTPException(status_code=400, detail="Le ore devono essere tra 0,1 e 24")
    if payload.job_id and not db.get(Job, payload.job_id):
        raise HTTPException(status_code=404, detail="Lavoro non trovato")
    rates = _resolve_rates(db, payload)
    entry = TimeEntry(
        project_id=project_id,
        job_id=payload.job_id,
        worker=rates["worker"],
        worker_id=rates["worker_ref"].id if rates["worker_ref"] else None,
        hourly_cost=rates["hourly_cost"],
        hourly_price=rates["hourly_price"],
        date=payload.date or Date.today(),
        hours=payload.hours,
        notes=payload.notes or "",
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return _time_entry_out(entry)


@app.put("/timesheets/{entry_id}")
def update_time_entry(entry_id: int, payload: TimeEntryCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    entry = db.get(TimeEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Riga ore non trovata")
    if payload.job_id and not db.get(Job, payload.job_id):
        raise HTTPException(status_code=404, detail="Lavoro non trovato")
    rates = _resolve_rates(db, payload)
    entry.job_id = payload.job_id
    entry.worker = rates["worker"]
    entry.worker_id = rates["worker_ref"].id if rates["worker_ref"] else None
    entry.hourly_cost = rates["hourly_cost"]
    entry.hourly_price = rates["hourly_price"]
    entry.date = payload.date or entry.date
    entry.hours = payload.hours
    entry.notes = payload.notes or ""
    db.commit()
    db.refresh(entry)
    return _time_entry_out(entry)


@app.delete("/timesheets/{entry_id}", status_code=204)
def delete_time_entry(entry_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    entry = db.get(TimeEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Riga ore non trovata")
    db.delete(entry)
    db.commit()
    return Response(status_code=204)


# =========================
# SCORTE: ARTICOLI SOTTO SCORTA MINIMA
# =========================

@app.get("/stock/alerts")
def stock_alerts(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Giacenza totale per articolo (tutti i magazzini) e flag sotto scorta."""
    totals = dict(db.query(Stock.item_id, SQLFunc.sum(Stock.qty)).group_by(Stock.item_id).all())
    result = []
    for item in db.query(Item).order_by(Item.name).all():
        total = round(totals.get(item.id, 0) or 0, 2)
        result.append({
            "item_id": item.id,
            "name": item.name,
            "sku": item.sku,
            "unit": item.unit,
            "total_qty": total,
            "min_stock": item.min_stock or 0,
            "alert": (item.min_stock or 0) > 0 and total <= (item.min_stock or 0),
        })
    return result


# =========================
# ORDINI DI ACQUISTO
# =========================

def next_po_number(db: Session) -> str:
    return _next_number(db, PurchaseOrder, f"OA-{Date.today().year}-")


def _po_out(po: PurchaseOrder) -> dict:
    data = PurchaseOrderOut.model_validate(po).model_dump()
    data["supplier_name"] = po.supplier.name if po.supplier else ""
    for line, out in zip(po.lines, data["lines"]):
        out["item_name"] = line.item_ref.name if line.item_ref else ""
    return data


@app.get("/purchase-orders")
def list_purchase_orders(status: Optional[str] = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(PurchaseOrder)
    if status:
        query = query.filter(PurchaseOrder.status == status)
    rows = query.order_by(PurchaseOrder.id.desc()).all()
    return [_po_out(po) for po in rows]


@app.get("/purchase-orders/{order_id}")
def get_purchase_order(order_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    po = db.get(PurchaseOrder, order_id)
    if not po:
        raise HTTPException(status_code=404, detail="Ordine non trovato")
    out = _po_out(po)
    out["total"] = money(sum((D(l.qty) * D(l.unit_cost) for l in po.lines), Decimal(0)))
    return out


@app.post("/purchase-orders", status_code=201)
def create_purchase_order(payload: PurchaseOrderCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Supplier, payload.supplier_id):
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    po = PurchaseOrder(
        number=next_po_number(db),
        supplier_id=payload.supplier_id,
        date=payload.date or Date.today(),
        expected_date=payload.expected_date,
        status=payload.status if payload.status in ("bozza", "inviato") else "bozza",
        notes=payload.notes or "",
        lines=[
            PurchaseOrderLine(item_id=l.item_id, description=l.description, qty=l.qty, unit_cost=l.unit_cost)
            for l in payload.lines
        ],
    )
    db.add(po)
    db.commit()
    db.refresh(po)
    return _po_out(po)


@app.put("/purchase-orders/{order_id}")
def update_purchase_order(order_id: int, payload: PurchaseOrderCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    po = db.get(PurchaseOrder, order_id)
    if not po:
        raise HTTPException(status_code=404, detail="Ordine non trovato")
    if not db.get(Supplier, payload.supplier_id):
        raise HTTPException(status_code=404, detail="Fornitore non trovato")
    if po.status == "ricevuto":
        raise HTTPException(status_code=400, detail="Ordine già ricevuto: non modificabile")
    po.supplier_id = payload.supplier_id
    po.date = payload.date or po.date
    po.expected_date = payload.expected_date
    po.notes = payload.notes or ""
    if payload.status and payload.status != po.status:
        if payload.status == "ricevuto":
            raise HTTPException(status_code=400, detail="Per ricevere l'ordine usa “Ricevi merce”: genera i carichi in magazzino")
        if payload.status not in ("bozza", "inviato", "annullato"):
            raise HTTPException(status_code=400, detail="Stato non valido")
        po.status = payload.status
    if payload.lines is not None:
        po.lines.clear()
        db.flush()
        for l in payload.lines:
            po.lines.append(PurchaseOrderLine(item_id=l.item_id, description=l.description, qty=l.qty, unit_cost=l.unit_cost))
    db.commit()
    db.refresh(po)
    return _po_out(po)


@app.post("/purchase-orders/{order_id}/status")
def set_purchase_order_status(order_id: int, status_value: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    po = db.get(PurchaseOrder, order_id)
    if not po:
        raise HTTPException(status_code=404, detail="Ordine non trovato")
    if status_value not in ["bozza", "inviato", "ricevuto", "annullato"]:
        raise HTTPException(status_code=400, detail="Stato non valido")
    if status_value == "ricevuto":
        raise HTTPException(status_code=400, detail="Per ricevere l'ordine usa “Ricevi merce”: genera i carichi in magazzino")
    if po.status == "ricevuto":
        raise HTTPException(status_code=400, detail="Ordine già ricevuto: lo stato non si cambia")
    po.status = status_value
    db.commit()
    db.refresh(po)
    return _po_out(po)


@app.post("/purchase-orders/{order_id}/receive")
def receive_purchase_order(
    order_id: int,
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Riceve l'ordine: genera i movimenti di carico in magazzino e chiude l'ordine."""
    po = db.get(PurchaseOrder, order_id)
    if not po:
        raise HTTPException(status_code=404, detail="Ordine non trovato")
    if po.status == "ricevuto":
        raise HTTPException(status_code=400, detail="Ordine già ricevuto")
    if po.status == "annullato":
        raise HTTPException(status_code=400, detail="Ordine annullato")
    warehouse = db.get(Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Magazzino non trovato")

    received = 0
    for line in po.lines:
        if not line.item_id:
            continue  # righe libere senza articolo: nessun carico
        stock = get_or_create_stock(db, warehouse_id, line.item_id)
        item = db.get(Item, line.item_id)
        if item:
            apply_average_cost(db, item, line.qty, line.unit_cost)
        stock.qty = float(D(stock.qty) + D(line.qty))
        db.add(Movement(
            warehouse_id=warehouse_id,
            item_id=line.item_id,
            type="carico",
            qty=line.qty,
            unit_cost=line.unit_cost or 0,
            note=f"Ricezione ordine {po.number}",
            user_id=current_user.id,
            date=Date.today(),
        ))
        received += 1

    po.status = "ricevuto"
    db.commit()
    return {"ok": True, "received_lines": received, "total_lines": len(po.lines)}


@app.delete("/purchase-orders/{order_id}", status_code=204)
def delete_purchase_order(order_id: int, db: Session = Depends(get_db), _: User = Depends(require_manager)):
    po = db.get(PurchaseOrder, order_id)
    if not po:
        raise HTTPException(status_code=404, detail="Ordine non trovato")
    if po.status == "ricevuto":
        raise HTTPException(status_code=400, detail="L'ordine è già stato ricevuto: non eliminabile")
    db.delete(po)
    db.commit()
    return Response(status_code=204)


# =========================
# INTERFACCIA WEB (SPA)
# =========================

from fastapi.staticfiles import StaticFiles

STATIC_DIR = BASE_DIR / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()

    # Scegli la prima porta libera a partire da PORT (utile se un'altra
    # istanza è già in esecuzione).
    chosen = PORT
    for candidate in range(PORT, PORT + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, candidate))
                chosen = candidate
                break
            except OSError:
                continue

    if chosen != PORT:
        globals()["PORT"] = chosen

    logging.getLogger().info("Avvio Cantiere Navale Pro su http://%s:%s", HOST, chosen)
    uvicorn.run(app, host=HOST, port=chosen, log_level="info")
