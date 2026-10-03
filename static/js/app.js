/* Cantiere Navale Pro — SPA v2 */
"use strict";

/* ============ Icone SVG (stroke, stile lucide) ============ */

const ICONS = {
  dashboard: '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
  users: '<circle cx="9" cy="7" r="3.5"/><path d="M2.5 21v-1.5A5.5 5.5 0 0 1 8 14h2a5.5 5.5 0 0 1 5.5 5.5V21"/><path d="M16 3.6a3.5 3.5 0 0 1 0 6.8"/><path d="M17.5 14.4a5.5 5.5 0 0 1 4 5.1V21"/>',
  anchor: '<circle cx="12" cy="5" r="3"/><path d="M12 22V8"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/>',
  clipboard: '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4M12 16h4M8 11h.01M8 16h.01"/>',
  box: '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
  file: '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v5h5"/><path d="M9 13h6M9 17h6"/>',
  folder: '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
  calendar: '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
  cart: '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>',
  alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4M12 17h.01"/>',
  euro: '<path d="M4 10h12M4 14h9"/><path d="M19 6a7.7 7.7 0 0 0-5.2-2A7.9 7.9 0 0 0 6 12a7.9 7.9 0 0 0 7.8 8 7.7 7.7 0 0 0 5.2-2"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  edit: '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>',
  trash: '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
  download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
  upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
  printer: '<path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8" rx="1"/>',
  x: '<path d="M18 6 6 18M6 6l12 12"/>',
  check: '<path d="M20 6 9 17l-5-5"/>',
  settings: '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M2 14h4M10 8h4M18 16h4"/>',
  logout: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>',
  chevron: '<path d="m9 18 6-6-6-6"/>',
  arrowleft: '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
  eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
  archive: '<rect x="2" y="3" width="20" height="5" rx="1"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/>',
  wallet: '<rect x="2" y="6" width="20" height="13" rx="2.5"/><circle cx="12" cy="12.5" r="2"/><path d="M6 6V4.5A1.5 1.5 0 0 1 7.5 3h9"/>',
  db: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/>',
  userplus: '<circle cx="10" cy="7" r="3.5"/><path d="M2.5 21v-1.5A5.5 5.5 0 0 1 8 14h4a5.5 5.5 0 0 1 5.5 5.5V21"/><path d="M19 8v6M16 11h6"/>',
};
const icon = (name, size = 17) =>
  `<svg class="ic" viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${ICONS[name] || ""}</svg>`;

/* ============ Helpers base ============ */

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

const eur = new Intl.NumberFormat("it-IT", { style: "currency", currency: "EUR" });
const fmtEur = v => eur.format(v || 0);
const fmtNum = v => new Intl.NumberFormat("it-IT").format(v || 0);
const fmtDate = iso => iso ? String(iso).slice(0, 10).split("-").reverse().join("/") : "—";
const fmtDateTime = iso => {
  if (!iso) return "—";
  const d = new Date(iso);
  return d.toLocaleDateString("it-IT") + " " + d.toLocaleTimeString("it-IT", { hour: "2-digit", minute: "2-digit" });
};
const fmtSize = b => {
  if (!b && b !== 0) return "—";
  if (b < 1024) return b + " B";
  if (b < 1048576) return (b / 1024).toFixed(1) + " KB";
  return (b / 1048576).toFixed(1) + " MB";
};
const todayISO = () => new Date().toISOString().slice(0, 10);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const num = v => { const n = parseFloat(String(v).replace(",", ".")); return isNaN(n) ? 0 : n; };

/* Inject icone nella sidebar/topbar statici */
document.querySelectorAll("#main-nav a").forEach(a => {
  const map = { dashboard: "dashboard", clienti: "users", imbarcazioni: "anchor", lavoratori: "userplus", commesse: "clipboard", agenda: "calendar", magazzino: "box", documenti: "file", scadenzario: "clock", acquisti: "cart", archivio: "archive", impostazioni: "settings" };
  a.insertAdjacentHTML("afterbegin", icon(map[a.dataset.nav] || "file", 16));
});
$(".search-icon").innerHTML = icon("search", 16);

function toast(message, type = "") {
  const el = document.createElement("div");
  el.className = "toast " + type;
  el.textContent = message;
  $("#toast-root").appendChild(el);
  setTimeout(() => el.remove(), 4200);
}

/* ============ API ============ */

let TOKEN = localStorage.getItem("cn_token") || "";
let CURRENT_USER = null;

async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (TOKEN) headers["Authorization"] = "Bearer " + TOKEN;
  if (options.json !== undefined) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(options.json);
    delete options.json;
  }
  const res = await fetch(path, { ...options, headers });

  if (res.status === 401 && TOKEN) {
    doLogout(false);
    throw new Error("Sessione scaduta: accedi di nuovo");
  }
  if (res.status === 204) return null;
  let data = null;
  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) data = await res.json();
  if (!res.ok) {
    const detail = data && (data.detail || data.message);
    throw new Error(typeof detail === "string" ? detail : "Errore " + res.status);
  }
  return data;
}

async function downloadFile(url, fallbackName) {
  const headers = TOKEN ? { "Authorization": "Bearer " + TOKEN } : {};
  const res = await fetch(url, { headers });
  if (!res.ok) {
    let msg = "Download non riuscito";
    try { const j = await res.json(); if (typeof j.detail === "string") msg = j.detail; } catch { /* nessun dettaglio */ }
    toast(msg, "error");
    return;
  }
  const blob = await res.blob();
  const cd = res.headers.get("content-disposition") || "";
  const m = cd.match(/filename\*=UTF-8''([^;]+)/) || cd.match(/filename="?([^";]+)"?/);
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = m ? decodeURIComponent(m[1]) : fallbackName;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
}

/* ============ Badge / etichette ============ */

const PROJECT_STATUS = {
  aperta: ["Aperta", "badge-blue"],
  in_lavorazione: ["In lavorazione", "badge-amber"],
  completata: ["Completata", "badge-green"],
  annullata: ["Annullata", "badge-gray"],
};
const DOC_STATUS = {
  bozza: ["Bozza", "badge-gray"],
  emessa: ["Emessa", "badge-teal"],
  pagata: ["Pagata", "badge-green"],
  annullata: ["Annullata", "badge-red"],
  archiviata: ["Archiviata", "badge-blue"],
};
const MOV_TYPE = {
  carico: ["Carico", "badge-green"],
  scarico: ["Scarico", "badge-red"],
  reso: ["Reso", "badge-amber"],
};
const JOB_STATUS = {
  "Da fare": ["Da fare", "badge-gray"],
  "In corso": ["In corso", "badge-amber"],
  "Completata": ["Completata", "badge-green"],
};
const badge = (map, key) => {
  const [label, cls] = map[key] || [key || "—", "badge-gray"];
  return `<span class="badge ${cls}">${esc(label)}</span>`;
};
/* I totali li calcola sempre il server (arrotondamenti al centesimo): qui si leggono soltanto */
const docTot = d => d.total || 0;
const lineTotal = l => Math.round((l.qty || 0) * (l.price || 0) * 100) / 100;
const VAT_NATURES = {
  "N3.4": "N3.4 — Non imponibile, operazioni assimilate all'esportazione (art. 8-bis)",
  "N3.1": "N3.1 — Non imponibile, esportazioni",
  "N3.2": "N3.2 — Non imponibile, cessioni intracomunitarie",
  "N4": "N4 — Esente",
  "N2.2": "N2.2 — Non soggetta, altri casi",
  "N6.9": "N6.9 — Inversione contabile",
  "N1": "N1 — Esclusa ex art. 15",
};
const vatNatureOptions = sel => `<option value="">— scegli —</option>` +
  Object.entries(VAT_NATURES).map(([k, l]) => `<option value="${k}" ${sel === k ? "selected" : ""}>${esc(l)}</option>`).join("");

/* ============ Cache ============ */

const cache = { clients: [], boats: [], warehouses: [], items: [], settings: null };
async function loadClients() { cache.clients = await api("/clients"); return cache.clients; }
async function loadBoats() { cache.boats = await api("/boats"); return cache.boats; }
async function loadWarehouses() { cache.warehouses = await api("/warehouses"); return cache.warehouses; }
async function loadItems() { cache.items = await api("/items"); return cache.items; }
async function loadSettings() { cache.settings = await api("/settings"); return cache.settings; }

/* ---- Tendine configurabili (Impostazioni → Liste personalizzate) ---- */

let LOOKUPS = {};  // { categoria: [valori] }

const LOOKUP_LABELS = {
  tipo_cliente: "Tipologia cliente",
  categoria_lavoro: "Categorie lavori",
  tipo_imbarcazione: "Tipi imbarcazione",
  materiale_scafo: "Materiali scafo",
  alimentazione: "Alimentazioni",
  ruolo_lavoratore: "Ruoli lavoratori",
};
const lookupLabel = cat => LOOKUP_LABELS[cat] || cat.replace(/_/g, " ");
const lookupValues = cat => (LOOKUPS[cat] && LOOKUPS[cat].length ? LOOKUPS[cat] : []);

async function loadLookups() {
  try { LOOKUPS = await api("/lookups"); }
  catch { LOOKUPS = {}; }
  renderDatalists();
}

// crea/aggiorna i <datalist> globali usati dai campi tipo "combo"
function renderDatalists() {
  const box = $("#datalists");
  if (!box) return;
  box.innerHTML = Object.keys({ ...LOOKUP_LABELS, ...LOOKUPS }).map(cat =>
    `<datalist id="dl-${cat}">${lookupValues(cat).map(v => `<option value="${esc(v)}">`).join("")}</datalist>`
  ).join("");
}

async function loadLookupsFull() {  // per Impostazioni: serve anche l'id di ogni voce
  const rows = await api("/lookups/full");
  const grouped = {};
  for (const r of rows) (grouped[r.category] = grouped[r.category] || []).push(r);
  return grouped;
}

const clientName = id => (cache.clients.find(c => c.id === id) || {}).name || ("#" + id);
const boatName = id => { const b = cache.boats.find(x => x.id === id); return b ? b.name : "—"; };

const insuranceBadge = date => {
  if (!date) return `<span class="badge badge-gray">Senza polizza</span>`;
  const days = Math.round((new Date(date) - new Date(todayISO())) / 86400000);
  if (days < 0) return `<span class="badge badge-red">Scaduta da ${-days} gg</span>`;
  if (days <= 30) return `<span class="badge badge-amber">Scade tra ${days} gg</span>`;
  return `<span class="badge badge-green">Valida</span>`;
};
// badge generico per scadenze (patenti, visite, servizi…)
const expiryBadge = (date, okLabel = "Ok") => {
  if (!date) return "";
  const days = Math.round((new Date(date) - new Date(todayISO())) / 86400000);
  if (days < 0) return `<span class="badge badge-red">scaduta da ${-days} gg</span>`;
  if (days <= 30) return `<span class="badge badge-amber">tra ${days} gg</span>`;
  return `<span class="badge badge-green">${okLabel}</span>`;
};
// colonne di scadenza attive di un lavoratore (solo se scadute o imminenti)
const workerExpiryBadges = w => {
  const items = [
    ["license_expiry", "Patente"],
    ["medical_exam_expiry", "Visita"],
    ["safety_training_expiry", "Sicurezza"],
  ].map(([k, label]) => {
    const b = expiryBadge(w[k]);
    return b ? b.replace("</span>", ` — ${label}</span>`) : "";
  }).filter(Boolean);
  const problematic = items.filter(b => b.includes("badge-red") || b.includes("badge-amber"));
  return problematic.length ? problematic.join(" ") : `<span class="badge badge-green">Scadenze ok</span>`;
};

/* ============ Modale ============ */

function openModal(html, wide = false) {
  const box = $("#modal-box");
  box.className = "modal" + (wide ? " wide" : "");
  box.innerHTML = html;
  $("#modal-root").classList.remove("hidden");
}
function closeModal() {
  $("#modal-root").classList.add("hidden");
  $("#modal-box").innerHTML = "";
}
$("#modal-root").addEventListener("click", e => { if (e.target === e.currentTarget) closeModal(); });

function confirmDialog(message, onConfirm, confirmLabel = "Elimina") {
  openModal(`
    <h2>Conferma</h2>
    <p style="margin-bottom:6px">${esc(message)}</p>
    <div class="modal-actions">
      <button class="btn" id="cf-cancel">Annulla</button>
      <button class="btn btn-danger" id="cf-ok">${esc(confirmLabel)}</button>
    </div>`);
  $("#cf-cancel").onclick = closeModal;
  $("#cf-ok").onclick = async () => { closeModal(); await onConfirm(); };
}

function showError(err) {
  const box = $("#mf-error");
  if (box) { box.textContent = err.message; box.classList.remove("hidden"); }
  else toast(err.message, "error");
}

function modalForm({ title, wide, body, onSubmit, submitLabel = "Salva" }) {
  openModal(`
    <h2>${esc(title)}</h2>
    <form id="mf-form">${body}
      <div class="form-error hidden" id="mf-error"></div>
      <div class="modal-actions">
        <button type="button" class="btn" id="mf-cancel">Annulla</button>
        <button class="btn btn-primary">${esc(submitLabel)}</button>
      </div>
    </form>`, wide);
  $("#mf-cancel").onclick = closeModal;
  $("#mf-form").onsubmit = async e => {
    e.preventDefault();
    try { await onSubmit(new FormData(e.target)); }
    catch (err) { showError(err); }
  };
}

const field = (name, label, opts = {}) => {
  const { type = "text", value = "", required, full, placeholder, min, step, disabled, id } = opts;
  const val = esc(value ?? "");
  const idAttr = id ? ` id="${id}"` : "";
  if (type === "textarea") return `<label class="field ${full ? "full" : ""}">${label}${required ? ' <span class="req">*</span>' : ""}
    <textarea name="${name}"${idAttr} placeholder="${esc(placeholder || "")}" ${required ? "required" : ""} ${disabled ? "disabled" : ""}>${val}</textarea></label>`;
  if (type === "select") {
    return `<label class="field ${full ? "full" : ""}">${label}${required ? ' <span class="req">*</span>' : ""}
      <select name="${name}"${idAttr} ${required ? "required" : ""} ${disabled ? "disabled" : ""}>${opts.options}</select></label>`;
  }
  // combo: input libero con suggerimenti da una tendina configurabile
  if (type === "combo") {
    return `<label class="field ${full ? "full" : ""}">${label}${required ? ' <span class="req">*</span>' : ""}
      <input name="${name}"${idAttr} type="text" list="dl-${opts.list || ""}" value="${val}" placeholder="${esc(placeholder || "")}" ${required ? "required" : ""} ${disabled ? "disabled" : ""}></label>`;
  }
  return `<label class="field ${full ? "full" : ""}">${label}${required ? ' <span class="req">*</span>' : ""}
    <input name="${name}"${idAttr} type="${type}" value="${val}" placeholder="${esc(placeholder || "")}" ${min != null ? `min="${min}"` : ""} ${step != null ? `step="${step}"` : ""} ${required ? "required" : ""} ${disabled ? "disabled" : ""}></label>`;
};

/* ============ Router ============ */

const routes = [];
function route(pattern, handler) { routes.push({ pattern, handler }); }

let renderSeq = 0;
async function render() {
  if (!CURRENT_USER) {
    $("#app-screen").classList.add("hidden");
    $("#login-screen").classList.remove("hidden");
    return;
  }
  const seq = ++renderSeq;
  const hash = location.hash.replace(/^#/, "") || "/dashboard";
  for (const r of routes) {
    const m = hash.match(r.pattern);
    if (m) {
      const seg = hash.split("/")[1] || "dashboard";
      markNav(seg);
      try { await r.handler(...m.slice(1)); }
      catch (err) { toast(err.message, "error"); console.error(err); }
      if (seq === renderSeq) window.scrollTo(0, 0);
      return;
    }
  }
  location.hash = "#/dashboard";
}

function markNav(section) {
  $$(".sidebar-nav a").forEach(a => a.classList.toggle("active", a.dataset.nav === section));
}

window.addEventListener("hashchange", render);

/* ============ Login / logout ============ */

function showApp() {
  $("#login-screen").classList.add("hidden");
  $("#app-screen").classList.remove("hidden");
  $("#sidebar-user").innerHTML = `${esc(CURRENT_USER.username)}<small>${esc(CURRENT_USER.role === "admin" ? "Amministratore" : CURRENT_USER.role === "manager" ? "Manager" : "Operatore")}</small>`;
  $("#topbar-user").innerHTML = `<b>${esc(CURRENT_USER.username)}</b>`;
}

function doLogout(showMsg = true) {
  TOKEN = "";
  localStorage.removeItem("cn_token");
  CURRENT_USER = null;
  $("#app-screen").classList.add("hidden");
  $("#login-screen").classList.remove("hidden");
  if (showMsg) toast("Sessione terminata");
}

$("#logout-btn").addEventListener("click", () => doLogout());

$("#login-form").addEventListener("submit", async e => {
  e.preventDefault();
  const errBox = $("#login-error");
  errBox.classList.add("hidden");
  try {
    const body = new URLSearchParams({
      username: $("#login-username").value.trim(),
      password: $("#login-password").value,
    });
    const res = await fetch("/auth/token", { method: "POST", body });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Credenziali non valide");
    TOKEN = data.access_token;
    localStorage.setItem("cn_token", TOKEN);
    CURRENT_USER = await api("/auth/me");
    showApp();
    await Promise.all([loadSettings(), loadLookups()]);
    location.hash = "#/dashboard";
    render();
  } catch (err) {
    errBox.textContent = err.message;
    errBox.classList.remove("hidden");
  }
});

/* ============ Ricerca globale ============ */

let searchTimer = null;
$("#global-search").addEventListener("input", e => {
  clearTimeout(searchTimer);
  const q = e.target.value.trim();
  if (q.length < 2) { $("#search-results").classList.add("hidden"); return; }
  searchTimer = setTimeout(async () => {
    try {
      const res = await api("/search?q=" + encodeURIComponent(q));
      const box = $("#search-results");
      const items = [];
      const add = (label, arr, icon_name) => {
        if (arr.length) {
          items.push(`<div class="sr-group">${label}</div>`);
          arr.forEach(r => items.push(`<a class="sr-item" href="${r.href}">${icon(icon_name, 14)} ${esc(r.label)}</a>`));
        }
      };
      add("Clienti", res.clients.map(c => ({ ...c, href: "#/clienti/" + c.id })), "users");
      add("Imbarcazioni", res.boats.map(b => ({ ...b, href: "#/imbarcazioni/" + b.id })), "anchor");
      add("Commesse", res.projects.map(p => ({ ...p, href: "#/commesse/" + p.id })), "clipboard");
      add("Documenti", res.documents.map(d => ({ ...d, href: "#/documenti/" + d.id })), "file");
      box.innerHTML = items.length ? items.join("") : `<div class="sr-empty">Nessun risultato per “${esc(q)}”</div>`;
      box.classList.remove("hidden");
    } catch { /* silenzioso */ }
  }, 220);
});
$("#global-search").addEventListener("keydown", e => { if (e.key === "Escape") $("#search-results").classList.add("hidden"); });
document.addEventListener("click", e => {
  if (!e.target.closest(".search-wrap")) $("#search-results").classList.add("hidden");
});

/* ============ Dashboard ============ */

route(/^\/dashboard$/, async () => {
  const [d] = await Promise.all([api("/dashboard"), loadClients(), loadBoats()]);
  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("dashboard")} Dashboard</h1><div class="sub">Panoramica dell'attività del cantiere</div></div>
      <div class="head-actions">
        <button class="btn" id="qa-client">${icon("plus", 14)} Cliente</button>
        <button class="btn" id="qa-project">${icon("plus", 14)} Commessa</button>
        <button class="btn btn-primary" id="qa-doc">${icon("plus", 14)} Documento</button>
      </div>
    </div>

    ${CURRENT_USER.default_password ? `<div class="alert-banner bad">${icon("alert", 16)} Stai usando la password predefinita: cambiala subito. <a href="#/impostazioni" style="margin-left:auto;color:inherit">Vai a Impostazioni →</a></div>` : ""}
    ${(cache.settings && (!cache.settings.company_vat || cache.settings.company_vat === "00000000000" || !cache.settings.company_address)) ? `<div class="alert-banner">${icon("alert", 16)} Completa i dati azienda (P.IVA, indirizzo): servono su documenti e fattura elettronica. <a href="#/impostazioni" style="margin-left:auto;color:inherit">Completa →</a></div>` : ""}
    ${d.payables_overdue_count ? `<div class="alert-banner bad">${icon("alert", 16)} ${d.payables_overdue_count} fattur${d.payables_overdue_count === 1 ? "a fornitore scaduta" : "e fornitori scadute"} da pagare — totale ${fmtEur(d.payables_overdue_total)} <a href="#/acquisti" style="margin-left:auto;color:inherit">Apri acquisti →</a></div>` : ""}
    ${d.overdue_count ? `<div class="alert-banner bad">${icon("alert", 16)} ${d.overdue_count} fattur${d.overdue_count === 1 ? "a" : "e"} scadut${d.overdue_count === 1 ? "a" : "e"} non saldat${d.overdue_count === 1 ? "a" : "e"} — totale ${fmtEur(d.overdue_total)} <a href="#/scadenzario" style="margin-left:auto;color:inherit">Apri lo scadenzario →</a></div>` : ""}

    <div class="stats-grid">
      <div class="stat"><div class="label">Clienti attivi</div><div class="value">${fmtNum(d.clients)}</div><div class="hint">${d.inactive_clients ? d.inactive_clients + " disattivati" : "&nbsp;"}</div></div>
      <div class="stat"><div class="label">Imbarcazioni</div><div class="value">${fmtNum(d.boats)}</div></div>
      <div class="stat"><div class="label">Commesse aperte</div><div class="value">${fmtNum(d.open_projects)}</div><div class="hint">su ${fmtNum(d.total_projects)} totali</div></div>
      <div class="stat bad"><div class="label">Da incassare</div><div class="value money">${fmtEur(d.to_collect)}</div><div class="hint">fatture non saldate</div></div>
      <div class="stat good"><div class="label">Fatturato ${new Date().getFullYear()}</div><div class="value money">${fmtEur(d.invoiced_year)}</div><div class="hint">totale storico ${fmtEur(d.invoiced)}</div></div>
      <div class="stat warn"><div class="label">Da pagare fornitori</div><div class="value money">${fmtEur(d.to_pay)}</div><div class="hint">fatture di acquisto aperte</div></div>
      <div class="stat good"><div class="label">Incassato</div><div class="value money">${fmtEur(d.collected)}</div></div>
      <div class="stat"><div class="label">Valore magazzino</div><div class="value money">${fmtEur(d.inventory_value)}</div><div class="hint">a costo</div></div>
    </div>

    <div class="grid-2">
      <div class="card">
        <h2>${icon("alert", 15)} Fatture scadute</h2>
        <table class="tbl"><tbody>
          ${d.overdue.length ? d.overdue.map(r => `
            <tr>
              <td><a href="#/documenti/${r.id}">${esc(r.number)}</a><span class="sub">${esc(r.client_name)}</span></td>
              <td>${fmtDate(r.due_date)}</td>
              <td class="num"><b>${fmtEur(r.residual)}</b></td>
              <td class="num"><span class="badge badge-red">${r.days_overdue} gg</span></td>
            </tr>`).join("") : `<tr class="empty-row"><td>Nessuna fattura scaduta 🎉</td></tr>`}
        </tbody></table>
      </div>
      <div class="card">
        <h2>${icon("calendar", 15)} Scali in arrivo (15 gg)</h2>
        <table class="tbl"><tbody>
          ${d.agenda_alerts.length ? d.agenda_alerts.map(b => `
            <tr>
              <td>${fmtDate(b.start_date)} → ${fmtDate(b.end_date)}<span class="sub">${esc(b.resource_name)}</span></td>
              <td class="primary">${esc(b.title)}</td>
              <td>${badge(BOOKING_STATUS, b.status)}</td>
            </tr>`).join("") : `<tr class="empty-row"><td>Nessuno scalo pianificato — <a href="#/agenda">apri l'agenda</a></td></tr>`}
        </tbody></table>
      </div>
    </div>

    <div class="card">
      <h2>${icon("alert", 15)} Scadenze in arrivo (60 gg)</h2>
      <table class="tbl"><tbody>
        ${d.expiries.length ? d.expiries.map(e => `
          <tr>
            <td class="primary">${esc(e.label)}<span class="sub">${e.kind === "barca" ? "Imbarcazione" : "Lavoratore"}</span></td>
            <td class="num">${fmtDate(e.date)}</td>
            <td>${expiryBadge(e.date)}</td>
            <td class="num"><a href="#${esc(e.ref)}">Apri →</a></td>
          </tr>`).join("") : `<tr class="empty-row"><td>Nessuna scadenza vicina — assicurazioni, servizi, patenti e visite sotto controllo 👍</td></tr>`}
      </tbody></table>
    </div>

    <div class="grid-2">
      <div class="card">
        <h2>${icon("box", 15)} Articoli sotto scorta</h2>
        <table class="tbl"><tbody>
          ${d.low_stock.length ? d.low_stock.map(a => `
            <tr>
              <td class="primary">${esc(a.name)}</td>
              <td class="num">${fmtNum(a.total_qty)} ${esc(a.unit)}</td>
              <td class="num"><span class="badge badge-red">min. ${fmtNum(a.min_stock)}</span></td>
              <td class="num"><a href="#/acquisti">Ordina →</a></td>
            </tr>`).join("") : `<tr class="empty-row"><td>Tutte le scorte ok 👍</td></tr>`}
        </tbody></table>
      </div>
      <div class="card">
        <h2>${icon("clipboard", 15)} Commesse in scadenza (15 gg)</h2>
        <table class="tbl"><tbody>
          ${d.upcoming.length ? d.upcoming.map(p => `
            <tr>
              <td><a href="#/commesse/${p.id}">${esc(p.number)}</a><span class="sub">${esc(p.title)}</span></td>
              <td>${esc(p.client_name)}</td>
              <td class="num">${fmtDate(p.due_date)}</td>
              <td class="num">${p.days_left < 0 ? `<span class="badge badge-red">in ritardo</span>` : `<span class="badge badge-amber">${p.days_left} gg</span>`}</td>
            </tr>`).join("") : `<tr class="empty-row"><td>Nessuna scadenza vicina</td></tr>`}
        </tbody></table>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <h2>${icon("clipboard", 15)} Ultime commesse</h2>
        <table class="tbl">
          <thead><tr><th>Numero</th><th>Cliente</th><th>Stato</th><th class="num"></th></tr></thead>
          <tbody>
            ${d.recent_projects.length ? d.recent_projects.map(p => `
              <tr>
                <td><a href="#/commesse/${p.id}">${esc(p.number)}</a><span class="sub">${esc(p.title)}</span></td>
                <td>${esc(p.client_name || clientName(p.client_id))}</td>
                <td>${badge(PROJECT_STATUS, p.status)}</td>
                <td class="num"><a href="#/commesse/${p.id}">Apri →</a></td>
              </tr>`).join("") : `<tr class="empty-row"><td colspan="4">Nessuna commessa</td></tr>`}
          </tbody>
        </table>
      </div>
      <div class="card">
        <h2>${icon("file", 15)} Ultimi documenti</h2>
        <table class="tbl">
          <thead><tr><th>Numero</th><th>Cliente</th><th>Stato</th><th class="num">Totale</th></tr></thead>
          <tbody>
            ${d.recent_documents.length ? d.recent_documents.map(x => `
              <tr>
                <td><a href="#/documenti/${x.id}">${esc(x.number)}</a><span class="sub">${esc(x.kind)}</span></td>
                <td>${esc(x.client_name)}</td>
                <td>${badge(DOC_STATUS, x.status)}</td>
                <td class="num"><b>${fmtEur(x.total)}</b></td>
              </tr>`).join("") : `<tr class="empty-row"><td colspan="4">Nessun documento</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>`;
  $("#qa-client").onclick = () => clientModal();
  $("#qa-project").onclick = () => projectModal();
  $("#qa-doc").onclick = () => documentModal();
});

/* ============ Clienti ============ */

let clientFilterActive = 1; // 1 attivi, 0 disattivati, -1 tutti

route(/^\/clienti$/, async () => {
  const qs = new URLSearchParams();
  if (clientFilterActive >= 0) qs.set("active", clientFilterActive);
  const clients = await api("/clients" + (qs.toString() ? "?" + qs.toString() : ""));
  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("users")} Clienti</h1><div class="sub">${clients.length} anagrafiche</div></div>
      <div class="head-actions">
        <button class="btn" id="export-clients">${icon("download", 14)} CSV</button>
        <button class="btn btn-primary" id="add-client">${icon("plus", 14)} Nuovo cliente</button>
      </div>
    </div>
    <div class="card">
      <div class="tabs" id="cl-tabs">
        <button data-v="1" class="${clientFilterActive === 1 ? "active" : ""}">Attivi</button>
        <button data-v="0" class="${clientFilterActive === 0 ? "active" : ""}">Disattivati</button>
        <button data-v="-1" class="${clientFilterActive === -1 ? "active" : ""}">Tutti</button>
        <div class="spacer" style="flex:1"></div>
        <input type="text" id="client-search" placeholder="Cerca nome, codice, P.IVA, città…" style="margin-bottom:6px">
      </div>
      <table class="tbl" id="client-table">
        <thead><tr><th>Codice</th><th>Cliente</th><th>Contatti</th><th>Sede</th><th>Stato</th><th class="num">Azioni</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>`;

  const paint = (filter = "") => {
    const f = filter.toLowerCase();
    const rows = clients.filter(c =>
      !f || [c.name, c.code, c.vat, c.tax_code, c.email, c.city, c.phone].some(v => (v || "").toLowerCase().includes(f)));
    $("#client-table tbody").innerHTML = rows.length ? rows.map(c => `
      <tr>
        <td><span class="badge badge-gray">${esc(c.code || "—")}</span></td>
        <td class="primary"><a href="#/clienti/${c.id}">${esc(c.name)}</a><span class="sub">${esc(c.client_type)}${c.referente ? " · " + esc(c.referente) : ""}</span></td>
        <td>${esc(c.email || "—")}${c.phone ? `<span class="sub">${esc(c.phone)}</span>` : ""}</td>
        <td>${esc([c.zip, c.city, c.province].filter(Boolean).join(" ") || "—")}</td>
        <td>${c.active ? `<span class="badge badge-green">Attivo</span>` : `<span class="badge badge-gray">Disattivo</span>`}</td>
        <td class="num"><div class="actions">
          <a class="btn btn-sm" href="#/clienti/${c.id}">${icon("eye", 13)} Apri</a>
          <button class="btn btn-sm" data-edit="${c.id}">${icon("edit", 13)}</button>
        </div></td>
      </tr>`).join("") : `<tr class="empty-row"><td colspan="6">Nessun cliente</td></tr>`;
    $$("[data-edit]", $("#client-table")).forEach(b => b.onclick = () => clientModal(clients.find(c => c.id == b.dataset.edit)));
  };
  paint();
  $("#client-search").oninput = e => paint(e.target.value);
  $$("#cl-tabs button").forEach(b => b.onclick = () => { clientFilterActive = parseInt(b.dataset.v); render(); });
  $("#add-client").onclick = () => clientModal();
  $("#export-clients").onclick = () => downloadFile("/clients/export", "clienti.csv");
});

function clientModal(client = null, onSaved = null) {
  const c = client || {};
  modalForm({
    title: client ? `Modifica cliente ${esc(client.code || "")}` : "Nuovo cliente",
    wide: true,
    body: `
      <div class="form-section">Dati principali</div>
      <div class="form-grid">
        ${field("name", "Nome / Ragione sociale", { required: true, value: c.name, full: true })}
        ${field("client_type", "Tipologia", { type: "combo", list: "tipo_cliente", value: c.client_type || "Privato" })}
        ${field("referente", "Referente", { value: c.referente })}
      </div>
      <div class="form-section">Dati fiscali</div>
      <div class="form-grid">
        ${field("vat", "Partita IVA", { value: c.vat, placeholder: "IT…" })}
        ${field("tax_code", "Codice fiscale", { value: c.tax_code })}
        ${field("email", "Email", { type: "email", value: c.email })}
        ${field("pec", "PEC", { type: "email", value: c.pec })}
        ${field("sdi_code", "Codice destinatario SdI", { value: c.sdi_code, placeholder: "7 caratteri (fatt. elettronica)" })}
      </div>
      <div class="form-section">Contatti</div>
      <div class="form-grid">
        ${field("phone", "Telefono", { value: c.phone })}
        ${field("mobile", "Cellulare", { value: c.mobile })}
        ${field("secondary_phone", "Secondo telefono", { value: c.secondary_phone })}
        ${field("website", "Sito web", { value: c.website, placeholder: "www…" })}
      </div>
      <div class="form-section">Sede</div>
      <div class="form-grid">
        ${field("address", "Indirizzo (via)", { value: c.address, full: true })}
        ${field("zip", "CAP", { value: c.zip })}
        ${field("city", "Città", { value: c.city })}
        ${field("province", "Provincia", { value: c.province })}
        ${field("country", "Nazione", { value: c.country ?? "Italia" })}
        ${field("ship_to", "Indirizzo di spedizione (per DDT)", { value: c.ship_to, full: true, placeholder: "Se diverso dalla sede" })}
      </div>
      <div class="form-section">Amministrazione</div>
      <div class="form-grid">
        ${field("iban", "IBAN", { value: c.iban, full: true })}
        ${field("payment_terms", "Condizioni di pagamento", { value: c.payment_terms, placeholder: "es. 30 gg data fattura (il numero imposta la scadenza)" })}
        ${field("discount", "Sconto abituale %", { type: "number", step: "any", min: 0, value: c.discount ?? 0 })}
        ${field("active", "Stato", { type: "select", options: `<option value="true" ${c.active !== false ? "selected" : ""}>Attivo</option><option value="false" ${c.active === false ? "selected" : ""}>Disattivo</option>` })}
        ${field("notes", "Note", { type: "textarea", value: c.notes, full: true })}
      </div>`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      payload.active = payload.active === "true";
      payload.discount = num(payload.discount);
      if (client) await api("/clients/" + client.id, { method: "PUT", json: payload });
      else await api("/clients", { method: "POST", json: payload });
      closeModal();
      toast(client ? "Cliente aggiornato" : "Cliente creato", "success");
      if (onSaved) onSaved(); else render();
    },
  });
}

/* ---- Scheda cliente ---- */

route(/^\/clienti\/(\d+)$/, async (id) => {
  const d = await api(`/clients/${id}/detail`);
  await loadBoats();
  const infoBox = (k, v) => `<div class="field-box"><div class="k">${k}</div><div class="v">${v || "—"}</div></div>`;
  const noteBox = (k, v) => `<div class="field-box wide"><div class="k">${k}</div><div class="v">${v || "—"}</div></div>`;

  $("#view").innerHTML = `
    <a class="back-link" href="#/clienti">${icon("arrowleft", 14)} Tutti i clienti</a>
    <div class="page-head">
      <div>
        <h1>${icon("users")} ${esc(d.name)} ${d.active ? "" : `<span class="badge badge-gray">Disattivo</span>`}</h1>
        <div class="doc-meta">
          <span class="badge badge-gray">${esc(d.code || "—")}</span>
          <span>${esc(d.client_type)}</span>
          <span>${esc([d.zip, d.city, d.province].filter(Boolean).join(" ") || "sede non indicata")}</span>
          ${d.email ? `<span>${esc(d.email)}</span>` : ""}
          ${d.phone ? `<span>${esc(d.phone)}</span>` : ""}
        </div>
      </div>
      <div class="head-actions">
        <button class="btn" id="c-edit">${icon("edit", 14)} Modifica</button>
        <button class="btn" id="c-boat">${icon("anchor", 14)} Imbarcazione</button>
        <button class="btn btn-primary" id="c-doc">${icon("plus", 14)} Documento</button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat"><div class="label">Imbarcazioni</div><div class="value">${fmtNum(d.stats.boats)}</div></div>
      <div class="stat"><div class="label">Commesse</div><div class="value">${fmtNum(d.stats.projects)}</div></div>
      <div class="stat"><div class="label">Documenti</div><div class="value">${fmtNum(d.stats.documents)}</div></div>
      <div class="stat good"><div class="label">Fatturato</div><div class="value money">${fmtEur(d.stats.invoiced)}</div></div>
      <div class="stat bad"><div class="label">Da incassare</div><div class="value money">${fmtEur(d.stats.to_collect)}</div></div>
    </div>

    <div class="card">
      <h2>${icon("clipboard", 15)} Anagrafica</h2>
      <div class="detail-grid">
        ${infoBox("Partita IVA", esc(d.vat))}
        ${infoBox("Codice fiscale", esc(d.tax_code))}
        ${infoBox("Referente", esc(d.referente))}
        ${infoBox("Email", esc(d.email))}
        ${infoBox("PEC", esc(d.pec))}
        ${infoBox("Telefono / Cell", esc([d.phone, d.mobile].filter(Boolean).join(" / ")))}
        ${infoBox("Indirizzo sede", esc([d.address, d.zip, d.city, d.province, d.country].filter(Boolean).join(", ")))}
        ${infoBox("Spedizione", esc(d.ship_to))}
        ${infoBox("IBAN", esc(d.iban))}
        ${infoBox("Pagamento", esc(d.payment_terms))}
        ${infoBox("Sconto abituale", d.discount ? esc(d.discount) + "%" : "")}
      </div>
      ${d.notes ? `<div class="detail-grid" style="margin-top:14px">${noteBox("Note", esc(d.notes))}</div>` : ""}
    </div>

    <div class="card">
      <h2>${icon("anchor", 15)} Imbarcazioni <span class="count">${d.boats.length}</span></h2>
      <table class="tbl">
        <thead><tr><th>Nome</th><th>Tipo</th><th>Immatricolazione</th><th>Assicurazione</th><th class="num"></th></tr></thead>
        <tbody>
          ${d.boats.length ? d.boats.map(b => `
            <tr>
              <td class="primary"><a href="#/imbarcazioni/${b.id}">${esc(b.name)}</a></td>
              <td>${esc(b.boat_type || "—")}</td>
              <td>${esc(b.registration || "—")}</td>
              <td>${insuranceBadge(b.insurance_expiry)}</td>
              <td class="num"><a href="#/imbarcazioni/${b.id}">Apri →</a></td>
            </tr>`).join("") : `<tr class="empty-row"><td>Nessuna imbarcazione</td></tr>`}
        </tbody>
      </table>
    </div>

    <div class="grid-2">
      <div class="card">
        <h2>${icon("clipboard", 15)} Commesse <span class="count">${d.projects.length}</span></h2>
        <table class="tbl">
          <tbody>
            ${d.projects.length ? d.projects.map(p => `
              <tr>
                <td><a href="#/commesse/${p.id}">${esc(p.number)}</a><span class="sub">${esc(p.title)}</span></td>
                <td>${badge(PROJECT_STATUS, p.status)}</td>
                <td class="num">${fmtDate(p.due_date)}</td>
              </tr>`).join("") : `<tr class="empty-row"><td>Nessuna commessa</td></tr>`}
          </tbody>
        </table>
      </div>
      <div class="card">
        <h2>${icon("file", 15)} Documenti <span class="count">${d.documents.length}</span></h2>
        <table class="tbl">
          <tbody>
            ${d.documents.length ? d.documents.map(x => `
              <tr>
                <td><a href="#/documenti/${x.id}">${esc(x.number)}</a><span class="sub">${esc(x.kind)} · ${fmtDate(x.date)}</span></td>
                <td>${badge(DOC_STATUS, x.status)}</td>
                <td class="num"><b>${fmtEur(x.total)}</b></td>
              </tr>`).join("") : `<tr class="empty-row"><td>Nessun documento</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>`;

  $("#c-edit").onclick = () => clientModal(d, () => render());
  $("#c-boat").onclick = () => boatModal(null, parseInt(id));
  $("#c-doc").onclick = () => documentModal(null, parseInt(id));
});

/* ============ Imbarcazioni ============ */

route(/^\/imbarcazioni$/, async () => {
  const [boats, clients] = await Promise.all([loadBoats(), loadClients()]);
  const soon = boats.filter(b => b.insurance_expiry && (new Date(b.insurance_expiry) - new Date(todayISO())) / 86400000 <= 30);
  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("anchor")} Imbarcazioni</h1><div class="sub">${boats.length} unità in anagrafica</div></div>
      <div class="head-actions"><button class="btn btn-primary" id="add-boat" ${clients.length ? "" : "disabled title='Aggiungi prima un cliente'"}>${icon("plus", 14)} Nuova imbarcazione</button></div>
    </div>
    ${soon.length ? `<div class="alert-banner warn">${icon("alert", 16)} ${soon.length} assicurazion${soon.length === 1 ? "e in scadenza/scaduta" : "i in scadenza o scadute"} — rivedi le schede sotto</div>` : ""}
    <div class="card">
      <div class="toolbar"><input type="text" id="boat-search" placeholder="Cerca per nome, cliente, immatricolazione…"></div>
      <table class="tbl" id="boat-table">
        <thead><tr><th>Imbarcazione</th><th>Cliente</th><th>Tipo / Lunghezza</th><th>Immatricolazione</th><th>Assicurazione</th><th class="num">Azioni</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>`;

  const paint = (filter = "") => {
    const f = filter.toLowerCase();
    const rows = boats.filter(b =>
      !f || [b.name, b.registration, b.boat_type, clientName(b.client_id), b.hull_id].some(v => (v || "").toLowerCase().includes(f)));
    $("#boat-table tbody").innerHTML = rows.length ? rows.map(b => `
      <tr>
        <td class="primary"><a href="#/imbarcazioni/${b.id}">${esc(b.name)}</a><span class="sub">${b.hull_id ? "Scafo " + esc(b.hull_id) : ""}</span></td>
        <td>${esc(clientName(b.client_id))}</td>
        <td>${esc(b.boat_type || "—")}${b.length ? `<span class="sub">${fmtNum(b.length)} m</span>` : ""}</td>
        <td>${esc(b.registration || "—")}</td>
        <td>${insuranceBadge(b.insurance_expiry)}</td>
        <td class="num"><div class="actions">
          <a class="btn btn-sm" href="#/imbarcazioni/${b.id}">${icon("eye", 13)} Apri</a>
          <button class="btn btn-sm" data-edit="${b.id}">${icon("edit", 13)}</button>
        </div></td>
      </tr>`).join("") : `<tr class="empty-row"><td colspan="6">Nessuna imbarcazione</td></tr>`;
    $$("[data-edit]", $("#boat-table")).forEach(btn => btn.onclick = () => boatModal(boats.find(x => x.id == btn.dataset.edit)));
  };
  paint();
  $("#boat-search").oninput = e => paint(e.target.value);
  $("#add-boat").onclick = () => boatModal();
});

function boatModal(boat = null, presetClientId = null, onSaved = null) {
  const b = boat || {};
  modalForm({
    title: boat ? `Modifica imbarcazione` : "Nuova imbarcazione",
    wide: true,
    body: `
      <div class="form-section">Dati principali</div>
      <div class="form-grid">
        ${field("client_id", "Proprietario", { type: "select", required: true, options: `<option value="">— scegli cliente —</option>` +
          cache.clients.map(c => `<option value="${c.id}" ${b.client_id === c.id || (!boat && presetClientId === c.id) ? "selected" : ""}>${esc(c.name)}</option>`).join("") })}
        ${field("name", "Nome imbarcazione", { required: true, value: b.name })}
        ${field("boat_type", "Tipo", { type: "combo", list: "tipo_imbarcazione", value: b.boat_type, placeholder: "Vela, Motore, Gommone…" })}
        ${field("model", "Modello", { value: b.model })}
        ${field("builder", "Cantiere / Costruttore", { value: b.builder })}
        ${field("build_year", "Anno di costruzione", { type: "number", min: 1900, max: 2100, value: b.build_year ?? "" })}
        ${field("flag", "Bandiera", { value: b.flag })}
        ${field("home_port", "Porto d'iscrizione", { value: b.home_port })}
        ${field("registration", "Immatricolazione", { value: b.registration })}
        ${field("hull_id", "Numero di scafo (HIN)", { value: b.hull_id })}
      </div>
      <div class="form-section">Scheda tecnica</div>
      <div class="form-grid">
        ${field("length", "Lunghezza (m)", { type: "number", step: "any", min: 0, value: b.length ?? "" })}
        ${field("beam", "Baglio (m)", { type: "number", step: "any", min: 0, value: b.beam ?? "" })}
        ${field("draft", "Pescaggio (m)", { type: "number", step: "any", min: 0, value: b.draft ?? "" })}
        ${field("displacement", "Dislocamento (t)", { type: "number", step: "any", min: 0, value: b.displacement ?? "" })}
        ${field("hull_material", "Materiale scafo", { type: "combo", list: "materiale_scafo", value: b.hull_material, placeholder: "VTR, alluminio, acciaio…" })}
        ${field("fuel_type", "Alimentazione", { type: "combo", list: "alimentazione", value: b.fuel_type, placeholder: "Diesel, benzina…" })}
      </div>
      <div class="form-section">Motore</div>
      <div class="form-grid">
        ${field("engine_make", "Marca motore", { value: b.engine_make, placeholder: "Volvo Penta, Yanmar…" })}
        ${field("engine_model", "Modello motore", { value: b.engine_model })}
        ${field("engine_power_hp", "Potenza (CV)", { type: "number", step: "any", min: 0, value: b.engine_power_hp ?? "" })}
        ${field("engine_hours", "Ore motore", { type: "number", step: "any", min: 0, value: b.engine_hours ?? "" })}
        ${field("engine", "Note motore", { value: b.engine, full: true })}
      </div>
      <div class="form-section">Assicurazione e manutenzione</div>
      <div class="form-grid">
        ${field("insurance_company", "Compagnia assicurazione", { value: b.insurance_company })}
        ${field("insurance_expiry", "Scadenza assicurazione", { type: "date", value: b.insurance_expiry || "" })}
        ${field("last_haul_out", "Ultimo varo / alaggio", { type: "date", value: b.last_haul_out || "" })}
        ${field("next_service_date", "Prossimo servizio", { type: "date", value: b.next_service_date || "" })}
        ${field("yard_position", "Posizione nello scalo", { value: b.yard_position, placeholder: "Bacino 2, alaggio est…" })}
        ${field("notes", "Note", { type: "textarea", value: b.notes, full: true })}
      </div>`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      payload.client_id = parseInt(payload.client_id);
      for (const k of ["length", "beam", "draft", "displacement", "engine_power_hp", "engine_hours"])
        payload[k] = payload[k] === "" ? null : num(payload[k]);
      payload.build_year = payload.build_year === "" ? null : parseInt(payload.build_year);
      for (const k of ["insurance_expiry", "last_haul_out", "next_service_date"])
        payload[k] = payload[k] || null;
      if (boat) await api("/boats/" + boat.id, { method: "PUT", json: payload });
      else await api("/boats", { method: "POST", json: payload });
      closeModal();
      toast("Imbarcazione salvata", "success");
      if (onSaved) onSaved(); else render();
    },
  });
}

/* ---- Scheda imbarcazione ---- */

route(/^\/imbarcazioni\/(\d+)$/, async (id) => {
  const d = await api(`/boats/${id}/detail`);
  const infoBox = (k, v) => `<div class="field-box"><div class="k">${k}</div><div class="v">${v || "—"}</div></div>`;
  $("#view").innerHTML = `
    <a class="back-link" href="#/imbarcazioni">${icon("arrowleft", 14)} Tutte le imbarcazioni</a>
    <div class="page-head">
      <div>
        <h1>${icon("anchor")} ${esc(d.name)}</h1>
        <div class="doc-meta">
          <span>Proprietario: <a href="#/clienti/${d.client_id}"><b>${esc(d.client_name)}</b></a></span>
          <span>${esc(d.boat_type || "tipo non indicato")}</span>
          ${insuranceBadge(d.insurance_expiry)}
        </div>
      </div>
      <div class="head-actions">
        <button class="btn" id="b-edit">${icon("edit", 14)} Modifica</button>
        <button class="btn btn-primary" id="b-project">${icon("plus", 14)} Commessa</button>
      </div>
    </div>

    ${d.insurance_expiry && (new Date(d.insurance_expiry) - new Date(todayISO())) / 86400000 <= 30
      ? `<div class="alert-banner warn">${icon("alert", 16)} Assicurazione in scadenza o scaduta il ${fmtDate(d.insurance_expiry)}</div>` : ""}

    ${d.next_service_date && (new Date(d.next_service_date) - new Date(todayISO())) / 86400000 <= 30
      ? `<div class="alert-banner warn">${icon("alert", 16)} Servizio programmato per il ${fmtDate(d.next_service_date)}</div>` : ""}

    <div class="card">
      <h2>${icon("anchor", 15)} Scheda tecnica</h2>
      <div class="detail-grid">
        ${infoBox("Tipo", esc(d.boat_type))}
        ${infoBox("Modello", esc(d.model))}
        ${infoBox("Cantiere", esc(d.builder))}
        ${infoBox("Anno di costruzione", d.build_year || "")}
        ${infoBox("Lunghezza", d.length ? fmtNum(d.length) + " m" : "")}
        ${infoBox("Baglio", d.beam ? fmtNum(d.beam) + " m" : "")}
        ${infoBox("Pescaggio", d.draft ? fmtNum(d.draft) + " m" : "")}
        ${infoBox("Dislocamento", d.displacement ? fmtNum(d.displacement) + " t" : "")}
        ${infoBox("Materiale scafo", esc(d.hull_material))}
        ${infoBox("Immatricolazione", esc(d.registration))}
        ${infoBox("Numero di scafo", esc(d.hull_id))}
        ${infoBox("Bandiera", esc(d.flag))}
        ${infoBox("Porto d'iscrizione", esc(d.home_port))}
        ${infoBox("Posizione nello scalo", esc(d.yard_position))}
        ${d.engine_make || d.engine_model || d.engine_power_hp ? infoBox("Motore",
          [d.engine_make, d.engine_model].filter(Boolean).join(" ") +
          (d.engine_power_hp ? ` — ${fmtNum(d.engine_power_hp)} CV` : "") +
          (d.engine_hours != null && d.engine_hours !== "" ? ` — ${fmtNum(d.engine_hours)} h` : "")) : ""}
        ${infoBox("Alimentazione", esc(d.fuel_type))}
        ${infoBox("Assicurazione", (d.insurance_company ? esc(d.insurance_company) + " — " : "") + fmtDate(d.insurance_expiry))}
        ${infoBox("Ultimo varo / alaggio", fmtDate(d.last_haul_out))}
        ${infoBox("Prossimo servizio", fmtDate(d.next_service_date))}
        ${d.notes ? infoBox("Note", esc(d.notes)) : ""}
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <h2>${icon("clipboard", 15)} Commesse <span class="count">${d.projects.length}</span></h2>
        <table class="tbl"><tbody>
          ${d.projects.length ? d.projects.map(p => `
            <tr>
              <td><a href="#/commesse/${p.id}">${esc(p.number)}</a><span class="sub">${esc(p.title)}</span></td>
              <td>${badge(PROJECT_STATUS, p.status)}</td>
              <td class="num">${fmtDate(p.due_date)}</td>
            </tr>`).join("") : `<tr class="empty-row"><td>Nessuna commessa</td></tr>`}
        </tbody></table>
      </div>
      <div class="card">
        <h2>${icon("file", 15)} Documenti <span class="count">${d.documents.length}</span></h2>
        <table class="tbl"><tbody>
          ${d.documents.length ? d.documents.map(x => `
            <tr>
              <td><a href="#/documenti/${x.id}">${esc(x.number)}</a><span class="sub">${esc(x.kind)} · ${fmtDate(x.date)}</span></td>
              <td>${badge(DOC_STATUS, x.status)}</td>
              <td class="num"><b>${fmtEur(x.total)}</b></td>
            </tr>`).join("") : `<tr class="empty-row"><td>Nessun documento</td></tr>`}
        </tbody></table>
      </div>
    </div>`;

  $("#b-edit").onclick = () => boatModal(d, null, () => render());
  $("#b-project").onclick = () => projectModal(null, null, null, parseInt(id));
});

/* ============ Commesse ============ */

route(/^\/commesse$/, async () => {
  const [projects, clients] = await Promise.all([api("/projects"), loadClients()]);
  await loadBoats();
  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("clipboard")} Commesse</h1><div class="sub">${projects.length} commesse</div></div>
      <div class="head-actions"><button class="btn btn-primary" id="add-project" ${clients.length ? "" : "disabled title='Aggiungi prima un cliente'"}>${icon("plus", 14)} Nuova commessa</button></div>
    </div>
    <div class="card">
      <div class="toolbar">
        <input type="text" id="proj-search" placeholder="Cerca numero o titolo…">
        <select id="proj-status"><option value="">Tutti gli stati</option>
          ${Object.entries(PROJECT_STATUS).map(([k, [l]]) => `<option value="${k}">${l}</option>`).join("")}</select>
      </div>
      <table class="tbl" id="proj-table">
        <thead><tr><th>Numero</th><th>Titolo</th><th>Cliente</th><th>Imbarcazione</th><th>Stato</th><th>Scadenza</th><th class="num">Azioni</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>`;

  const paint = (fq = "", fs = "") => {
    const f = fq.toLowerCase();
    const rows = projects.filter(p =>
      (!f || [p.number, p.title].some(v => (v || "").toLowerCase().includes(f))) && (!fs || p.status === fs));
    $("#proj-table tbody").innerHTML = rows.length ? rows.map(p => `
      <tr>
        <td><a href="#/commesse/${p.id}">${esc(p.number)}</a></td>
        <td class="primary">${esc(p.title)}</td>
        <td>${esc(clientName(p.client_id))}</td>
        <td>${esc(p.boat_id ? boatName(p.boat_id) : "—")}</td>
        <td>${badge(PROJECT_STATUS, p.status)}</td>
        <td>${fmtDate(p.due_date)}</td>
        <td class="num"><div class="actions">
          <a href="#/commesse/${p.id}" class="btn btn-sm">${icon("eye", 13)} Apri</a>
          <button class="btn btn-sm btn-danger" data-del="${p.id}">${icon("trash", 13)}</button>
        </div></td>
      </tr>`).join("") : `<tr class="empty-row"><td colspan="7">Nessuna commessa</td></tr>`;
    $$("[data-del]", $("#proj-table")).forEach(b => b.onclick = () => {
      const p = projects.find(x => x.id == b.dataset.del);
      confirmDialog(`Eliminare la commessa ${p.number}? Verranno rimossi anche lavori e allegati.`, async () => {
        try { await api("/projects/" + p.id, { method: "DELETE" }); toast("Commessa eliminata", "success"); render(); }
        catch (err) { toast(err.message, "error"); }
      });
    });
  };
  paint();
  $("#proj-search").oninput = e => paint(e.target.value, $("#proj-status").value);
  $("#proj-status").onchange = e => paint($("#proj-search").value, e.target.value);
  $("#add-project").onclick = () => projectModal();
});

function projectModal(project = null, onSaved = null, _unused = null, presetClientId = null) {
  const p = project || {};
  modalForm({
    title: project ? "Modifica commessa" : "Nuova commessa",
    body: `
      <div class="form-grid">
        ${field("client_id", "Cliente", { type: "select", required: true, id: "pj-client", options: `<option value="">— scegli —</option>` +
          cache.clients.filter(c => c.active !== false).map(c => `<option value="${c.id}" ${p.client_id === c.id || (!project && presetClientId === c.id) ? "selected" : ""}>${esc(c.name)}</option>`).join("") })}
        ${field("boat_id", "Imbarcazione", { type: "select", id: "pj-boat", options: `<option value="">— nessuna —</option>` })}
        ${field("title", "Titolo", { required: true, value: p.title, full: true, placeholder: "es. Rimessa in moto + antivegetativa" })}
        ${field("status", "Stato", { type: "select", options: Object.entries(PROJECT_STATUS).map(([k, [l]]) => `<option value="${k}" ${p.status === k ? "selected" : ""}>${l}</option>`).join("") })}
        ${field("start_date", "Data inizio", { type: "date", value: p.start_date || "" })}
        ${field("due_date", "Scadenza", { type: "date", value: p.due_date || "" })}
        ${field("notes", "Note", { type: "textarea", value: p.notes, full: true })}
      </div>`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      payload.client_id = parseInt(payload.client_id);
      payload.boat_id = payload.boat_id ? parseInt(payload.boat_id) : null;
      for (const k of ["start_date", "due_date"]) if (!payload[k]) payload[k] = null;
      if (project) await api("/projects/" + project.id, { method: "PUT", json: payload });
      else {
        const created = await api("/projects", { method: "POST", json: payload });
        closeModal(); toast("Commessa creata", "success");
        location.hash = "#/commesse/" + created.id;
        return;
      }
      closeModal(); toast("Commessa aggiornata", "success");
      if (onSaved) onSaved(); else render();
    },
  });

  const boatSel = $("#pj-boat");
  const fillBoats = () => {
    const cid = parseInt($("#pj-client").value);
    const boats = cache.boats.filter(b => b.client_id === cid);
    let options = boats.map(b => `<option value="${b.id}" ${p.boat_id === b.id ? "selected" : ""}>${esc(b.name)}</option>`).join("");
    if (p.boat_id && !boats.some(b => b.id === p.boat_id)) {
      options += `<option value="${p.boat_id}" selected>${esc(boatName(p.boat_id))}</option>`;
    }
    boatSel.innerHTML = `<option value="">— nessuna —</option>` + options;
  };
  fillBoats();
  $("#pj-client").onchange = fillBoats;
}

/* ---- Dettaglio commessa ---- */

route(/^\/commesse\/(\d+)$/, async (id) => {
  const project = await api("/projects").then(list => list.find(p => p.id === parseInt(id)));
  if (!project) { $("#view").innerHTML = `<p>Commessa non trovata</p>`; return; }

  const jobs = await api(`/projects/${id}/jobs`);
  const projMovs = await api(`/projects/${id}/movements`);
  const timesheets = await api(`/projects/${id}/timesheets`);
  const sum = await api(`/projects/${id}/summary`);
  const [allDocs] = await Promise.all([api("/documents"), loadClients()]);
  const linkedDocs = allDocs.filter(d => d.project_id === project.id);
  await loadBoats();


  $("#view").innerHTML = `
    <a class="back-link" href="#/commesse">${icon("arrowleft", 14)} Tutte le commesse</a>
    <div class="page-head">
      <div>
        <h1>${icon("clipboard")} ${esc(project.number)} — ${esc(project.title)}</h1>
        <div class="doc-meta">
          ${badge(PROJECT_STATUS, project.status)}
          <span>Cliente: <a href="#/clienti/${project.client_id}"><b>${esc(clientName(project.client_id))}</b></a></span>
          <span>Imbarcazione: ${esc(project.boat_id ? boatName(project.boat_id) : "—")}</span>
          <span>Inizio: ${fmtDate(project.start_date)}</span>
          <span>Scadenza: ${fmtDate(project.due_date)}</span>
        </div>
        ${project.notes ? `<div class="doc-meta">${esc(project.notes)}</div>` : ""}
      </div>
      <div class="head-actions">
        <select id="p-status">
          ${Object.entries(PROJECT_STATUS).map(([k, [l]]) => `<option value="${k}" ${project.status === k ? "selected" : ""}>${l}</option>`).join("")}
        </select>
        <button class="btn" id="p-edit">${icon("edit", 14)} Modifica</button>
        <button class="btn" id="p-mkdoc-Proforma">${icon("file", 14)} Proforma</button>
        <button class="btn btn-primary" id="p-mkdoc-Fattura">${icon("file", 14)} Fattura</button>
        <button class="btn" id="p-mkdoc-DDT">${icon("file", 14)} DDT</button>
        <button class="btn btn-danger" id="p-del">${icon("trash", 14)}</button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat good"><div class="label">Valore lavori</div><div class="value money">${fmtEur(sum.revenue)}</div><div class="hint">${fmtNum(sum.jobs)} lavori a prezzo</div></div>
      <div class="stat warn"><div class="label">Costi</div><div class="value money">${fmtEur(sum.total_cost)}</div><div class="hint">preventivo ${fmtEur(sum.estimated_cost)}</div></div>
      <div class="stat ${sum.margin >= 0 ? "good" : "bad"}"><div class="label">Margine</div><div class="value money">${fmtEur(sum.margin)}</div><div class="hint">${sum.margin_pct != null ? fmtNum(sum.margin_pct) + "% del valore" : "&nbsp;"}</div></div>
      <div class="stat"><div class="label">Ore</div><div class="value">${fmtNum(sum.hours)}</div><div class="hint">preventivate ${fmtNum(sum.budget_hours)}</div></div>
      <div class="stat"><div class="label">Da fatturare</div><div class="value money">${fmtEur(sum.to_invoice)}</div><div class="hint">già fatturato ${fmtEur(sum.invoiced)}</div></div>
    </div>
    <p style="color:var(--muted);font-size:12.5px;margin:-6px 0 14px">Costi: manodopera ${fmtEur(sum.labor_cost)} (${sum.labor_source}) · materiali ${fmtEur(sum.material_cost)} (${sum.material_source})${sum.other_cost ? " · altri costi " + fmtEur(sum.other_cost) : ""}. Dove esiste il consuntivo si usa quello, altrimenti il preventivo dei lavori.</p>

    <div class="card">
      <h2>${icon("clipboard", 15)} Lavori <span class="count">${jobs.length}</span></h2>
      <table class="tbl">
        <thead><tr><th>Descrizione</th><th>Categoria</th><th>Stato</th><th class="num">Qtà</th><th class="num">Costo</th><th class="num">Prezzo</th><th class="num">Totale</th><th>Assegnato a</th><th class="num">Azioni</th></tr></thead>
        <tbody id="jobs-body">
          ${jobs.length ? jobs.map(j => `
            <tr>
              <td class="primary">${esc(j.description)}</td>
              <td>${esc(j.category)}</td>
              <td>${badge(JOB_STATUS, j.status)}${j.priority && j.priority !== "normale" ? ` <span class="badge ${j.priority === "urgente" ? "badge-red" : "badge-amber"}">${esc(j.priority)}</span>` : ""}</td>
              <td class="num">${fmtNum(j.qty)} ${esc(j.unit)}</td>
              <td class="num">${fmtEur(j.unit_cost)}</td>
              <td class="num">${fmtEur(j.unit_price)}</td>
              <td class="num">${fmtEur((j.qty || 0) * (j.unit_price || 0))}</td>
              <td>${esc(j.assigned_to || "—")}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-jedit="${j.id}">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-jdel="${j.id}">${icon("trash", 13)}</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="9">Nessun lavoro registrato</td></tr>`}
        </tbody>
      </table>
      <div style="margin-top:12px"><button class="btn btn-primary btn-sm" id="add-job">${icon("plus", 13)} Aggiungi lavoro</button></div>
    </div>

    <div class="card">
      <h2>${icon("box", 15)} Materiali movimentati <span class="count">${projMovs.length}</span></h2>
      <table class="tbl">
        <thead><tr><th>Data</th><th>Tipo</th><th>Articolo</th><th>Magazzino</th><th class="num">Qtà</th><th class="num">Costo unit.</th><th class="num">Totale costo</th><th>Note</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${projMovs.length ? projMovs.map(x => `
            <tr>
              <td>${fmtDate(x.date)}</td>
              <td>${badge(MOV_TYPE, x.type)}</td>
              <td class="primary">${esc(x.item)}</td>
              <td>${esc(x.warehouse)}</td>
              <td class="num">${fmtNum(x.qty)}</td>
              <td class="num">${fmtEur(x.unit_cost)}</td>
              <td class="num"><b>${fmtEur(x.qty * x.unit_cost)}</b></td>
              <td>${esc(x.note || "")}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-pmedit="${x.id}" title="Modifica">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-pmdel="${x.id}" title="Elimina">${icon("trash", 13)}</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="9">Nessun articolo movimentato su questa commessa</td></tr>`}
        </tbody>
      </table>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-primary btn-sm" id="add-projmov">${icon("box", 13)} Scarica articolo da magazzino</button>
        <button class="btn btn-sm" id="add-projmov-generic">${icon("plus", 13)} Altro movimento</button>
      </div>
      <p style="color:var(--muted);font-size:12.5px;margin-top:10px">Lo scarico toglie le quantità dal magazzino e qui viene contabilizzato nei costi della commessa. I movimenti restano modificabili anche da Magazzino → Movimenti.</p>
    </div>

    <div class="card">
      <h2>${icon("clock", 15)} Ore lavorative <span class="count">${timesheets.entries.length}</span></h2>
      ${Object.keys(timesheets.by_worker).length ? `<p style="font-size:13px;color:var(--muted);margin-bottom:10px">Per persona: ${Object.entries(timesheets.by_worker).map(([w, s]) => `<b style="color:var(--text)">${esc(w)}</b> ${fmtNum(s.hours)} h${s.cost ? " · " + fmtEur(s.cost) : ""}`).join(" · ")}</p>` : ""}
      <table class="tbl">
        <thead><tr><th>Data</th><th>Lavoratore</th><th>Lavoro</th><th class="num">Ore</th><th class="num">Costo</th><th>Note</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${timesheets.entries.length ? timesheets.entries.map(t => `
            <tr>
              <td>${fmtDate(t.date)}</td>
              <td class="primary">${esc(t.worker_name || "—")}${t.hourly_cost ? `<span class="sub">${fmtEur(t.hourly_cost)}/h</span>` : ""}</td>
              <td>${esc(t.job_description || "—")}</td>
              <td class="num"><b>${fmtNum(t.hours)}</b></td>
              <td class="num">${t.hourly_cost ? `<b>${fmtEur(t.hours * t.hourly_cost)}</b>` : "—"}</td>
              <td>${esc(t.notes || "")}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-tedit="${t.id}">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-tdel="${t.id}">${icon("trash", 13)}</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="7">Nessuna ora registrata</td></tr>`}
        </tbody>
      </table>
      <div style="margin-top:12px"><button class="btn btn-primary btn-sm" id="add-time">${icon("plus", 13)} Registra ore</button></div>
    </div>

    <div class="card">
      <h2>${icon("archive", 15)} Allegati</h2>
      <div class="toolbar">
        <input type="file" id="att-file">
        <button class="btn btn-sm btn-primary" id="att-upload">${icon("upload", 13)} Carica allegato</button>
      </div>
      <table class="tbl"><tbody id="att-body"></tbody></table>
    </div>

    <div class="card">
      <h2>${icon("file", 15)} Documenti collegati <span class="count">${linkedDocs.length}</span></h2>
      <table class="tbl">
        <thead><tr><th>Numero</th><th>Tipo</th><th>Data</th><th>Stato</th><th class="num">Totale</th><th class="num"></th></tr></thead>
        <tbody>
          ${linkedDocs.length ? linkedDocs.map(x => `
            <tr>
              <td><a href="#/documenti/${x.id}">${esc(x.number)}</a></td>
              <td>${esc(x.kind)}</td>
              <td>${fmtDate(x.date)}</td>
              <td>${badge(DOC_STATUS, x.status)}</td>
              <td class="num"><b>${fmtEur(docTot(x))}</b></td>
              <td class="num"><a href="#/documenti/${x.id}">Apri →</a></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="6">Nessun documento collegato</td></tr>`}
        </tbody>
      </table>
    </div>`;

  $("#p-status").onchange = async e => {
    try { await api(`/projects/${id}/status?status_value=${e.target.value}`, { method: "POST" }); toast("Stato aggiornato", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  };
  $("#p-edit").onclick = () => projectModal(project);
  $("#p-del").onclick = () => confirmDialog(`Eliminare la commessa ${project.number}?`, async () => {
    try { await api("/projects/" + id, { method: "DELETE" }); toast("Commessa eliminata", "success"); location.hash = "#/commesse"; }
    catch (err) { toast(err.message, "error"); }
  });
  ["Proforma", "Fattura", "DDT"].forEach(kind => $("#p-mkdoc-" + kind).onclick = async () => {
    try {
      const doc = await api(`/projects/${id}/create-document?kind=${kind}`, { method: "POST" });
      toast(`${kind} ${doc.number} creato dai lavori della commessa`, "success");
      location.hash = "#/documenti/" + doc.id;
    } catch (err) { toast(err.message, "error"); }
  });
  $("#add-job").onclick = () => jobModal(id);
  $("#add-projmov").onclick = () => movementModal(null, project.id, "scarico");
  $("#add-projmov-generic").onclick = () => movementModal(null, project.id);
  $$("[data-pmedit]").forEach(b => b.onclick = () => movementModal(projMovs.find(x => x.id == b.dataset.pmedit)));
  $$("[data-pmdel]").forEach(b => b.onclick = () => confirmDialog("Eliminare questo movimento? La giacenza verrà ricalcolata.", async () => {
    try { await api("/movements/" + b.dataset.pmdel, { method: "DELETE" }); toast("Movimento eliminato, giacenze ricalcolate", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));
  // timesheet
  if ($("#add-time")) $("#add-time").onclick = () => timeEntryModal(id, null, jobs);
  $$("[data-tdel]").forEach(b => b.onclick = () => confirmDialog("Eliminare questa registrazione di ore?", async () => {
    try { await api("/timesheets/" + b.dataset.tdel, { method: "DELETE" }); toast("Ore eliminate", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));
  $$("[data-tedit]").forEach(b => b.onclick = () => {
    const entry = timesheets.entries.find(x => x.id == b.dataset.tedit);
    timeEntryModal(id, entry, jobs);
  });
  $$("[data-jedit]").forEach(b => b.onclick = () => jobModal(id, jobs.find(x => x.id == b.dataset.jedit)));
  $$("[data-jdel]").forEach(b => b.onclick = () => confirmDialog("Eliminare questo lavoro?", async () => {
    try { await api("/jobs/" + b.dataset.jdel, { method: "DELETE" }); toast("Lavoro eliminato", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));

  paintAttachments(id, $("#att-body"));
  $("#att-upload").onclick = async () => {
    const input = $("#att-file");
    if (!input.files.length) { toast("Scegli un file", "error"); return; }
    const fd = new FormData();
    fd.append("file", input.files[0]);
    try {
      await api(`/projects/${id}/attachments`, { method: "POST", body: fd });
      toast("Allegato caricato", "success");
      render();
    } catch (err) { toast(err.message, "error"); }
  };
});

function attachmentsListHtml(list) {
  if (!list || !list.length) return `<tr class="empty-row"><td>Nessun allegato</td></tr>`;
  return list.map(a => `
    <tr>
      <td>${icon("file", 14)} <b>${esc(a.filename)}</b></td>
      <td>${fmtSize(a.file_size)}</td>
      <td>${fmtDateTime(a.created_at)}</td>
      <td class="num"><div class="actions">
        <button class="btn btn-sm" data-adl="${a.id}">${icon("download", 13)} Scarica</button>
        <button class="btn btn-sm btn-danger" data-adel="${a.id}">${icon("trash", 13)}</button>
      </div></td>
    </tr>`).join("");
}

async function paintAttachments(projectId, body) {
  try {
    const res = await fetch(`/projects/${projectId}/attachments`, { headers: { "Authorization": "Bearer " + TOKEN } });
    if (!res.ok) throw new Error();
    const list = await res.json();
    body.innerHTML = attachmentsListHtml(list);
    $$("[data-adl]", body).forEach(b => b.onclick = () => {
      const att = list.find(x => x.id == b.dataset.adl);
      downloadFile(`/attachments/${att.id}/download`, att.filename);
    });
    $$("[data-adel]", body).forEach(b => b.onclick = () => confirmDialog("Rimuovere questo allegato?", async () => {
      try { await api("/attachments/" + b.dataset.adel, { method: "DELETE" }); toast("Allegato rimosso", "success"); render(); }
      catch (err) { toast(err.message, "error"); }
    }));
  } catch { body.innerHTML = `<tr class="empty-row"><td>Allegati non disponibili</td></tr>`; }
}

async function timeEntryModal(projectId, entry = null, jobs = []) {
  const [workers] = await Promise.all([api("/workers?active=1"), loadClients()]);
  const e = entry || {};
  const lastWorkerId = localStorage.getItem("cn_last_worker");
  modalForm({
    title: entry ? "Modifica ore" : "Registra ore",
    body: `
      <div class="form-grid">
        ${workers.length
          ? field("worker_id", "Lavoratore", { type: "select", required: true, id: "te-worker", options: `<option value="">— scegli —</option>` + workers.map(w => `<option value="${w.id}" ${e.worker_id === w.id || (!entry && String(lastWorkerId) === String(w.id)) ? "selected" : ""}>${esc(w.name)}${w.role ? " (" + esc(w.role) + ")" : ""} — ${fmtEur(w.hourly_cost)}/h</option>`).join("") })
          : field("worker", "Nome operatore (occasionale)", { value: e.worker, full: true })}
        ${field("date", "Data", { type: "date", required: true, value: e.date || todayISO() })}
        ${field("job_id", "Lavoro (opzionale)", { type: "select", options: `<option value="">— generico —</option>` + jobs.map(j => `<option value="${j.id}" ${e.job_id === j.id ? "selected" : ""}>${esc(j.description.slice(0, 45))}</option>`).join("") })}
        <label class="field full">Ore
          <div style="display:flex;gap:6px;align-items:center;margin-top:4px">
            <input name="hours" type="number" step="0.25" min="0.25" max="24" required value="${e.hours ?? ""}" style="flex:1" id="te-hours">
            <button type="button" class="btn btn-sm" data-h="1">1h</button>
            <button type="button" class="btn btn-sm" data-h="2">2h</button>
            <button type="button" class="btn btn-sm" data-h="4">4h</button>
            <button type="button" class="btn btn-sm" data-h="8">8h</button>
          </div></label>
        ${field("notes", "Nota", { value: e.notes, full: true })}
      </div>
      ${workers.length
        ? `<p style="color:var(--muted);font-size:12.5px">Il costo è calcolato con il costo/h del lavoratore e storicizzato su questa riga.</p>`
        : `<p style="color:var(--muted);font-size:12.5px">Suggerimento: crea la squadra in <a href="#/lavoratori">Lavoratori</a> per avere il costo orario automatico.</p>`}`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      payload.hours = num(payload.hours);
      payload.date = payload.date || null;
      payload.job_id = payload.job_id ? parseInt(payload.job_id) : null;
      if (workers.length) {
        payload.worker_id = parseInt(payload.worker_id);
        payload.worker = "";
        localStorage.setItem("cn_last_worker", payload.worker_id);
      } else {
        payload.worker_id = null;
        payload.worker = (payload.worker || "").trim();
      }
      if (entry) await api("/timesheets/" + entry.id, { method: "PUT", json: payload });
      else await api(`/projects/${projectId}/timesheets`, { method: "POST", json: payload });
      closeModal(); toast(entry ? "Ore aggiornate" : "Ore registrate", "success"); render();
    },
  });
  // pulsanti ore veloci
  $$("#modal-box [data-h]").forEach(b => b.onclick = () => { $("#te-hours").value = b.dataset.h; });
}

function jobModal(projectId, job = null) {  const j = job || {};
  const CATS = lookupValues("categoria_lavoro").length
    ? lookupValues("categoria_lavoro")
    : ["Manodopera", "Ricambi", "Materiali", "Noleggio", "Subappalto", "Altro"];
  modalForm({
    title: job ? "Modifica lavoro" : "Nuovo lavoro",
    body: `
      <div class="form-grid">
        ${field("description", "Descrizione", { required: true, value: j.description, full: true })}
        ${field("category", "Categoria", { type: "select", id: "jb-cat", options: CATS.map(c => `<option ${j.category === c ? "selected" : ""}>${esc(c)}</option>`).join("") })}
        ${field("status", "Stato", { type: "select", options: Object.keys(JOB_STATUS).map(s => `<option ${j.status === s ? "selected" : ""}>${s}</option>`).join("") })}
        ${field("priority", "Priorità", { type: "select", options: ["bassa", "normale", "alta", "urgente"].map(p => `<option ${j.priority === p || (!job && p === "normale") ? "selected" : ""}>${p}</option>`).join("") })}
        ${field("qty", "Quantità", { type: "number", step: "any", min: 0, value: j.qty ?? 1 })}
        ${field("unit", "Unità", { value: j.unit || ((j.category ?? "Manodopera") === "Manodopera" ? "ore" : "pz"), id: "jb-unit" })}
        ${field("unit_cost", "Costo unitario (€)", { type: "number", step: "any", min: 0, value: j.unit_cost ?? 0 })}
        ${field("unit_price", "Prezzo unitario (€)", { type: "number", step: "any", min: 0, value: j.unit_price ?? 0 })}
        ${field("assigned_to", "Assegnato a", { value: j.assigned_to, full: true })}
      </div>
      <p style="color:var(--muted);font-size:12.5px">Per la manodopera l'unità è in ore: prezzo e costo si intendono <b>all'ora</b> e in proforma/fattura compariranno come €/ora.</p>`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      for (const k of ["qty", "unit_cost", "unit_price"]) payload[k] = num(payload[k]);
      if (job) await api("/jobs/" + job.id, { method: "PUT", json: payload });
      else await api(`/projects/${projectId}/jobs`, { method: "POST", json: payload });
      closeModal(); toast("Lavoro salvato", "success"); render();
    },
  });
  // manodopera = sempre ore (con unità comunque modificabile)
  const catSel = $("#jb-cat"), unitInp = $("#jb-unit");
  catSel.onchange = () => {
    if (catSel.value === "Manodopera") unitInp.value = "ore";
    else if (unitInp.value === "ore") unitInp.value = "pz";
  };
}

/* ============ Magazzino ============ */

let warehouseTab = "articoli";
let warehouseFilterId = null;

route(/^\/magazzino$/, async () => {
  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("box")} Magazzino</h1><div class="sub">Articoli, giacenze e movimenti</div></div>
      <div class="head-actions" id="wh-actions"></div>
    </div>
    <div class="tabs" id="wh-tabs">
      <button data-tab="articoli" class="${warehouseTab === "articoli" ? "active" : ""}">Articoli</button>
      <button data-tab="giacenze" class="${warehouseTab === "giacenze" ? "active" : ""}">Giacenze</button>
      <button data-tab="movimenti" class="${warehouseTab === "movimenti" ? "active" : ""}">Movimenti</button>
      <button data-tab="magazzini" class="${warehouseTab === "magazzini" ? "active" : ""}">Magazzini</button>
    </div>
    <div id="wh-content"></div>`;

  $$("#wh-tabs button").forEach(b => b.onclick = () => { warehouseTab = b.dataset.tab; render(); });
  await loadWarehouses();

  const actions = $("#wh-actions");
  if (warehouseTab === "articoli") { actions.innerHTML = `<button class="btn btn-primary" id="add-item">${icon("plus", 14)} Nuovo articolo</button>`; $("#add-item").onclick = () => itemModal(); }
  if (warehouseTab === "movimenti") { actions.innerHTML = `<button class="btn btn-primary" id="add-mov">${icon("plus", 14)} Nuovo movimento</button>`; $("#add-mov").onclick = async () => { await loadItems(); movementModal(); }; }
  if (warehouseTab === "magazzini") { actions.innerHTML = `<button class="btn btn-primary" id="add-wh">${icon("plus", 14)} Nuovo magazzino</button>`; $("#add-wh").onclick = () => warehouseModal(); }

  if (warehouseTab === "articoli") await tabArticoli();
  if (warehouseTab === "giacenze") await tabGiacenze();
  if (warehouseTab === "movimenti") await tabMovimenti();
  if (warehouseTab === "magazzini") await tabMagazzini();
});

async function tabArticoli() {
  const [items, alerts] = await Promise.all([loadItems(), api("/stock/alerts")]);
  const alertMap = {};
  alerts.forEach(a => alertMap[a.item_id] = a);
  $("#wh-content").innerHTML = `
    <div class="card">
      <table class="tbl">
        <thead><tr><th>SKU</th><th>Articolo</th><th>Categoria</th><th>Unità</th><th class="num">Costo</th><th class="num">Prezzo</th><th class="num">Scorta tot.</th><th class="num">Min.</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${items.length ? items.map(i => {
            const a = alertMap[i.id];
            return `
            <tr>
              <td><span class="badge badge-gray">${esc(i.sku || "—")}</span></td>
              <td class="primary">${esc(i.name)} ${a?.alert ? `<span class="badge badge-red">sotto scorta</span>` : ""}</td>
              <td>${esc(i.category || "—")}</td>
              <td>${esc(i.unit)}</td>
              <td class="num">${fmtEur(i.cost)}</td>
              <td class="num">${fmtEur(i.price)}</td>
              <td class="num">${fmtNum(a?.total_qty ?? 0)}</td>
              <td class="num">${i.min_stock ? fmtNum(i.min_stock) : "—"}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-edit="${i.id}">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-del="${i.id}">${icon("trash", 13)}</button>
              </div></td>
            </tr>`;
          }).join("") : `<tr class="empty-row"><td colspan="9">Nessun articolo</td></tr>`}
        </tbody>
      </table>
      <p style="color:var(--muted);font-size:12.5px;margin-top:10px">Imposta la scorta minima nella scheda articolo: quando la giacenza totale scende sotto, l'articolo viene segnalato qui e in dashboard.</p>
    </div>`;
  $$("[data-edit]").forEach(b => b.onclick = () => itemModal(items.find(x => x.id == b.dataset.edit)));
  $$("[data-del]").forEach(b => b.onclick = () => {
    const it = items.find(x => x.id == b.dataset.del);
    confirmDialog(`Eliminare l'articolo “${it.name}”?`, async () => {
      try { await api("/items/" + it.id, { method: "DELETE" }); toast("Articolo eliminato", "success"); render(); }
      catch (err) { toast(err.message, "error"); }
    });
  });
}

async function tabGiacenze() {
  const stock = await api("/stock" + (warehouseFilterId ? `?warehouse_id=${warehouseFilterId}` : ""));
  $("#wh-content").innerHTML = `
    <div class="card">
      <div class="toolbar">
        <select id="stock-wh">
          <option value="">Tutti i magazzini</option>
          ${cache.warehouses.map(w => `<option value="${w.id}" ${warehouseFilterId === w.id ? "selected" : ""}>${esc(w.name)}</option>`).join("")}
        </select>
      </div>
      <table class="tbl">
        <thead><tr><th>Magazzino</th><th>Articolo</th><th class="num">Quantità</th></tr></thead>
        <tbody>
          ${stock.length ? stock.map(s => `
            <tr>
              <td>${esc(s.warehouse)}</td>
              <td class="primary">${esc(s.item)}</td>
              <td class="num">${fmtNum(s.qty)}</td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="3">Nessuna giacenza: registra un movimento di carico</td></tr>`}
        </tbody>
      </table>
    </div>`;
  $("#stock-wh").onchange = e => { warehouseFilterId = e.target.value ? parseInt(e.target.value) : null; render(); };
}

async function tabMovimenti() {
  const movements = await api("/movements");
  $("#wh-content").innerHTML = `
    <div class="card">
      <table class="tbl">
        <thead><tr><th>Data</th><th>Tipo</th><th>Articolo</th><th>Magazzino</th><th>Commessa</th><th class="num">Qtà</th><th class="num">Costo unit.</th><th>Note</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${movements.length ? movements.map(m => `
            <tr>
              <td>${fmtDate(m.date)}</td>
              <td>${badge(MOV_TYPE, m.type)}</td>
              <td class="primary">${esc(m.item)}</td>
              <td>${esc(m.warehouse)}</td>
              <td>${m.project_id ? `<a href="#/commesse/${m.project_id}">${esc(m.project)}</a>` : "—"}</td>
              <td class="num">${fmtNum(m.qty)}</td>
              <td class="num">${fmtEur(m.unit_cost)}</td>
              <td>${esc(m.note || "")}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-medit="${m.id}" title="Modifica">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-mdel="${m.id}" title="Elimina">${icon("trash", 13)}</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="9">Nessun movimento</td></tr>`}
        </tbody>
      </table>
      <p style="color:var(--muted);font-size:12.5px;margin-top:10px">Modificando o eliminando un movimento le giacenze vengono ricalcolate automaticamente.</p>
    </div>`;
  $$("[data-medit]").forEach(b => b.onclick = () => movementModal(movements.find(x => x.id == b.dataset.medit)));
  $$("[data-mdel]").forEach(b => b.onclick = () => confirmDialog("Eliminare questo movimento? La giacenza verrà ricalcolata.", async () => {
    try { await api("/movements/" + b.dataset.mdel, { method: "DELETE" }); toast("Movimento eliminato, giacenze ricalcolate", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));
}

async function tabMagazzini() {
  const warehouses = cache.warehouses;
  $("#wh-content").innerHTML = `
    <div class="card">
      <table class="tbl">
        <thead><tr><th>Codice</th><th>Nome</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${warehouses.length ? warehouses.map(w => `
            <tr>
              <td><span class="badge badge-gray">${esc(w.code)}</span></td>
              <td class="primary">${esc(w.name)}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-wedit="${w.id}" title="Modifica">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-wdel="${w.id}" title="Elimina">${icon("trash", 13)}</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="3">Nessun magazzino</td></tr>`}
        </tbody>
      </table>
      <p style="color:var(--muted);font-size:12.5px;margin-top:10px">Un magazzino si elimina solo se non ha giacenze né movimenti.</p>
    </div>`;
  $$("[data-wedit]").forEach(b => b.onclick = () => warehouseModal(warehouses.find(x => x.id == b.dataset.wedit)));
  $$("[data-wdel]").forEach(b => b.onclick = () => {
    const w = warehouses.find(x => x.id == b.dataset.wdel);
    confirmDialog(`Eliminare il magazzino “${w.name}”?`, async () => {
      try { await api("/warehouses/" + w.id, { method: "DELETE" }); toast("Magazzino eliminato", "success"); render(); }
      catch (err) { toast(err.message, "error"); }
    });
  });
}

function itemModal(item = null) {
  const i = item || {};
  modalForm({
    title: item ? "Modifica articolo" : "Nuovo articolo",
    body: `
      <div class="form-grid">
        ${field("sku", "SKU", { value: i.sku })}
        ${field("name", "Nome", { required: true, value: i.name })}
        ${field("category", "Categoria", { value: i.category })}
        ${field("unit", "Unità", { value: i.unit || "pz" })}
        ${field("cost", "Costo (€)", { type: "number", step: "any", min: 0, value: i.cost ?? 0 })}
        ${field("price", "Prezzo di vendita (€)", { type: "number", step: "any", min: 0, value: i.price ?? 0 })}
        ${field("min_stock", "Scorta minima (alert sotto questa quantità)", { type: "number", step: "any", min: 0, value: i.min_stock ?? 0, full: true })}
      </div>`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      payload.cost = num(payload.cost); payload.price = num(payload.price);
      payload.min_stock = num(payload.min_stock);
      if (item) await api("/items/" + item.id, { method: "PUT", json: payload });
      else await api("/items", { method: "POST", json: payload });
      closeModal(); toast("Articolo salvato", "success"); render();
    },
  });
}

async function movementModal(movement = null, presetProjectId = null, presetType = null) {
  const m = movement || {};
  if (!cache.items.length) await loadItems();
  if (!cache.warehouses.length) await loadWarehouses();
  const projects = await api("/projects");
  modalForm({
    title: movement ? "Modifica movimento" : "Nuovo movimento",
    body: `
      <div class="form-grid">
        ${field("warehouse_id", "Magazzino", { type: "select", required: true, options: `<option value="">— scegli —</option>` + cache.warehouses.map(w => `<option value="${w.id}" ${m.warehouse_id === w.id ? "selected" : ""}>${esc(w.name)}</option>`).join("") })}
        ${field("item_id", "Articolo", { type: "select", required: true, id: "mv-item", options: `<option value="">— scegli —</option>` + cache.items.map(i => `<option value="${i.id}" ${m.item_id === i.id ? "selected" : ""}>${esc(i.name)}</option>`).join("") })}
        ${field("type", "Tipo", { type: "select", options: `<option value="carico" ${m.type === "carico" ? "selected" : ""}>Carico</option><option value="scarico" ${m.type === "scarico" ? "selected" : ""}>Scarico</option><option value="reso" ${m.type === "reso" ? "selected" : ""}>Reso</option>` })}
        ${field("qty", "Quantità", { type: "number", step: "any", min: "0.01", required: true, value: m.qty ?? "" })}
        ${field("unit_cost", "Costo unitario (€) — proposto dalla scheda articolo", { type: "number", step: "any", min: 0, value: m.unit_cost ?? 0, id: "mv-cost" })}
        ${field("project_id", "Commessa di riferimento", { type: "select", options: `<option value="">— nessuna —</option>` + projects.map(p => `<option value="${p.id}" ${m.project_id === p.id || (!movement && presetProjectId === p.id) ? "selected" : ""}>${esc(p.number)} — ${esc(p.title)}</option>`).join("") })}
        ${field("note", "Nota", { full: true, value: m.note || "" })}
      </div>`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      payload.warehouse_id = parseInt(payload.warehouse_id);
      payload.item_id = parseInt(payload.item_id);
      payload.qty = num(payload.qty);
      payload.unit_cost = payload.unit_cost === "" ? null : num(payload.unit_cost);
      payload.project_id = payload.project_id ? parseInt(payload.project_id) : null;
      if (movement) await api("/movements/" + movement.id, { method: "PUT", json: payload });
      else await api("/movements", { method: "POST", json: payload });
      closeModal(); toast(movement ? "Movimento aggiornato" : "Movimento registrato", "success"); render();
    },
  });
  if (!movement && presetType) {
    const typeSel = $("#mf-form [name='type']");
    if (typeSel) typeSel.value = presetType;
  }
  // scelto l'articolo, propone il costo unitario dalla sua scheda (campo comunque modificabile)
  $("#mv-item").onchange = e => {
    const item = cache.items.find(i => i.id === parseInt(e.target.value));
    if (item) $("#mv-cost").value = item.cost ?? 0;
  };
}

function warehouseModal(warehouse = null) {
  const w = warehouse || {};
  modalForm({
    title: warehouse ? "Modifica magazzino" : "Nuovo magazzino",
    body: `${field("code", "Codice", { required: true, value: w.code, placeholder: "es. SEDE2" })}${field("name", "Nome", { required: true, value: w.name, placeholder: "es. Rimessa al molo" })}`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      if (warehouse) await api("/warehouses/" + warehouse.id, { method: "PUT", json: payload });
      else await api("/warehouses", { method: "POST", json: payload });
      closeModal(); toast(warehouse ? "Magazzino aggiornato" : "Magazzino creato", "success"); render();
    },
  });
}

/* ============ Documenti ============ */

let docFilter = { kind: "", status: "", client_id: "", year: "", q: "" };

route(/^\/documenti$/, async () => {
  const [docs, clients] = await Promise.all([api("/documents" + docQueryString()), loadClients()]);
  const years = [...new Set(docs.map(d => (d.number.match(/-(\d{4})-/) || [])[1]).filter(Boolean))].sort().reverse();
  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("file")} Documenti</h1><div class="sub">DDT, Proforme e Fatture</div></div>
      <div class="head-actions">
        <button class="btn" id="export-docs">${icon("download", 14)} CSV</button>
        <button class="btn btn-primary" id="add-doc">${icon("plus", 14)} Nuovo documento</button>
      </div>
    </div>
    <div class="card">
      <div class="toolbar">
        <select id="f-kind"><option value="">Tutti i tipi</option>
          ${["DDT", "Proforma", "Fattura"].map(k => `<option ${docFilter.kind === k ? "selected" : ""}>${k}</option>`).join("")}</select>
        <select id="f-status"><option value="">Tutti gli stati</option>
          ${Object.entries(DOC_STATUS).map(([k, [l]]) => `<option value="${k}" ${docFilter.status === k ? "selected" : ""}>${l}</option>`).join("")}</select>
        <select id="f-client"><option value="">Tutti i clienti</option>
          ${clients.map(c => `<option value="${c.id}" ${String(docFilter.client_id) === String(c.id) ? "selected" : ""}>${esc(c.name)}</option>`).join("")}</select>
        <select id="f-year"><option value="">Tutti gli anni</option>
          ${years.map(y => `<option ${docFilter.year === y ? "selected" : ""}>${y}</option>`).join("")}</select>
        <input type="text" id="f-q" placeholder="Numero…" value="${esc(docFilter.q)}">
        ${docFilterActive() ? `<button class="btn btn-sm" id="f-reset">${icon("x", 13)} Azzera filtri</button>` : ""}
      </div>
      <table class="tbl">
        <thead><tr><th>Numero</th><th>Tipo</th><th>Cliente</th><th>Data</th><th>Stato</th><th class="num">Totale</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${docs.length ? docs.map(x => `
            <tr>
              <td><a href="#/documenti/${x.id}"><b>${esc(x.number)}</b></a></td>
              <td>${esc(x.kind)}</td>
              <td>${esc(clientName(x.client_id))}</td>
              <td>${fmtDate(x.date)}</td>
              <td>${badge(DOC_STATUS, x.status)}</td>
              <td class="num"><b>${fmtEur(docTot(x))}</b></td>
              <td class="num"><div class="actions">
                <a class="btn btn-sm" href="#/documenti/${x.id}">${icon("eye", 13)} Apri</a>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="7">Nessun documento con questi filtri</td></tr>`}
        </tbody>
      </table>
    </div>`;

  const onFilter = () => {
    docFilter = {
      kind: $("#f-kind").value, status: $("#f-status").value,
      client_id: $("#f-client").value, year: $("#f-year").value, q: $("#f-q").value.trim(),
    };
    render();
  };
  ["#f-kind", "#f-status", "#f-client", "#f-year"].forEach(s => $(s).onchange = onFilter);
  let dt = null;
  $("#f-q").oninput = e => { clearTimeout(dt); dt = setTimeout(onFilter, 350); };
  if ($("#f-reset")) $("#f-reset").onclick = () => { docFilter = { kind: "", status: "", client_id: "", year: "", q: "" }; render(); };
  $("#add-doc").onclick = () => documentModal();
  $("#export-docs").onclick = () => downloadFile("/documents/export", "documenti.csv");
});

function docFilterActive() { return Object.values(docFilter).some(v => v !== ""); }
function docQueryString() {
  const qs = new URLSearchParams();
  if (docFilter.kind) qs.set("kind", docFilter.kind);
  if (docFilter.status) qs.set("status", docFilter.status);
  if (docFilter.client_id) qs.set("client_id", docFilter.client_id);
  if (docFilter.year) qs.set("year", docFilter.year);
  if (docFilter.q) qs.set("q", docFilter.q);
  const s = qs.toString();
  return s ? "?" + s : "";
}

function documentModal(presetProjectId = null, presetClientId = null) {
  modalForm({
    title: "Nuovo documento",
    wide: true,
    body: `
      <div class="form-grid">
        ${field("kind", "Tipo", { type: "select", id: "nd-kind", options: ["Proforma", "Fattura", "DDT"].map(k => `<option value="${k}">${k}</option>`).join("") })}
        ${field("client_id", "Cliente", { type: "select", required: true, id: "nd-client", options: `<option value="">— scegli —</option>` +
          cache.clients.filter(c => c.active !== false).map(c => `<option value="${c.id}" ${presetClientId === c.id ? "selected" : ""}>${esc(c.name)}${c.discount ? " (sconto " + c.discount + "%)" : ""}</option>`).join("") })}
        ${field("project_id", "Commessa", { type: "select", id: "nd-project", options: `<option value="">— nessuna —</option>` })}
        ${field("date", "Data", { type: "date", value: todayISO() })}
        ${field("due_date", "Scadenza", { type: "date" })}
        ${field("discount_pct", "Sconto %", { type: "number", step: "any", min: 0, id: "nd-discount-pct", placeholder: "da scheda cliente" })}
        ${field("discount", "Sconto aggiuntivo (€)", { type: "number", step: "any", min: 0, value: 0 })}
        ${field("tax_rate", "IVA %", { type: "number", step: "any", min: 0, id: "nd-tax", value: cache.settings?.default_tax_rate ?? 22 })}
        ${field("vat_nature", "Natura IVA (se 0%)", { type: "select", id: "nd-nature", options: vatNatureOptions("") })}
      </div>
      <div class="form-section">Note</div>
      ${field("notes", "Note a piè di documento", { type: "textarea", full: true })}
      <div id="nd-ddt" class="hidden">
        <div class="form-section">Trasporto (DDT)</div>
        <div class="form-grid">
          ${field("ddt_reason", "Causale trasporto")}
          ${field("ddt_carrier", "Vettore")}
          ${field("ddt_destination", "Destinazione")}
          ${field("ddt_parcels", "Colli", { type: "number", min: 0 })}
          ${field("ddt_weight", "Peso (kg)", { type: "number", step: "any", min: 0 })}
        </div>
      </div>
      <p style="color:var(--muted);font-size:13px">Le righe si aggiungono dopo la creazione, nella pagina del documento.</p>`,
    onSubmit: async fd => {
      const payload = {
        kind: fd.get("kind"),
        client_id: parseInt(fd.get("client_id")),
        project_id: fd.get("project_id") ? parseInt(fd.get("project_id")) : null,
        date: fd.get("date") || null,
        due_date: fd.get("due_date") || null,
        discount: num(fd.get("discount")),
        discount_pct: fd.get("discount_pct") === "" ? null : num(fd.get("discount_pct")),
        tax_rate: fd.get("tax_rate") === "" ? null : num(fd.get("tax_rate")),
        vat_nature: fd.get("vat_nature") || "",
        notes: fd.get("notes") || "",
      };
      if (payload.kind === "DDT") {
        payload.ddt_reason = fd.get("ddt_reason") || "";
        payload.ddt_carrier = fd.get("ddt_carrier") || "";
        payload.ddt_destination = fd.get("ddt_destination") || "";
        payload.ddt_parcels = fd.get("ddt_parcels") ? parseInt(fd.get("ddt_parcels")) : null;
        payload.ddt_weight = fd.get("ddt_weight") ? num(fd.get("ddt_weight")) : null;
      }
      const doc = await api("/documents", { method: "POST", json: payload });
      closeModal(); toast("Documento creato", "success");
      location.hash = "#/documenti/" + doc.id;
    },
  });

  api("/projects").then(projects => {
    $("#nd-project").insertAdjacentHTML("beforeend",
      projects.map(p => `<option value="${p.id}" ${presetProjectId === p.id ? "selected" : ""}>${esc(p.number)} — ${esc(p.title)}</option>`).join(""));
  });
  const kindSel = $("#nd-kind");
  kindSel.onchange = () => $("#nd-ddt").classList.toggle("hidden", kindSel.value !== "DDT");
  $("#nd-client").onchange = e => {
    const c = cache.clients.find(x => x.id === parseInt(e.target.value));
    $("#nd-discount-pct").value = c && c.discount ? c.discount : "";
    $("#nd-discount-pct").placeholder = c && c.discount ? "" : "nessuno";
  };
  const syncNature = () => $("#nd-nature").closest("label").classList.toggle("hidden", num($("#nd-tax").value) !== 0);
  $("#nd-tax").oninput = syncNature;
  syncNature();
  if (presetClientId) $("#nd-client").onchange({ target: $("#nd-client") });
}

/* Formattazione righe documento: la manodopera è in ore (prezzo = €/ora) */
const lineQty = l => `${fmtNum(l.qty)}${l.unit && l.unit !== "pz" ? " " + esc(l.unit) : ""}`;
const linePrice = l => `${fmtEur(l.price)}${l.unit === "ore" ? "/ora" : l.unit && l.unit !== "pz" ? "/" + esc(l.unit) : ""}`;

/* ---- Dettaglio documento ---- */

route(/^\/documenti\/(\d+)$/, async (id) => {
  const doc = await api("/documents/" + id);
  await Promise.all([loadClients(), loadSettings()]);
  const client = cache.clients.find(c => c.id === doc.client_id);
  const s = cache.settings;

  $("#view").innerHTML = `
    <a class="back-link" href="#/documenti">${icon("arrowleft", 14)} Tutti i documenti</a>
    <div class="page-head">
      <div>
        <h1>${icon("file")} ${esc(doc.kind)} ${esc(doc.number)}</h1>
        <div class="doc-meta">
          ${badge(DOC_STATUS, doc.status)}
          <span>Data: <b>${fmtDate(doc.date)}</b></span>
          ${doc.due_date ? `<span>Scadenza: ${fmtDate(doc.due_date)}</span>` : ""}
          <span>Cliente: <a href="#/clienti/${doc.client_id}"><b>${esc(client?.name || "—")}</b></a></span>
          ${doc.project_id ? `<span><a href="#/commesse/${doc.project_id}">Vai alla commessa →</a></span>` : ""}
          ${doc.created_by ? `<span>Creato da ${esc(doc.created_by)}</span>` : ""}
        </div>
        ${doc.kind === "DDT" ? `
          <div class="doc-meta">
            ${doc.ddt_reason ? `<span>Causale: ${esc(doc.ddt_reason)}</span>` : ""}
            ${doc.ddt_carrier ? `<span>Vettore: ${esc(doc.ddt_carrier)}</span>` : ""}
            ${doc.ddt_destination ? `<span>Destinazione: ${esc(doc.ddt_destination)}</span>` : ""}
            ${doc.ddt_parcels != null ? `<span>Colli: ${esc(doc.ddt_parcels)}</span>` : ""}
            ${doc.ddt_weight != null ? `<span>Peso: ${esc(doc.ddt_weight)} kg</span>` : ""}
          </div>` : ""}
        ${doc.notes ? `<div class="doc-meta">${esc(doc.notes)}</div>` : ""}
      </div>
      <div class="head-actions">
        ${doc.status !== "annullata" && doc.status !== "archiviata" ? `<button class="btn" id="d-edit">${icon("edit", 14)} Modifica</button>` : ""}
        ${doc.status === "bozza" ? `<button class="btn btn-primary" id="d-issue">${icon("check", 14)} Emetti</button>` : ""}
        ${doc.status === "emessa" && !(doc.payments || []).length ? `<button class="btn" id="d-cancel">Annulla documento</button>` : ""}
        ${["DDT", "Proforma"].includes(doc.kind) ? `<button class="btn" id="d-convert">${icon("file", 14)} Converti in fattura</button>` : ""}
        ${doc.kind === "Fattura" ? `<button class="btn" id="d-xml">${icon("download", 14)} XML</button>` : ""}
        ${["emessa", "pagata"].includes(doc.status) ? `<button class="btn" id="d-archive">${icon("archive", 14)} Archivia</button>` : ""}
        ${doc.status === "archiviata" ? `<button class="btn" id="d-unarchive">Riattiva</button>` : ""}
        ${doc.status === "annullata" ? `<button class="btn" id="d-unarchive">Ripristina come bozza</button>` : ""}
        <button class="btn" id="d-print">${icon("printer", 14)} Stampa</button>
        ${doc.status === "bozza" ? `<button class="btn btn-danger" id="d-del">${icon("trash", 14)}</button>` : ""}
      </div>
    </div>

    <div class="card">
      <h2>${icon("clipboard", 15)} Righe <span class="count">${doc.lines.length}</span></h2>
      <table class="tbl">
        <thead><tr><th>Descrizione</th><th class="num">Qtà</th><th class="num">Prezzo unit.</th><th class="num">Totale</th><th class="num"></th></tr></thead>
        <tbody>
          ${doc.lines.length ? doc.lines.map(l => `
            <tr>
              <td>${esc(l.description)}</td>
              <td class="num">${lineQty(l)}</td>
              <td class="num">${linePrice(l)}</td>
              <td class="num"><b>${fmtEur(lineTotal(l))}</b></td>
              <td class="num">${["bozza", "emessa"].includes(doc.status) ? `
                <div class="actions">
                  <button class="btn btn-sm" data-ledit="${l.id}">${icon("edit", 13)}</button>
                  <button class="btn btn-sm btn-danger" data-ldel="${l.id}">${icon("trash", 13)}</button>
                </div>` : ""}</td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="5">Nessuna riga</td></tr>`}
        </tbody>
      </table>
      ${["bozza", "emessa"].includes(doc.status) ? `
      <form class="inline-form" id="line-form" style="margin-top:14px">
        <label class="field" style="flex:3;min-width:220px">Descrizione<input name="description" required placeholder="Descrizione riga"></label>
        <label class="field">Quantità<input name="qty" type="number" step="any" min="0" value="1"></label>
        <label class="field">Unità<input name="unit" placeholder="pz" style="width:80px" title="es. ore per la manodopera (prezzo = €/ora)"></label>
        <label class="field">Prezzo (€)<input name="price" type="number" step="any" min="0" value="0"></label>
        <button class="btn btn-primary">${icon("plus", 13)} Aggiungi</button>
      </form>` : ""}
    </div>

    <div class="grid-2">
      <div class="card">
        <h2>${icon("wallet", 15)} Pagamenti</h2>
        ${doc.kind === "DDT" ? `<p style="color:var(--muted)">Un DDT non ha pagamenti: convertilo in fattura per incassare.</p>` : `
        <table class="tbl"><tbody>
          ${doc.payments?.length ? doc.payments.map(p => `
            <tr><td>${fmtDate(p.date)}</td><td>${esc(p.method)}</td><td class="num"><b>${fmtEur(p.amount)}</b></td>
            <td class="num">${["admin", "manager"].includes(CURRENT_USER.role) && doc.status !== "archiviata" ? `<button class="btn btn-sm btn-danger" data-pdel="${p.id}" title="Elimina pagamento">${icon("trash", 12)}</button>` : ""}</td></tr>`).join("")
            : `<tr class="empty-row"><td colspan="4">Nessun pagamento registrato</td></tr>`}
        </tbody></table>
        ${doc.status === "bozza" ? `<p style="margin-top:12px;color:var(--muted)">Emetti il documento per poter registrare gli incassi.</p>` : ""}
        ${!["bozza", "annullata", "archiviata"].includes(doc.status) && doc.residual > 0 ? `
        <form class="inline-form" id="pay-form" style="margin-top:14px">
          <label class="field">Importo (€)<input name="amount" type="number" step="0.01" min="0.01" max="${doc.residual}" required value="${doc.residual.toFixed(2)}"></label>
          <label class="field">Data<input name="date" type="date" value="${todayISO()}"></label>
          <label class="field">Metodo
            <select name="method">
              <option value="bonifico">Bonifico</option>
              <option value="contanti">Contanti</option>
              <option value="carta">Carta</option>
              <option value="assegno">Assegno</option>
              ${client?.payment_terms ? `<option value="${esc(client.payment_terms)}">${esc(client.payment_terms)}</option>` : ""}
            </select></label>
          <button class="btn btn-primary">Registra</button>
        </form>` : ""}
        <p style="margin-top:10px;color:var(--muted);font-size:13px">Totale <b>${fmtEur(doc.total)}</b> · incassato <b>${fmtEur(doc.paid)}</b> · residuo <b>${fmtEur(doc.residual)}</b>${doc.status !== "pagata" ? " — al saldo lo stato passa a “Pagata”" : ""}.</p>`}
      </div>
      <div class="card totals-box">
        <h2>${icon("euro", 15)} Totali</h2>
        <div class="row"><span>Subtotale</span><span>${fmtEur(doc.subtotal)}</span></div>
        ${doc.discount_amount ? `<div class="row"><span>Sconto${doc.discount_pct ? " " + fmtNum(doc.discount_pct) + "%" : ""}</span><span>- ${fmtEur(doc.discount_amount)}</span></div>` : ""}
        <div class="row"><span>Imponibile</span><span>${fmtEur(doc.taxable)}</span></div>
        <div class="row"><span>IVA ${fmtNum(doc.tax_rate)}%${doc.vat_nature ? " (" + esc(doc.vat_nature) + ")" : ""}</span><span>${fmtEur(doc.tax)}</span></div>
        <div class="row grand"><span>Totale</span><span>${fmtEur(doc.total)}</span></div>
      </div>
    </div>`;

  if ($("#line-form")) $("#line-form").onsubmit = async e => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
      await api(`/documents/${id}/lines`, {
        method: "POST",
        json: {
          description: fd.get("description"),
          qty: num(fd.get("qty")),
          price: num(fd.get("price")),
          unit: (fd.get("unit") || "").trim(),
        },
      });
      toast("Riga aggiunta", "success"); render();
    } catch (err) { toast(err.message, "error"); }
  };
  $$("[data-ldel]").forEach(b => b.onclick = () => confirmDialog("Rimuovere questa riga?", async () => {
    try { await api(`/documents/${id}/lines/${b.dataset.ldel}`, { method: "DELETE" }); toast("Riga rimossa", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));
  $$("[data-ledit]").forEach(b => b.onclick = () => {
    const line = doc.lines.find(x => x.id == b.dataset.ledit);
    modalForm({
      title: "Modifica riga",
      body: `
        <div class="form-grid">
          ${field("description", "Descrizione", { required: true, value: line.description, full: true })}
          ${field("qty", "Quantità", { type: "number", step: "any", min: 0, value: line.qty })}
          ${field("unit", "Unità", { value: line.unit || "", placeholder: "pz", full: false })}
          ${field("price", "Prezzo (€)", { type: "number", step: "any", min: 0, value: line.price })}
        </div>
        <p style="color:var(--muted);font-size:12.5px">Con unità “ore” il prezzo si intende <b>€/ora</b> (manodopera) e comparirà come tale anche in stampa.</p>`,
      onSubmit: async fd => {
        const payload = Object.fromEntries(fd.entries());
        payload.qty = num(payload.qty);
        payload.price = num(payload.price);
        payload.unit = (payload.unit || "").trim();
        await api(`/documents/${id}/lines/${line.id}`, { method: "PUT", json: payload });
        closeModal(); toast("Riga aggiornata", "success"); render();
      },
    });
  });
  if ($("#pay-form")) $("#pay-form").onsubmit = async e => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
      await api(`/documents/${id}/payments`, {
        method: "POST",
        json: { amount: num(fd.get("amount")), method: fd.get("method"), date: fd.get("date") || null },
      });
      toast("Pagamento registrato", "success"); render();
    } catch (err) { toast(err.message, "error"); }
  };
  $$("[data-pdel]").forEach(b => b.onclick = () => confirmDialog("Eliminare questo pagamento?", async () => {
    try { await api(`/documents/${id}/payments/${b.dataset.pdel}`, { method: "DELETE" }); toast("Pagamento eliminato", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));
  if ($("#d-cancel")) $("#d-cancel").onclick = () => confirmDialog("Annullare questo documento? Resterà in archivio ma non conterà nei totali.", async () => {
    try { await api(`/documents/${id}/status?status_value=annullata`, { method: "POST" }); toast("Documento annullato", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }, "Annulla documento");
  if ($("#d-issue")) $("#d-issue").onclick = async () => {
    try { await api(`/documents/${id}/status?status_value=emessa`, { method: "POST" }); toast("Documento emesso", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  };
  if ($("#d-convert")) $("#d-convert").onclick = () => confirmDialog("Convertire questo documento in fattura?", async () => {
    try {
      const newDoc = await api(`/documents/${id}/convert`, { method: "POST" });
      toast("Fattura creata", "success");
      location.hash = "#/documenti/" + newDoc.id;
    } catch (err) { toast(err.message, "error"); }
  }, "Converti");
  if ($("#d-xml")) $("#d-xml").onclick = () => downloadFile(`/documents/${id}/xml`, doc.number + ".xml");
  if ($("#d-archive")) $("#d-archive").onclick = () => confirmDialog("Archiviare questo documento? Non apparirà più nei totali né nello scadenzario.", async () => {
    try { await api(`/documents/${id}/status?status_value=archiviata`, { method: "POST" }); toast("Documento archiviato", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }, "Archivia");
  if ($("#d-unarchive")) $("#d-unarchive").onclick = async () => {
    const target = doc.status === "annullata" ? "bozza" : "emessa";
    try { await api(`/documents/${id}/status?status_value=${target}`, { method: "POST" }); toast("Documento riattivato", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  };
  if ($("#d-del")) $("#d-del").onclick = () => confirmDialog("Eliminare definitivamente questo documento? (solo bozze)", async () => {
    try { await api("/documents/" + id, { method: "DELETE" }); toast("Documento eliminato", "success"); location.hash = "#/documenti"; }
    catch (err) { toast(err.message, "error"); }
  });
  $("#d-print").onclick = () => printDocument(doc, client, s);
  if ($("#d-edit")) $("#d-edit").onclick = () => documentEditModal(doc);
});

function documentEditModal(doc) {
  modalForm({
    title: `Modifica ${doc.kind} ${doc.number}`,
    wide: true,
    body: `
      <div class="form-grid">
        ${field("client_id", "Cliente", { type: "select", required: true, options: cache.clients.map(c => `<option value="${c.id}" ${doc.client_id === c.id ? "selected" : ""}>${esc(c.name)}</option>`).join("") })}
        ${field("project_id", "Commessa", { type: "select", id: "ne-project", options: `<option value="">— nessuna —</option>` })}
        ${field("date", "Data", { type: "date", value: doc.date })}
        ${field("due_date", "Scadenza", { type: "date", value: doc.due_date || "" })}
        ${doc.status !== "pagata" ? field("discount_pct", "Sconto %", { type: "number", step: "any", min: 0, value: doc.discount_pct || 0 }) : ""}
        ${doc.status !== "pagata" ? field("discount", "Sconto aggiuntivo (€)", { type: "number", step: "any", min: 0, value: doc.discount }) : ""}
        ${doc.status !== "pagata" ? field("tax_rate", "IVA %", { type: "number", step: "any", min: 0, id: "ne-tax", value: doc.tax_rate }) : ""}
        ${doc.status !== "pagata" ? field("vat_nature", "Natura IVA (se 0%)", { type: "select", id: "ne-nature", options: vatNatureOptions(doc.vat_nature) }) : ""}
      </div>
      <div class="form-section">Note</div>
      ${field("notes", "Note a piè di documento", { type: "textarea", full: true, value: doc.notes })}
      ${doc.kind === "DDT" ? `
      <div class="form-section">Trasporto (DDT)</div>
      <div class="form-grid">
        ${field("ddt_reason", "Causale trasporto", { value: doc.ddt_reason })}
        ${field("ddt_carrier", "Vettore", { value: doc.ddt_carrier })}
        ${field("ddt_destination", "Destinazione", { value: doc.ddt_destination })}
        ${field("ddt_parcels", "Colli", { type: "number", min: 0, value: doc.ddt_parcels ?? "" })}
        ${field("ddt_weight", "Peso (kg)", { type: "number", step: "any", min: 0, value: doc.ddt_weight ?? "" })}
      </div>` : ""}`,
    onSubmit: async fd => {
      const payload = {
        client_id: parseInt(fd.get("client_id")),
        project_id: fd.get("project_id") ? parseInt(fd.get("project_id")) : null,
        date: fd.get("date") || null,
        due_date: fd.get("due_date") || null,
        notes: fd.get("notes") || "",
      };
      if (doc.status !== "pagata") {
        payload.discount = num(fd.get("discount"));
        payload.discount_pct = num(fd.get("discount_pct"));
        payload.tax_rate = num(fd.get("tax_rate"));
        payload.vat_nature = fd.get("vat_nature") || "";
      }
      if (doc.kind === "DDT") {
        payload.ddt_reason = fd.get("ddt_reason") || "";
        payload.ddt_carrier = fd.get("ddt_carrier") || "";
        payload.ddt_destination = fd.get("ddt_destination") || "";
        payload.ddt_parcels = fd.get("ddt_parcels") ? parseInt(fd.get("ddt_parcels")) : null;
        payload.ddt_weight = fd.get("ddt_weight") ? num(fd.get("ddt_weight")) : null;
      }
      await api("/documents/" + doc.id, { method: "PUT", json: payload });
      closeModal(); toast("Documento aggiornato", "success"); render();
    },
  });
  api("/projects").then(projects => {
    $("#ne-project").insertAdjacentHTML("beforeend",
      projects.map(p => `<option value="${p.id}" ${doc.project_id === p.id ? "selected" : ""}>${esc(p.number)} — ${esc(p.title)}</option>`).join(""));
  });
  if ($("#ne-tax")) {
    const syncNature = () => $("#ne-nature").closest("label").classList.toggle("hidden", num($("#ne-tax").value) !== 0);
    $("#ne-tax").oninput = syncNature;
    syncNature();
  }
}

function printDocument(doc, client, s) {
  $("#print-area").innerHTML = `
    <div class="print-doc">
      <div class="p-head">
        <div>
          <div style="font-weight:800;font-size:17px">${esc(s.company_name || "—")}</div>
          <div style="font-size:12px;line-height:1.5">
            ${esc(s.company_address || "")}${s.company_address && (s.company_zip || s.company_city) ? " — " : ""}
            ${esc(s.company_zip || "")} ${esc(s.company_city || "")}<br>
            ${s.company_vat ? "P.IVA " + esc(s.company_vat) : ""}
            ${s.company_tax_code ? " · CF " + esc(s.company_tax_code) : ""}
            ${s.company_phone ? " · Tel. " + esc(s.company_phone) : ""}
            ${s.company_email ? " · " + esc(s.company_email) : ""}
          </div>
        </div>
        <div style="text-align:right">
          <div class="p-title">${esc(doc.kind)}</div>
          <div style="font-size:13px">N. <b>${esc(doc.number)}</b></div>
          <div style="font-size:13px">Data: ${fmtDate(doc.date)}</div>
          ${doc.due_date ? `<div style="font-size:13px">Scadenza: ${fmtDate(doc.due_date)}</div>` : ""}
        </div>
      </div>
      <div style="margin-bottom:10px">
        <div style="font-size:11px;text-transform:uppercase;color:#555">Spett.le</div>
        <div style="font-weight:800;font-size:15px">${esc(client?.name || "")} ${client?.code ? "(" + esc(client.code) + ")" : ""}</div>
        <div style="font-size:12px">${esc([client?.address, client?.zip, client?.city].filter(Boolean).join(", "))}</div>
        ${client?.vat ? `<div style="font-size:12px">P.IVA ${esc(client.vat)}</div>` : ""}
        ${doc.kind === "DDT" && client?.ship_to ? `<div style="font-size:12px">Destinazione: ${esc(client.ship_to)}</div>` : ""}
      </div>
      ${doc.kind === "DDT" ? `
      <div style="font-size:12px;margin-bottom:6px">
        ${doc.ddt_reason ? "Causale: " + esc(doc.ddt_reason) + " · " : ""}
        ${doc.ddt_carrier ? "Vettore: " + esc(doc.ddt_carrier) + " · " : ""}
        ${doc.ddt_destination ? "Destinazione: " + esc(doc.ddt_destination) : ""}
      </div>` : ""}
      <table>
        <thead><tr><th>Descrizione</th><th style="width:80px">Qtà</th><th style="width:110px">Prezzo unit.</th><th style="width:110px">Totale</th></tr></thead>
        <tbody>
          ${doc.lines.map(l => `
            <tr><td>${esc(l.description)}</td><td>${lineQty(l)}</td><td>${linePrice(l)}</td><td>${fmtEur(lineTotal(l))}</td></tr>`).join("")}
        </tbody>
      </table>
      <div class="p-totals">
        <div><span>Subtotale</span><span>${fmtEur(doc.subtotal)}</span></div>
        ${doc.discount_amount ? `<div><span>Sconto${doc.discount_pct ? " " + fmtNum(doc.discount_pct) + "%" : ""}</span><span>- ${fmtEur(doc.discount_amount)}</span></div>` : ""}
        <div><span>Imponibile</span><span>${fmtEur(doc.taxable)}</span></div>
        <div><span>IVA ${fmtNum(doc.tax_rate)}%${doc.vat_nature ? " (" + esc(doc.vat_nature) + ")" : ""}</span><span>${fmtEur(doc.tax)}</span></div>
        <div class="grand"><span>TOTALE</span><span>${fmtEur(doc.total)}</span></div>
      </div>
      <div class="p-footer">
        ${doc.due_date && doc.kind !== "DDT" ? "Scadenza pagamento: " + fmtDate(doc.due_date) + "<br>" : ""}
        ${s.iban ? "IBAN: " + esc(s.iban) + "<br>" : ""}
        ${doc.notes ? esc(doc.notes) + "<br>" : ""}
        Documento stampato il ${new Date().toLocaleString("it-IT")} — Cantiere Navale Pro
      </div>
    </div>`;
  window.print();
}

/* ============ Scadenzario ============ */

route(/^\/scadenzario$/, async () => {
  const rows = await api("/scadenzario");
  await loadClients();
  const totalRes = rows.reduce((a, r) => a + r.residual, 0);
  const overdue = rows.filter(r => r.days_overdue > 0);

  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("calendar")} Scadenzario</h1><div class="sub">Fatture non saldate, ordinate per scadenza</div></div>
    </div>
    <div class="stats-grid">
      <div class="stat bad"><div class="label">Da incassare</div><div class="value money">${fmtEur(totalRes)}</div><div class="hint">${rows.length} fattur${rows.length === 1 ? "a" : "e"}</div></div>
      <div class="stat bad"><div class="label">Scadute</div><div class="value money">${fmtEur(overdue.reduce((a, r) => a + r.residual, 0))}</div><div class="hint">${overdue.length} fattur${overdue.length === 1 ? "a" : "e"} oltre scadenza</div></div>
    </div>
    <div class="card">
      <table class="tbl">
        <thead><tr><th>Numero</th><th>Cliente</th><th>Data fattura</th><th>Scadenza</th><th class="num">Totale</th><th class="num">Pagato</th><th class="num">Residuo</th><th>Ritardo</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${rows.length ? rows.map(r => `
            <tr>
              <td><a href="#/documenti/${r.id}"><b>${esc(r.number)}</b></a></td>
              <td>${esc(r.client_name)}</td>
              <td>${fmtDate(r.date)}</td>
              <td>${fmtDate(r.due_date)}</td>
              <td class="num">${fmtEur(r.total)}</td>
              <td class="num">${fmtEur(r.paid)}</td>
              <td class="num"><b>${fmtEur(r.residual)}</b></td>
              <td>${r.days_overdue > 0 ? `<span class="badge badge-red">${r.days_overdue} gg</span>` : `<span class="badge badge-green">in tempo</span>`}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm btn-primary" data-pay="${r.id}" data-res="${r.residual}">${icon("wallet", 13)} Pagamento</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="9">Nessuna fattura da incassare 🎉</td></tr>`}
        </tbody>
      </table>
    </div>`;

  $$("[data-pay]").forEach(b => b.onclick = () => {
    const res = num(b.dataset.res);
    modalForm({
      title: "Registra pagamento",
      body: `
        <div class="form-grid">
          ${field("amount", "Importo (€)", { type: "number", step: "any", min: "0.01", required: true, value: res })}
          ${field("method", "Metodo", { type: "select", options: `<option value="bonifico">Bonifico</option><option value="contanti">Contanti</option><option value="carta">Carta</option><option value="assegno">Assegno</option>` })}
        </div>`,
      submitLabel: "Registra",
      onSubmit: async fd => {
        await api(`/documents/${b.dataset.pay}/payments`, {
          method: "POST",
          json: { amount: num(fd.get("amount")), method: fd.get("method") },
        });
        closeModal(); toast("Pagamento registrato", "success"); render();
      },
    });
  });
});

/* ============ Archivio documentale ============ */

let archiveFolderId = null;
let archiveQuery = "";

route(/^\/archivio$/, async () => {
  const folders = await api("/archive/folders");
  if (archiveFolderId == null || !folders.some(f => f.id === archiveFolderId)) {
    archiveFolderId = folders.length ? folders[0].id : null;
  }
  const filesQs = new URLSearchParams();
  if (archiveFolderId) filesQs.set("folder_id", archiveFolderId);
  if (archiveQuery) filesQs.set("q", archiveQuery);
  const files = await api("/archive/files" + (filesQs.toString() ? "?" + filesQs.toString() : ""));
  const currentFolder = folders.find(f => f.id === archiveFolderId);

  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("archive")} Archivio</h1><div class="sub">Documentazione generica del cantiere</div></div>
      <div class="head-actions">
        <button class="btn" id="add-folder">${icon("plus", 14)} Nuova cartella</button>
        <button class="btn btn-primary" id="upload-arc" ${archiveFolderId ? "" : "disabled"}>${icon("upload", 14)} Carica file</button>
      </div>
    </div>
    <div class="grid-3-1">
      <div class="card">
        <h2>${icon("folder", 15)} Cartelle</h2>
        <div class="folder-list">
          ${folders.length ? folders.map(f => `
            <div class="folder-item ${f.id === archiveFolderId ? "active" : ""}" data-folder="${f.id}">
              ${icon("folder", 15)} ${esc(f.name)}
              <span class="fc">${f.file_count}</span>
              <button class="btn btn-sm" data-fedit="${f.id}" title="Rinomina" style="margin-left:6px;padding:2px 6px">${icon("edit", 12)}</button>
            </div>`).join("") : `<p style="color:var(--muted)">Nessuna cartella: creane una</p>`}
        </div>
        ${currentFolder && currentFolder.file_count === 0 ? `<div style="margin-top:14px"><button class="btn btn-sm btn-danger" id="del-folder">${icon("trash", 13)} Elimina cartella vuota</button></div>` : ""}
      </div>
      <div class="card">
        <h2>${icon("file", 15)} File ${currentFolder ? `— ${esc(currentFolder.name)}` : ""} <span class="count">${files.length}</span></h2>
        <div class="toolbar">
          <input type="text" id="arc-search" placeholder="Cerca file o note…" value="${esc(archiveQuery)}">
          <input type="file" id="arc-file" class="hidden">
        </div>
        <table class="tbl">
          <thead><tr><th>Nome</th><th>Note</th><th>Dimensione</th><th>Caricato</th><th class="num">Azioni</th></tr></thead>
          <tbody>
            ${files.length ? files.map(a => `
              <tr>
                <td class="primary">${icon("file", 14)} ${esc(a.filename)}</td>
                <td>${esc(a.notes || "—")}</td>
                <td>${fmtSize(a.file_size)}</td>
                <td>${fmtDateTime(a.created_at)}</td>
                <td class="num"><div class="actions">
                  <button class="btn btn-sm" data-dl="${a.id}">${icon("download", 13)} Scarica</button>
                  <button class="btn btn-sm btn-danger" data-rm="${a.id}">${icon("trash", 13)}</button>
                </div></td>
              </tr>`).join("") : `<tr class="empty-row"><td colspan="5">Nessun file ${archiveQuery ? "per la ricerca" : "in questa cartella"}</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>`;

  $$(".folder-item").forEach(f => f.onclick = () => { archiveFolderId = parseInt(f.dataset.folder); archiveQuery = ""; render(); });
  $$("[data-fedit]").forEach(b => b.onclick = e => {
    e.stopPropagation();
    const folder = folders.find(x => x.id == b.dataset.fedit);
    modalForm({
      title: `Rinomina cartella`,
      body: `${field("name", "Nome", { required: true, value: folder.name })}${field("description", "Descrizione", { value: folder.description })}`,
      submitLabel: "Rinomina",
      onSubmit: async fd => {
        const payload = Object.fromEntries(fd.entries());
        await api("/archive/folders/" + folder.id, { method: "PUT", json: payload });
        closeModal(); toast("Cartella aggiornata", "success"); render();
      },
    });
  });
  if ($("#del-folder")) $("#del-folder").onclick = () => confirmDialog(`Eliminare la cartella “${currentFolder.name}”?`, async () => {
    try { await api("/archive/folders/" + archiveFolderId, { method: "DELETE" }); archiveFolderId = null; toast("Cartella eliminata", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  });
  $("#add-folder").onclick = () => {
    modalForm({
      title: "Nuova cartella archivio",
      body: `${field("name", "Nome", { required: true, placeholder: "es. Autorizzazioni" })}${field("description", "Descrizione")}`,
      onSubmit: async fd => {
        const payload = Object.fromEntries(fd.entries());
        await api("/archive/folders", { method: "POST", json: payload });
        closeModal(); toast("Cartella creata", "success"); render();
      },
    });
  };
  $("#upload-arc").onclick = () => $("#arc-file").click();
  $("#arc-file").onchange = async e => {
    if (!e.target.files.length) return;
    const fd = new FormData();
    fd.append("file", e.target.files[0]);
    const notes = prompt("Note sul file (opzionale):") || "";
    try {
      await api(`/archive/files?folder_id=${archiveFolderId}&notes=${encodeURIComponent(notes)}`, { method: "POST", body: fd });
      toast("File caricato in archivio", "success"); render();
    } catch (err) { toast(err.message, "error"); }
  };
  let at = null;
  $("#arc-search").oninput = e => { clearTimeout(at); at = setTimeout(() => { archiveQuery = e.target.value.trim(); render(); }, 350); };
  $$("[data-dl]").forEach(b => b.onclick = () => {
    const f = files.find(x => x.id == b.dataset.dl);
    downloadFile(`/archive/files/${f.id}/download`, f.filename);
  });
  $$("[data-rm]").forEach(b => b.onclick = () => confirmDialog("Rimuovere questo file dall'archivio?", async () => {
    try { await api("/archive/files/" + b.dataset.rm, { method: "DELETE" }); toast("File rimosso", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));
});

/* ============ Acquisti ============ */

let acquistiTab = "fatture";

route(/^\/acquisti$/, async () => {
  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("cart")} Acquisti</h1><div class="sub">Fatture dei fornitori, ordini e registro IVA</div></div>
      <div class="head-actions" id="acq-actions"></div>
    </div>
    <div class="tabs" id="acq-tabs">
      <button data-tab="fatture" class="${acquistiTab === "fatture" ? "active" : ""}">Fatture di acquisto</button>
      <button data-tab="ordini" class="${acquistiTab === "ordini" ? "active" : ""}">Ordini</button>
      <button data-tab="registro" class="${acquistiTab === "registro" ? "active" : ""}">Registro IVA</button>
      <button data-tab="fornitori" class="${acquistiTab === "fornitori" ? "active" : ""}">Fornitori</button>
    </div>
    <div id="acq-content"></div>`;

  $$("#acq-tabs button").forEach(b => b.onclick = () => { acquistiTab = b.dataset.tab; render(); });

  if (acquistiTab === "fatture") await acqFatture();
  if (acquistiTab === "ordini") await acqOrdini();
  if (acquistiTab === "registro") await acqRegistro();
  if (acquistiTab === "fornitori") await acqFornitori();
});

async function acqFatture() {
  const [invoices, suppliers] = await Promise.all([api("/purchase-invoices"), api("/suppliers")]);
  $("#acq-actions").innerHTML = `<button class="btn btn-primary" id="add-pinv" ${suppliers.length ? "" : "disabled title='Aggiungi prima un fornitore'"}>${icon("plus", 14)} Nuova fattura</button>`;
  $("#add-pinv").onclick = () => purchaseInvoiceModal();
  $("#acq-content").innerHTML = `
    <div class="card">
      <table class="tbl">
        <thead><tr><th>Numero</th><th>Fornitore</th><th>Data</th><th>Scadenza</th><th class="num">Imponibile</th><th class="num">IVA</th><th class="num">Totale</th><th>Stato</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${invoices.length ? invoices.map(v => `
            <tr>
              <td><b>${esc(v.number || "s/n")}</b></td>
              <td>${esc(v.supplier_name)}</td>
              <td>${fmtDate(v.date)}</td>
              <td>${fmtDate(v.due_date)}</td>
              <td class="num">${fmtEur(v.amount_net)}</td>
              <td class="num">${fmtEur(v.vat)}</td>
              <td class="num"><b>${fmtEur(v.total)}</b></td>
              <td>${v.status === "pagata" ? `<span class="badge badge-green">Pagata</span>` : `<span class="badge badge-red">Da pagare</span>`}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-pedit="${v.id}">${icon("edit", 13)}</button>
                <button class="btn btn-sm" data-ppay="${v.id}">${v.status === "pagata" ? "Riapri" : "Pagata"}</button>
                <button class="btn btn-sm btn-danger" data-pdel="${v.id}">${icon("trash", 13)}</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="9">Nessuna fattura di acquisto</td></tr>`}
        </tbody>
      </table>
    </div>`;
  $$("[data-pedit]").forEach(b => b.onclick = () => purchaseInvoiceModal(invoices.find(x => x.id == b.dataset.pedit)));
  $$("[data-ppay]").forEach(b => b.onclick = () => {
    const v = invoices.find(x => x.id == b.dataset.ppay);
    purchaseInvoiceModal(v, v.status === "pagata" ? "da_pagare" : "pagata");
  });
  $$("[data-pdel]").forEach(b => b.onclick = () => confirmDialog("Eliminare questa fattura di acquisto?", async () => {
    try { await api("/purchase-invoices/" + b.dataset.pdel, { method: "DELETE" }); toast("Fattura eliminata", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));
}

function purchaseInvoiceModal(inv = null, forceStatus = null) {
  const v = inv || {};
  api("/suppliers").then(suppliers => {
    modalForm({
      title: inv ? "Modifica fattura di acquisto" : "Nuova fattura di acquisto",
      body: `
        <div class="form-grid">
          ${field("supplier_id", "Fornitore", { type: "select", required: true, options: `<option value="">— scegli —</option>` + suppliers.map(s => `<option value="${s.id}" ${v.supplier_id === s.id ? "selected" : ""}>${esc(s.name)}</option>`).join("") })}
          ${field("number", "Numero fattura fornitore", { value: v.number || "" })}
          ${field("date", "Data", { type: "date", value: v.date || todayISO() })}
          ${field("due_date", "Scadenza", { type: "date", value: v.due_date || "" })}
          ${field("amount_net", "Imponibile (€)", { type: "number", step: "any", min: 0, required: true, value: v.amount_net ?? "" })}
          ${field("vat_rate", "IVA %", { type: "number", step: "any", min: 0, value: v.vat_rate ?? 22 })}
          ${field("status", "Stato", { type: "select", options: `<option value="da_pagare" ${forceStatus === "da_pagare" || (!forceStatus && v.status !== "pagata") ? "selected" : ""}>Da pagare</option><option value="pagata" ${forceStatus === "pagata" || (!forceStatus && v.status === "pagata") ? "selected" : ""}>Pagata</option>` })}
          ${field("paid_date", "Data pagamento", { type: "date", value: v.paid_date || "" })}
          ${field("notes", "Note", { type: "textarea", value: v.notes, full: true })}
        </div>`,
      onSubmit: async fd => {
        const payload = Object.fromEntries(fd.entries());
        payload.supplier_id = parseInt(payload.supplier_id);
        payload.amount_net = num(payload.amount_net);
        payload.vat_rate = num(payload.vat_rate);
        payload.due_date = payload.due_date || null;
        payload.paid_date = payload.paid_date || null;
        if (inv) await api("/purchase-invoices/" + inv.id, { method: "PUT", json: payload });
        else await api("/purchase-invoices", { method: "POST", json: payload });
        closeModal(); toast("Fattura salvata", "success"); render();
      },
    });
  });
}

async function acqOrdini() {
  const orders = await api("/purchase-orders");
  $("#acq-actions").innerHTML = `<button class="btn btn-primary" id="add-po">${icon("plus", 14)} Nuovo ordine</button>`;
  $("#add-po").onclick = () => purchaseOrderModal();
  $("#acq-content").innerHTML = `
    <div class="card">
      <table class="tbl">
        <thead><tr><th>Numero</th><th>Fornitore</th><th>Data</th><th>Consegna prevista</th><th class="num">Righe</th><th class="num">Totale</th><th>Stato</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${orders.length ? orders.map(o => {
            const total = o.lines.reduce((a, l) => a + l.qty * l.unit_cost, 0);
            return `
            <tr>
              <td><a href="#/ordini/${o.id}"><b>${esc(o.number)}</b></a></td>
              <td>${esc(o.supplier_name)}</td>
              <td>${fmtDate(o.date)}</td>
              <td>${fmtDate(o.expected_date)}</td>
              <td class="num">${o.lines.length}</td>
              <td class="num"><b>${fmtEur(total)}</b></td>
              <td>${badge(PO_STATUS, o.status)}</td>
              <td class="num"><div class="actions">
                <a class="btn btn-sm" href="#/ordini/${o.id}">${icon("eye", 13)} Apri</a>
                <button class="btn btn-sm btn-danger" data-odel="${o.id}">${icon("trash", 13)}</button>
              </div></td>
            </tr>`;
          }).join("") : `<tr class="empty-row"><td colspan="8">Nessun ordine</td></tr>`}
        </tbody>
      </table>
    </div>`;
  $$("[data-odel]").forEach(b => b.onclick = () => confirmDialog("Eliminare questo ordine?", async () => {
    try { await api("/purchase-orders/" + b.dataset.odel, { method: "DELETE" }); toast("Ordine eliminato", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));
}

const PO_STATUS = {
  bozza: ["Bozza", "badge-gray"],
  inviato: ["Inviato", "badge-blue"],
  ricevuto: ["Ricevuto", "badge-green"],
  annullato: ["Annullato", "badge-red"],
};

async function purchaseOrderModal(po = null) {
  const [suppliers, items] = await Promise.all([api("/suppliers"), loadItems()]);
  const o = po || {};
  modalForm({
    title: po ? `Modifica ordine ${esc(o.number)}` : "Nuovo ordine di acquisto",
    wide: true,
    body: `
      <div class="form-grid">
        ${field("supplier_id", "Fornitore", { type: "select", required: true, options: `<option value="">— scegli —</option>` + suppliers.map(s => `<option value="${s.id}" ${o.supplier_id === s.id ? "selected" : ""}>${esc(s.name)}</option>`).join("") })}
        ${field("date", "Data", { type: "date", value: o.date || todayISO() })}
        ${field("expected_date", "Consegna prevista", { type: "date", value: o.expected_date || "" })}
        ${field("notes", "Note", { type: "textarea", value: o.notes, full: true })}
      </div>
      ${po ? "" : `<p style="color:var(--muted);font-size:13px">Le righe si aggiungono dopo la creazione, nella pagina dell'ordine.</p>`}`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      payload.supplier_id = parseInt(payload.supplier_id);
      payload.expected_date = payload.expected_date || null;
      payload.lines = [];
      if (po) await api("/purchase-orders/" + po.id, { method: "PUT", json: payload });
      else {
        const created = await api("/purchase-orders", { method: "POST", json: payload });
        closeModal(); toast("Ordine creato", "success");
        location.hash = "#/ordini/" + created.id;
        return;
      }
      closeModal(); toast("Ordine aggiornato", "success"); render();
    },
  });
}

/* ---- Dettaglio ordine di acquisto ---- */

route(/^\/ordini\/(\d+)$/, async (id) => {
  const po = await api("/purchase-orders/" + id);
  const total = po.lines.reduce((a, l) => a + l.qty * l.unit_cost, 0);
  $("#view").innerHTML = `
    <a class="back-link" href="#/acquisti">${icon("arrowleft", 14)} Acquisti</a>
    <div class="page-head">
      <div>
        <h1>${icon("cart")} Ordine ${esc(po.number)}</h1>
        <div class="doc-meta">
          ${badge(PO_STATUS, po.status)}
          <span>Fornitore: <b>${esc(po.supplier_name)}</b></span>
          <span>Data: ${fmtDate(po.date)}</span>
          <span>Consegna prevista: ${fmtDate(po.expected_date)}</span>
        </div>
        ${po.notes ? `<div class="doc-meta">${esc(po.notes)}</div>` : ""}
      </div>
      <div class="head-actions">
        ${["bozza", "inviato"].includes(po.status) ? `<button class="btn" id="po-status">${po.status === "bozza" ? "Segna inviato" : "Segna da ricevere"}</button>` : ""}
        ${["bozza", "inviato"].includes(po.status) ? `<button class="btn btn-primary" id="po-receive">${icon("download", 14)} Ricevi in magazzino</button>` : ""}
        <button class="btn" id="po-edit">${icon("edit", 14)} Modifica</button>
      </div>
    </div>

    <div class="card">
      <h2>${icon("clipboard", 15)} Righe ordine <span class="count">${po.lines.length}</span></h2>
      <table class="tbl">
        <thead><tr><th>Articolo</th><th>Descrizione</th><th class="num">Qtà</th><th class="num">Costo unit.</th><th class="num">Totale</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${po.lines.length ? po.lines.map(l => `
            <tr>
              <td>${l.item_name ? `<span class="badge badge-gray">${esc(l.item_name)}</span>` : "—"}</td>
              <td class="primary">${esc(l.description)}</td>
              <td class="num">${fmtNum(l.qty)}</td>
              <td class="num">${fmtEur(l.unit_cost)}</td>
              <td class="num"><b>${fmtEur(l.qty * l.unit_cost)}</b></td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-olEdit="${l.id}">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-olDel="${l.id}">${icon("trash", 13)}</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="6">Nessuna riga</td></tr>`}
        </tbody>
      </table>
      ${po.status !== "ricevuto" ? `
      <form class="inline-form" id="po-line-form" style="margin-top:14px">
        <label class="field" style="min-width:180px">Articolo (opz.)
          <select name="item_id" id="pol-item"><option value="">— libero —</option>
            ${cache.items.length ? "" : ""}${(await loadItems()).map(i => `<option value="${i.id}">${esc(i.name)}</option>`).join("")}
          </select></label>
        <label class="field" style="flex:2;min-width:200px">Descrizione<input name="description" required></label>
        <label class="field">Qtà<input name="qty" type="number" step="any" min="0.01" value="1" required></label>
        <label class="field">Costo (€)<input name="unit_cost" type="number" step="any" min="0" value="0"></label>
        <button class="btn btn-primary">${icon("plus", 13)} Aggiungi</button>
      </form>` : ""}
    </div>

    <div class="grid-2">
      <div class="card">
        <h2>${icon("wallet", 15)} Riepilogo</h2>
        <div class="totals-box" style="margin:0">
          <div class="row"><span>Righe</span><span>${po.lines.length}</span></div>
          <div class="row grand"><span>Totale ordine</span><span>${fmtEur(total)}</span></div>
        </div>
        ${po.status === "ricevuto" ? `<p style="color:var(--green);font-weight:600;margin-top:12px">${icon("check", 14)} Ordine ricevuto: i carichi sono stati registrati in magazzino.</p>` : ""}
      </div>
      <div class="card">
        <h2>${icon("info" , 15)} Come funziona</h2>
        <p style="color:var(--muted);font-size:13.5px">"Ricevi in magazzino" genera automaticamente i <b>movimenti di carico</b> per ogni riga collegata a un articolo, con il costo dell'ordine, e chiude l'ordine.</p>
      </div>
    </div>`;

  if ($("#po-line-form")) {
    $("#pol-item").onchange = e => {
      const item = (cache.items || []).find(i => i.id === parseInt(e.target.value));
      if (item) {
        const form = $("#po-line-form");
        form.querySelector('[name="description"]').value = item.name;
        form.querySelector('[name="unit_cost"]').value = item.cost ?? 0;
      }
    };
    $("#po-line-form").onsubmit = async e => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const payload = {
        supplier_id: po.supplier_id,
        date: po.date,
        expected_date: po.expected_date,
        notes: po.notes,
        lines: [...po.lines.map(l => ({ item_id: l.item_id, description: l.description, qty: l.qty, unit_cost: l.unit_cost })),
          { item_id: fd.get("item_id") ? parseInt(fd.get("item_id")) : null, description: fd.get("description"), qty: num(fd.get("qty")), unit_cost: num(fd.get("unit_cost")) }],
      };
      try { await api("/purchase-orders/" + id, { method: "PUT", json: payload }); toast("Riga aggiunta", "success"); render(); }
      catch (err) { toast(err.message, "error"); }
    };
    $$("[data-olDel]").forEach(b => b.onclick = () => confirmDialog("Rimuovere questa riga?", async () => {
      const lines = po.lines.filter(l => l.id != b.dataset.olDel).map(l => ({ item_id: l.item_id, description: l.description, qty: l.qty, unit_cost: l.unit_cost }));
      try {
        await api("/purchase-orders/" + id, { method: "PUT", json: { supplier_id: po.supplier_id, date: po.date, expected_date: po.expected_date, notes: po.notes, lines } });
        toast("Riga rimossa", "success"); render();
      } catch (err) { toast(err.message, "error"); }
    }));
    $$("[data-olEdit]").forEach(b => b.onclick = () => {
      const line = po.lines.find(l => l.id == b.dataset.olEdit);
      modalForm({
        title: "Modifica riga ordine",
        body: `
          <div class="form-grid">
            ${field("description", "Descrizione", { required: true, value: line.description, full: true })}
            ${field("qty", "Quantità", { type: "number", step: "any", min: 0.01, value: line.qty })}
            ${field("unit_cost", "Costo unitario (€)", { type: "number", step: "any", min: 0, value: line.unit_cost })}
          </div>`,
        onSubmit: async fd => {
          const updated = po.lines.map(l => l.id === line.id
            ? { item_id: l.item_id, description: fd.get("description"), qty: num(fd.get("qty")), unit_cost: num(fd.get("unit_cost")) }
            : { item_id: l.item_id, description: l.description, qty: l.qty, unit_cost: l.unit_cost });
          try {
            await api("/purchase-orders/" + id, { method: "PUT", json: { supplier_id: po.supplier_id, date: po.date, expected_date: po.expected_date, notes: po.notes, lines: updated } });
            closeModal(); toast("Riga aggiornata", "success"); render();
          } catch (err) { showError(err); }
        },
      });
    });
  }
  if ($("#po-status")) $("#po-status").onclick = async () => {
    const next = po.status === "bozza" ? "inviato" : "inviato";
    try { await api(`/purchase-orders/${id}/status?status_value=${next}`, { method: "POST" }); toast("Stato aggiornato", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  };
  if ($("#po-receive")) $("#po-receive").onclick = () => {
    api("/warehouses").then(warehouses => {
      modalForm({
        title: "Ricevi ordine in magazzino",
        body: field("warehouse_id", "Magazzino di destinazione", { type: "select", required: true, options: warehouses.map(w => `<option value="${w.id}">${esc(w.name)}</option>`).join("") }),
        submitLabel: "Ricevi e carica",
        onSubmit: async fd => {
          const res = await api(`/purchase-orders/${id}/receive?warehouse_id=${fd.get("warehouse_id")}`, { method: "POST" });
          closeModal();
          toast(`Ordine ricevuto: ${res.received_lines} righe caricate su ${res.total_lines}`, "success");
          render();
        },
      });
    });
  };
  $("#po-edit").onclick = () => purchaseOrderModal(po);
});

async function acqRegistro() {
  const year = acqRegistroYear || Date.today ? (acqRegistroYear || new Date().getFullYear()) : new Date().getFullYear();
  const reg = await api("/vat-register?year=" + year);
  $("#acq-actions").innerHTML = `<button class="btn" id="reg-csv">${icon("download", 14)} CSV acquisti</button>`;
  $("#reg-csv").onclick = () => downloadFile(`/purchase-invoices/export?year=${year}`, `registro_iva_acquisti_${year}.csv`);
  $("#acq-content").innerHTML = `
    <div class="toolbar">
      <label class="field" style="margin:0">Anno
        <select id="reg-year">${[0, 1, 2].map(i => {
          const y = new Date().getFullYear() - i;
          return `<option ${y === +year ? "selected" : ""}>${y}</option>`;
        }).join("")}</select></label>
    </div>
    <div class="stats-grid">
      <div class="stat bad"><div class="label">IVA a debito (vendite)</div><div class="value money">${fmtEur(reg.summary.sales_vat)}</div><div class="hint">imponibile ${fmtEur(reg.summary.sales_taxable)}</div></div>
      <div class="stat good"><div class="label">IVA a credito (acquisti)</div><div class="value money">${fmtEur(reg.summary.purchases_vat)}</div><div class="hint">imponibile ${fmtEur(reg.summary.purchases_net)}</div></div>
      <div class="stat ${reg.summary.balance >= 0 ? "bad" : "good"}"><div class="label">Saldo IVA</div><div class="value money">${fmtEur(Math.abs(reg.summary.balance))}</div><div class="hint">${reg.summary.balance >= 0 ? "a debito" : "a credito"}</div></div>
    </div>
    ${(reg.sales_by_rate.length || reg.purchases_by_rate.length) ? `
    <div class="card">
      <h2>${icon("euro", 15)} Riepilogo per aliquota</h2>
      <table class="tbl">
        <thead><tr><th>Aliquota</th><th class="num">Imponibile vendite</th><th class="num">IVA vendite</th><th class="num">Imponibile acquisti</th><th class="num">IVA acquisti</th></tr></thead>
        <tbody>${[...new Set([...reg.sales_by_rate, ...reg.purchases_by_rate].map(r => r.rate))].sort((a, b) => a - b).map(rate => {
          const sl = reg.sales_by_rate.find(r => r.rate === rate) || { taxable: 0, vat: 0 };
          const pu = reg.purchases_by_rate.find(r => r.rate === rate) || { taxable: 0, vat: 0 };
          return `<tr><td>${fmtNum(rate)}%</td><td class="num">${fmtEur(sl.taxable)}</td><td class="num">${fmtEur(sl.vat)}</td><td class="num">${fmtEur(pu.taxable)}</td><td class="num">${fmtEur(pu.vat)}</td></tr>`;
        }).join("")}</tbody>
      </table>
    </div>` : ""}
    <div class="grid-2">
      <div class="card">
        <h2>${icon("file", 15)} Vendite (${reg.sales.length})</h2>
        <table class="tbl">
          <thead><tr><th>Numero</th><th>Cliente</th><th class="num">Imponibile</th><th class="num">IVA</th></tr></thead>
          <tbody>
            ${reg.sales.length ? reg.sales.map(s => `
              <tr><td>${esc(s.number)}</td><td>${esc(s.client_name)}</td><td class="num">${fmtEur(s.taxable)}</td><td class="num">${fmtEur(s.vat)}</td></tr>`).join("")
              : `<tr class="empty-row"><td colspan="4">Nessuna fattura emessa</td></tr>`}
          </tbody>
        </table>
      </div>
      <div class="card">
        <h2>${icon("cart", 15)} Acquisti (${reg.purchases.length})</h2>
        <table class="tbl">
          <thead><tr><th>Numero</th><th>Fornitore</th><th class="num">Imponibile</th><th class="num">IVA</th></tr></thead>
          <tbody>
            ${reg.purchases.length ? reg.purchases.map(s => `
              <tr><td>${esc(s.number || "s/n")}</td><td>${esc(s.supplier_name)}</td><td class="num">${fmtEur(s.amount_net)}</td><td class="num">${fmtEur(s.vat)}</td></tr>`).join("")
              : `<tr class="empty-row"><td colspan="4">Nessuna fattura di acquisto</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>`;
  $("#reg-year").onchange = e => { acqRegistroYear = parseInt(e.target.value); render(); };
}
let acqRegistroYear = null;

async function acqFornitori() {
  const suppliers = await api("/suppliers");
  $("#acq-actions").innerHTML = `<button class="btn btn-primary" id="add-sup">${icon("plus", 14)} Nuovo fornitore</button>`;
  $("#add-sup").onclick = () => supplierModal();
  $("#acq-content").innerHTML = `
    <div class="card">
      <table class="tbl">
        <thead><tr><th>Fornitore</th><th>P.IVA</th><th>Contatti</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${suppliers.length ? suppliers.map(s => `
            <tr>
              <td class="primary">${esc(s.name)}</td>
              <td>${esc(s.vat || "—")}</td>
              <td>${esc(s.email || s.phone || "—")}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-sedit="${s.id}">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-sdel="${s.id}">${icon("trash", 13)}</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="4">Nessun fornitore</td></tr>`}
        </tbody>
      </table>
    </div>`;
  $$("[data-sedit]").forEach(b => b.onclick = () => supplierModal(suppliers.find(x => x.id == b.dataset.sedit)));
  $$("[data-sdel]").forEach(b => b.onclick = () => {
    const s = suppliers.find(x => x.id == b.dataset.sdel);
    confirmDialog(`Eliminare il fornitore “${s.name}”?`, async () => {
      try { await api("/suppliers/" + s.id, { method: "DELETE" }); toast("Fornitore eliminato", "success"); render(); }
      catch (err) { toast(err.message, "error"); }
    });
  });
}

function supplierModal(supplier = null) {
  const s = supplier || {};
  modalForm({
    title: supplier ? "Modifica fornitore" : "Nuovo fornitore",
    body: `
      <div class="form-grid">
        ${field("name", "Nome / Ragione sociale", { required: true, value: s.name, full: true })}
        ${field("vat", "Partita IVA", { value: s.vat })}
        ${field("email", "Email", { type: "email", value: s.email })}
        ${field("phone", "Telefono", { value: s.phone })}
        ${field("address", "Indirizzo", { value: s.address, full: true })}
        ${field("notes", "Note", { type: "textarea", value: s.notes, full: true })}
      </div>`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      if (supplier) await api("/suppliers/" + supplier.id, { method: "PUT", json: payload });
      else await api("/suppliers", { method: "POST", json: payload });
      closeModal(); toast("Fornitore salvato", "success"); render();
    },
  });
}

/* ============ Agenda scalo ============ */

const MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"];
let agendaY = null, agendaM = null, agendaResource = null;

route(/^\/agenda$/, async () => {
  if (agendaY == null) {
    const now = new Date();
    agendaY = now.getFullYear(); agendaM = now.getMonth(); // 0-based
  }
  const [bookings, resources, boats] = await Promise.all([
    api(`/bookings?year=${agendaY}&month=${agendaM + 1}`),
    api("/resources"),
    loadBoats(),
  ]);
  const filtered = agendaResource ? bookings.filter(b => b.resource_id === agendaResource) : bookings;
  await loadClients();

  // prossimi scali (30 giorni)
  const today = new Date(todayISO());
  const in30 = new Date(today); in30.setDate(in30.getDate() + 30);
  const upcoming = (await api("/bookings")).filter(b =>
    ["pianificato", "in_corso"].includes(b.status) &&
    new Date(b.end_date) >= today && new Date(b.start_date) <= in30
  ).sort((a, b) => a.start_date.localeCompare(b.start_date));

  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("calendar")} Agenda scalo</h1><div class="sub">Viaggi, botteghe e postazioni</div></div>
      <div class="head-actions">
        <button class="btn" id="mgr-resources">${icon("settings", 14)} Postazioni</button>
        <button class="btn btn-primary" id="add-booking" ${resources.length ? "" : "disabled title='Crea prima una postazione'"}>${icon("plus", 14)} Nuova prenotazione</button>
      </div>
    </div>

    ${upcoming.some(b => b.status === "in_corso") ? `<div class="alert-banner warn">${icon("alert", 16)} ${upcoming.filter(b => b.status === "in_corso").length} scal${upcoming.filter(b => b.status === "in_corso").length === 1 ? "o" : "i"} in corso ora</div>` : ""}

    <div class="card">
      <div class="cal-head">
        <button class="btn btn-sm" id="cal-prev">‹</button>
        <span class="cal-title">${MESI[agendaM]} ${agendaY}</span>
        <button class="btn btn-sm" id="cal-next">›</button>
        <select id="cal-resource" style="padding:6px 10px;border:1.5px solid var(--border);border-radius:8px">
          <option value="">Tutte le postazioni</option>
          ${resources.map(r => `<option value="${r.id}" ${agendaResource === r.id ? "selected" : ""}>${esc(r.name)}</option>`).join("")}
        </select>
        <div class="spacer" style="flex:1"></div>
        <div class="cal-legend">
          <span><span class="sw" style="background:var(--blue-bg)"></span>Pianificato</span>
          <span><span class="sw" style="background:var(--amber-bg)"></span>In corso</span>
          <span><span class="sw" style="background:var(--green-bg)"></span>Completato</span>
        </div>
      </div>
      <div class="cal-grid" id="cal-grid"></div>
    </div>

    <div class="card">
      <h2>${icon("calendar", 15)} Prossimi 30 giorni <span class="count">${upcoming.length}</span></h2>
      <table class="tbl">
        <thead><tr><th>Periodo</th><th>Postazione</th><th>Titolo</th><th>Imbarcazione / Commessa</th><th>Stato</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${upcoming.length ? upcoming.map(b => {
            const days = Math.round((new Date(b.start_date) - today) / 86400000);
            return `
            <tr>
              <td>${fmtDate(b.start_date)} → ${fmtDate(b.end_date)}${b.status === "in_corso" ? ' <span class="badge badge-amber">in corso</span>' : days === 0 ? ' <span class="badge badge-blue">oggi</span>' : ""}</td>
              <td>${esc(b.resource_name)}</td>
              <td class="primary">${esc(b.title)}</td>
              <td>${esc(b.boat_name || "—")}${b.project_id ? ` <a href="#/commesse/${b.project_id}">→ ${esc(b.project_number)}</a>` : ""}</td>
              <td>${badge(BOOKING_STATUS, b.status)}</td>
              <td class="num"><div class="actions">
                ${b.status === "pianificato" ? `<button class="btn btn-sm" data-bstart="${b.id}">Inizia</button>` : ""}
                ${b.status === "in_corso" ? `<button class="btn btn-sm" data-bdone="${b.id}">Completa</button>` : ""}
                <button class="btn btn-sm" data-bedit="${b.id}">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-bdel="${b.id}">${icon("trash", 13)}</button>
              </div></td>
            </tr>`;
          }).join("") : `<tr class="empty-row"><td colspan="6">Nessuno scalo nei prossimi 30 giorni</td></tr>`}
        </tbody>
      </table>
    </div>`;

  // calendario mensile
  const first = new Date(agendaY, agendaM, 1);
  const startOffset = (first.getDay() + 6) % 7; // lunedì = 0
  const daysInMonth = new Date(agendaY, agendaM + 1, 0).getDate();
  const grid = $("#cal-grid");
  grid.innerHTML = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"].map(d => `<div class="cal-dow">${d}</div>`).join("");
  const todayStr = todayISO();
  for (let i = 0; i < startOffset; i++) grid.insertAdjacentHTML("beforeend", `<div class="cal-cell other"></div>`);
  for (let day = 1; day <= daysInMonth; day++) {
    const iso = `${agendaY}-${String(agendaM + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    const dayBookings = filtered.filter(b => b.start_date <= iso && b.end_date >= iso);
    grid.insertAdjacentHTML("beforeend", `
      <div class="cal-cell ${iso === todayStr ? "today" : ""}" data-day="${iso}">
        <span class="dnum">${day}</span>
        ${dayBookings.map(b => `<button class="cal-chip s-${b.status}" data-chip="${b.id}" title="${esc(b.title)} — ${esc(b.resource_name)} (${fmtDate(b.start_date)}→${fmtDate(b.end_date)})">${esc(b.title)}</button>`).join("")}
      </div>`);
  }
  $$("#cal-grid .cal-cell[data-day]").forEach(cell => cell.onclick = e => {
    if (e.target.closest("[data-chip]")) return;
    bookingModal({ start_date: cell.dataset.day, end_date: cell.dataset.day, status: "pianificato" }, null, null, resources);
  });
  $$("[data-chip]").forEach(chip => chip.onclick = e => {
    e.stopPropagation();
    const b = bookings.find(x => x.id == chip.dataset.chip);
    if (b) bookingModal(b, null, null, resources);
  });
  $("#cal-prev").onclick = () => { agendaM--; if (agendaM < 0) { agendaM = 11; agendaY--; } render(); };
  $("#cal-next").onclick = () => { agendaM++; if (agendaM > 11) { agendaM = 0; agendaY++; } render(); };
  $("#cal-resource").onchange = e => { agendaResource = e.target.value ? parseInt(e.target.value) : null; render(); };
  $("#add-booking").onclick = () => bookingModal(null, null, null, resources);
  $("#mgr-resources").onclick = () => resourcesModal();

  $$("[data-bedit]").forEach(b => b.onclick = () => bookingModal(bookings.find(x => x.id == b.dataset.bedit), null, null, resources));
  $$("[data-bdel]").forEach(b => b.onclick = () => confirmDialog("Eliminare questa prenotazione?", async () => {
    try { await api("/bookings/" + b.dataset.bdel, { method: "DELETE" }); toast("Prenotazione eliminata", "success"); render(); }
    catch (err) { toast(err.message, "error"); }
  }));
  $$("[data-bstart]").forEach(b => b.onclick = () => setBookingStatus(b.dataset.bstart, "in_corso"));
  $$("[data-bdone]").forEach(b => b.onclick = () => setBookingStatus(b.dataset.bdone, "completato"));
});

const BOOKING_STATUS = {
  pianificato: ["Pianificato", "badge-blue"],
  in_corso: ["In corso", "badge-amber"],
  completato: ["Completato", "badge-green"],
  annullato: ["Annullato", "badge-gray"],
};

async function setBookingStatus(id, status) {
  try { await api(`/bookings/${id}/status?status_value=${status}`, { method: "POST" }); toast("Stato aggiornato", "success"); render(); }
  catch (err) { toast(err.message, "error"); }
}

function bookingModal(booking = null, onSaved = null, _unused = null, resources = null) {
  const b = booking || {};
  Promise.all([
    resources ? Promise.resolve(resources) : api("/resources"),
    api("/projects"),
    loadBoats(),
  ]).then(([resList, projects]) => {
    if (!resList.length) { toast("Crea prima una postazione (Pulsante Postazioni)", "error"); return; }
    modalForm({
      title: booking ? "Modifica prenotazione" : "Nuova prenotazione",
      body: `
        <div class="form-grid">
          ${field("resource_id", "Postazione", { type: "select", required: true, options: resList.map(r => `<option value="${r.id}" ${b.resource_id === r.id ? "selected" : ""}>${esc(r.name)} (${esc(r.rtype)})</option>`).join("") })}
          ${field("title", "Titolo", { required: true, value: b.title, placeholder: "es. Hauling + carenaggio" })}
          ${field("start_date", "Dal", { type: "date", required: true, value: b.start_date || "" })}
          ${field("end_date", "Al", { type: "date", required: true, value: b.end_date || "" })}
          ${field("boat_id", "Imbarcazione", { type: "select", options: `<option value="">— nessuna —</option>` + cache.boats.map(bt => `<option value="${bt.id}" ${b.boat_id === bt.id ? "selected" : ""}>${esc(bt.name)}</option>`).join("") })}
          ${field("project_id", "Commessa", { type: "select", options: `<option value="">— nessuna —</option>` + projects.map(p => `<option value="${p.id}" ${b.project_id === p.id ? "selected" : ""}>${esc(p.number)} — ${esc(p.title)}</option>`).join("") })}
          ${field("status", "Stato", { type: "select", options: Object.entries(BOOKING_STATUS).map(([k, [l]]) => `<option value="${k}" ${b.status === k ? "selected" : ""}>${l}</option>`).join("") })}
          ${field("notes", "Note", { type: "textarea", value: b.notes, full: true })}
        </div>
        <p style="color:var(--muted);font-size:12.5px">Il sistema impedisce due prenotazioni sovrapposte sulla stessa postazione.</p>`,
      onSubmit: async fd => {
        const payload = Object.fromEntries(fd.entries());
        payload.resource_id = parseInt(payload.resource_id);
        payload.boat_id = payload.boat_id ? parseInt(payload.boat_id) : null;
        payload.project_id = payload.project_id ? parseInt(payload.project_id) : null;
        try {
          if (booking) await api("/bookings/" + booking.id, { method: "PUT", json: payload });
          else await api("/bookings", { method: "POST", json: payload });
          closeModal(); toast("Prenotazione salvata", "success");
          if (onSaved) onSaved(); else render();
        } catch (err) { showError(err); }
      },
    });
  });
}

function resourcesModal() {
  openModal(`
    <h2>Postazioni dello scalo</h2>
    <div id="res-list" class="folder-list">Carico…</div>
    <div class="modal-actions">
      <button class="btn" id="res-close">Chiudi</button>
      <button class="btn btn-primary" id="res-add">Nuova postazione</button>
    </div>`);
  $("#res-close").onclick = () => { closeModal(); render(); };
  $("#res-add").onclick = () => resourceModal(null, resourcesModal);
  paintResourcesList();
}

async function paintResourcesList() {
  const resources = await api("/resources");
  const listEl = $("#res-list");
  if (!listEl) return; // il modale è stato sostituito da un altro form: niente da aggiornare
  listEl.innerHTML = `
    <table class="tbl"><tbody>
      ${resources.length ? resources.map(r => `
        <tr>
          <td><span class="badge badge-teal">${esc(r.rtype)}</span></td>
          <td class="primary">${esc(r.name)}</td>
          <td>${esc(r.notes || "")}</td>
          <td class="num"><div class="actions">
            <button class="btn btn-sm" data-redit="${r.id}">${icon("edit", 13)}</button>
            <button class="btn btn-sm btn-danger" data-rdel="${r.id}">${icon("trash", 13)}</button>
          </div></td>
        </tr>`).join("") : `<tr class="empty-row"><td>Nessuna postazione: creane una (es. Viaggio A, Bottega 1, Seul 2…)</td></tr>`}
    </tbody></table>`;
  $$("[data-redit]", listEl).forEach(btn => btn.onclick = () => resourceModal(resources.find(x => x.id == btn.dataset.redit), resourcesModal));
  $$("[data-rdel]", listEl).forEach(btn => btn.onclick = () => {
    const r = resources.find(x => x.id == btn.dataset.rdel);
    confirmDialog(`Eliminare la postazione “${r.name}”?`, async () => {
      try { await api("/resources/" + r.id, { method: "DELETE" }); toast("Postazione eliminata", "success"); resourcesModal(); }
      catch (err) { toast(err.message, "error"); }
    });
  });
}

function resourceModal(resource = null, onSaved = null) {
  const r = resource || {};
  modalForm({
    title: resource ? "Modifica postazione" : "Nuova postazione",
    body: `
      ${field("name", "Nome", { required: true, value: r.name, placeholder: "es. Viaggio A, Bottega 1, Seul 2" })}
      ${field("rtype", "Tipo", { type: "select", options: ["Viaggio", "Bottega", "Seul", "Postazione", "Molo", "Altro"].map(t => `<option ${r.rtype === t ? "selected" : ""}>${t}</option>`).join("") })}
      ${field("notes", "Note", { type: "textarea", value: r.notes })}`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      if (resource) await api("/resources/" + resource.id, { method: "PUT", json: payload });
      else await api("/resources", { method: "POST", json: payload });
      closeModal(); toast("Postazione salvata", "success");
      if (onSaved) onSaved();
    },
  });
}

/* ============ Lavoratori ============ */

let workerFilterActive = 1;

route(/^\/lavoratori$/, async () => {
  const qs = workerFilterActive >= 0 ? `?active=${workerFilterActive}` : "";
  const workers = await api("/workers" + qs);
  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("userplus")} Lavoratori</h1><div class="sub">Squadra dello scalo con le tariffe orarie</div></div>
      <div class="head-actions"><button class="btn btn-primary" id="add-worker">${icon("plus", 14)} Nuovo lavoratore</button></div>
    </div>
    <div class="card">
      <div class="tabs">
        <button data-v="1" class="${workerFilterActive === 1 ? "active" : ""}">Attivi</button>
        <button data-v="0" class="${workerFilterActive === 0 ? "active" : ""}">Disattivi</button>
        <button data-v="-1" class="${workerFilterActive === -1 ? "active" : ""}">Tutti</button>
      </div>
      <table class="tbl">
        <thead><tr><th>Lavoratore</th><th>Ruolo</th><th class="num">Costo/h</th><th class="num">Prezzo/h</th><th>Scadenze</th><th>Stato</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${workers.length ? workers.map(w => `
            <tr>
              <td class="primary">${esc(w.name)}${w.employee_code ? `<span class="sub">matr. ${esc(w.employee_code)}</span>` : ""}</td>
              <td>${esc(w.role || "—")}</td>
              <td class="num">${fmtEur(w.hourly_cost)}</td>
              <td class="num">${fmtEur(w.hourly_price)}</td>
              <td>${workerExpiryBadges(w)}</td>
              <td>${w.active ? `<span class="badge badge-green">Attivo</span>` : `<span class="badge badge-gray">Disattivo</span>`}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-wedit="${w.id}">${icon("edit", 13)}</button>
                <button class="btn btn-sm btn-danger" data-wdel="${w.id}">${icon("trash", 13)}</button>
              </div></td>
            </tr>`).join("") : `<tr class="empty-row"><td colspan="7">Nessun lavoratore — creane uno per registrare le ore con il costo reale</td></tr>`}
        </tbody>
      </table>
      <p style="color:var(--muted);font-size:12.5px;margin-top:10px">Il <b>costo/h</b> è quanto ti costa l'ora del lavoratore (entro il margine), il <b>prezzo/h</b> è quanto lo fatturi al cliente. Le ore registrate nelle commesse usano la tariffa del momento, anche se poi cambi le tariffe.</p>
    </div>`;
  $$(".tabs button").forEach(b => b.onclick = () => { workerFilterActive = parseInt(b.dataset.v); render(); });
  $("#add-worker").onclick = () => workerModal();
  $$("[data-wedit]").forEach(b => b.onclick = () => workerModal(workers.find(x => x.id == b.dataset.wedit)));
  $$("[data-wdel]").forEach(b => b.onclick = () => {
    const w = workers.find(x => x.id == b.dataset.wdel);
    confirmDialog(`Eliminare il lavoratore “${w.name}”? Le ore già registrate restano nei loro costi.`, async () => {
      try { await api("/workers/" + w.id, { method: "DELETE" }); toast("Lavoratore eliminato", "success"); render(); }
      catch (err) { toast(err.message, "error"); }
    });
  });
});

function workerModal(worker = null) {
  const w = worker || {};
  modalForm({
    title: worker ? "Modifica lavoratore" : "Nuovo lavoratore",
    wide: true,
    body: `
      <div class="form-section">Dati principali</div>
      <div class="form-grid">
        ${field("name", "Nome e cognome", { required: true, value: w.name })}
        ${field("employee_code", "Matricola", { value: w.employee_code })}
        ${field("role", "Ruolo", { type: "combo", list: "ruolo_lavoratore", value: w.role, placeholder: "es. Meccanico, Carpentiere, Verniciatore" })}
        ${field("phone", "Telefono", { value: w.phone })}
        ${field("email", "Email", { type: "email", value: w.email })}
        ${field("birth_date", "Data di nascita", { type: "date", value: w.birth_date || "" })}
      </div>
      <div class="form-section">Tariffe</div>
      <div class="form-grid">
        ${field("hourly_cost", "Costo orario (€/h)", { type: "number", step: "any", min: 0, value: w.hourly_cost ?? 0 })}
        ${field("hourly_price", "Prezzo orario di fatturazione (€/h)", { type: "number", step: "any", min: 0, value: w.hourly_price ?? 0 })}
        ${field("active", "Stato", { type: "select", options: `<option value="true" ${w.active !== false ? "selected" : ""}>Attivo</option><option value="false" ${w.active === false ? "selected" : ""}>Disattivo</option>` })}
      </div>
      <div class="form-section">Contratto</div>
      <div class="form-grid">
        ${field("hire_date", "Data assunzione", { type: "date", value: w.hire_date || "" })}
        ${field("contract_type", "Tipo contratto", { value: w.contract_type, placeholder: "CCNL, a tempo indeterminato…" })}
        ${field("weekly_hours", "Ore settimanali", { type: "number", step: "any", min: 0, value: w.weekly_hours ?? "" })}
        ${field("vacation_days", "Giorni ferie annui", { type: "number", step: "any", min: 0, value: w.vacation_days ?? "" })}
        ${field("iban", "IBAN", { value: w.iban, full: true })}
      </div>
      <div class="form-section">Patenti, visite e sicurezza</div>
      <div class="form-grid">
        ${field("license", "Patente", { value: w.license, placeholder: "B, C, nautica, carrello elevatore…" })}
        ${field("license_expiry", "Scadenza patente", { type: "date", value: w.license_expiry || "" })}
        ${field("medical_exam_expiry", "Scadenza visita medica", { type: "date", value: w.medical_exam_expiry || "" })}
        ${field("safety_training_expiry", "Scadenza corso sicurezza", { type: "date", value: w.safety_training_expiry || "" })}
        ${field("skills", "Competenze", { value: w.skills, full: true, placeholder: "es. impiantistica elettrica, vela, gelcoat…" })}
        ${field("certifications", "Certificazioni", { value: w.certifications, full: true, placeholder: "es. abilitazione lavori in quota, GFL…" })}
      </div>
      <div class="form-section">Emergenza e note</div>
      <div class="form-grid">
        ${field("emergency_contact", "Contatto di emergenza", { value: w.emergency_contact })}
        ${field("emergency_phone", "Telefono emergenza", { value: w.emergency_phone })}
        ${field("notes", "Note", { type: "textarea", value: w.notes, full: true })}
      </div>`,
    onSubmit: async fd => {
      const payload = Object.fromEntries(fd.entries());
      payload.hourly_cost = num(payload.hourly_cost);
      payload.hourly_price = num(payload.hourly_price);
      payload.active = payload.active === "true";
      for (const k of ["weekly_hours", "vacation_days"])
        payload[k] = payload[k] === "" ? null : num(payload[k]);
      for (const k of ["birth_date", "hire_date", "license_expiry", "medical_exam_expiry", "safety_training_expiry"])
        payload[k] = payload[k] || null;
      if (worker) await api("/workers/" + worker.id, { method: "PUT", json: payload });
      else await api("/workers", { method: "POST", json: payload });
      closeModal(); toast("Lavoratore salvato", "success"); render();
    },
  });
}

/* ============ Impostazioni ============ */

route(/^\/impostazioni$/, async () => {
  const s = await loadSettings();
  const isAdmin = CURRENT_USER.role === "admin";
  let users = [];
  if (isAdmin) {
    try { users = await api("/users"); } catch { users = []; }
  }
  let backupInfo = null;
  if (isAdmin) {
    try { backupInfo = await api("/admin/backup/info"); } catch { backupInfo = null; }
  }
  let lookupRows = {};
  if (isAdmin) {
    try { lookupRows = await loadLookupsFull(); } catch { lookupRows = {}; }
  }
  const lookupSection = !isAdmin ? "" : `
    <div class="card">
      <h2>${icon("list", 15)} Liste personalizzate</h2>
      <p style="color:var(--muted);font-size:12.5px;margin-top:-4px">Le voci compaiono come suggerimenti nelle form: tipologia cliente, categorie dei lavori, tipi di imbarcazione, materiali, alimentazioni e ruoli. Puoi aggiungere o togliere voci liberamente.</p>
      ${Object.keys({ ...LOOKUP_LABELS, ...lookupRows }).map(cat => {
        const opts = lookupRows[cat] || [];
        return `<div style="border-top:1px solid var(--border);padding:11px 0;display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap">
          <div style="width:190px;font-weight:600;font-size:13px;padding-top:2px">${esc(lookupLabel(cat))}</div>
          <div style="flex:1;display:flex;gap:6px;flex-wrap:wrap;align-items:center;min-width:200px">
            ${opts.length ? opts.map(o => `<span class="badge badge-teal">${esc(o.value)}
              <a href="#" data-ldel="${o.id}" data-lval="${esc(o.value)}" title="Elimina “${esc(o.value)}”" style="color:inherit;font-weight:700;margin-left:2px">×</a></span>`).join("") : `<span style="color:var(--muted);font-size:12.5px">nessuna voce</span>`}
          </div>
          <form class="inline-form" data-lcat="${cat}" style="display:flex;gap:8px;align-items:center">
            <label class="field" style="margin-bottom:0"><input type="text" placeholder="Nuova voce…" required></label>
            <button class="btn btn-sm" type="submit">${icon("plus", 12)} Aggiungi</button>
          </form>
        </div>`;
      }).join("")}
    </div>`;

  $("#view").innerHTML = `
    <div class="page-head">
      <div><h1>${icon("settings")} Impostazioni</h1><div class="sub">Dati azienda, account e backup</div></div>
    </div>

    <div class="card">
      <h2>${icon("file", 15)} Dati azienda (usati su documenti e fattura elettronica)</h2>
      <form id="settings-form">
        <div class="form-grid">
          ${field("company_name", "Ragione sociale", { value: s.company_name, full: true, disabled: !isAdmin })}
          ${field("company_vat", "Partita IVA", { value: s.company_vat, disabled: !isAdmin })}
          ${field("company_tax_code", "Codice fiscale", { value: s.company_tax_code, disabled: !isAdmin })}
          ${field("company_address", "Indirizzo", { value: s.company_address, full: true, disabled: !isAdmin })}
          ${field("company_zip", "CAP", { value: s.company_zip, disabled: !isAdmin })}
          ${field("company_city", "Città", { value: s.company_city, disabled: !isAdmin })}
          ${field("company_province", "Provincia (sigla)", { value: s.company_province, disabled: !isAdmin })}
          ${field("company_regime", "Regime fiscale (codice SdI)", { value: s.company_regime || "RF01", disabled: !isAdmin, placeholder: "RF01 = ordinario" })}
          ${field("default_tax_rate", "IVA predefinita %", { type: "number", step: "any", min: 0, value: s.default_tax_rate ?? 22, disabled: !isAdmin })}
          ${field("default_payment_days", "Scadenza predefinita (giorni)", { type: "number", min: 0, value: s.default_payment_days ?? 30, disabled: !isAdmin })}
          ${field("company_email", "Email", { value: s.company_email, disabled: !isAdmin })}
          ${field("company_phone", "Telefono", { value: s.company_phone, disabled: !isAdmin })}
          ${field("iban", "IBAN (stampato su documenti)", { value: s.iban, full: true, disabled: !isAdmin })}
        </div>
        ${isAdmin ? `<button class="btn btn-primary">${icon("check", 14)} Salva impostazioni</button>` : `<p style="color:var(--muted)">Solo un amministratore può modificare i dati azienda.</p>`}
      </form>
    </div>

    ${lookupSection}

    ${isAdmin ? `
    <div class="card">
      <h2>${icon("users", 15)} Utenti <span class="count">${users.length}</span></h2>
      <table class="tbl">
        <thead><tr><th>Username</th><th>Email</th><th>Ruolo</th><th>Stato</th><th class="num">Azioni</th></tr></thead>
        <tbody>
          ${users.map(u => `
            <tr>
              <td class="primary">${esc(u.username)} ${u.id === CURRENT_USER.id ? '<span class="badge badge-teal">tu</span>' : ""}</td>
              <td>${esc(u.email || "—")}</td>
              <td><span class="badge ${u.role === "admin" ? "badge-red" : u.role === "manager" ? "badge-amber" : "badge-gray"}">${esc(u.role)}</span></td>
              <td>${u.active ? `<span class="badge badge-green">Attivo</span>` : `<span class="badge badge-gray">Disattivo</span>`}</td>
              <td class="num"><div class="actions">
                <button class="btn btn-sm" data-urole="${u.id}">${icon("edit", 13)} Ruolo</button>
                <button class="btn btn-sm" data-upw="${u.id}">Password</button>
                <button class="btn btn-sm btn-danger" data-utoggle="${u.id}">${u.active ? "Disattiva" : "Attiva"}</button>
              </div></td>
            </tr>`).join("")}
        </tbody>
      </table>
      <div style="margin-top:12px"><button class="btn btn-primary btn-sm" id="add-user">${icon("userplus", 13)} Nuovo utente</button></div>
    </div>` : ""}

    <div class="card">
      <h2>${icon("db", 15)} Backup dati</h2>
      <p style="color:var(--muted);margin-bottom:12px">Ogni giorno l'app crea da sola una copia del database (ultime 14 conservate)${backupInfo ? ` nella cartella <code>${esc(backupInfo.folder)}</code>${backupInfo.last ? " — ultima: " + fmtDateTime(backupInfo.last) : ""}` : ""}.<br>Per sicurezza copia ogni tanto la cartella dati anche su un altro disco o su cloud.</p>
      ${isAdmin ? `<button class="btn" id="btn-backup">${icon("download", 14)} Scarica backup del database</button>` : `<p style="color:var(--muted)">Solo gli amministratori possono scaricare il backup.</p>`}
    </div>

    <div class="card">
      <h2>${icon("edit", 15)} Cambia password</h2>
      <form id="pw-form">
        <div class="form-grid">
          ${field("old_password", "Password attuale", { type: "password", required: true })}
          ${field("new_password", "Nuova password (min 8)", { type: "password", required: true })}
        </div>
        <button class="btn btn-primary">Cambia password</button>
      </form>
    </div>`;

  // Liste personalizzate: aggiunta e rimozione voci
  $$("form[data-lcat]").forEach(f => f.onsubmit = async e => {
    e.preventDefault();
    const input = f.querySelector("input");
    try {
      await api("/lookups", { method: "POST", json: { category: f.dataset.lcat, value: input.value.trim() } });
      toast("Voce aggiunta", "success");
      await loadLookups();
      render();
    } catch (err) { toast(err.message, "error"); }
  });
  $$("[data-ldel]").forEach(a => a.onclick = async e => {
    e.preventDefault();
    confirmDialog(`Eliminare la voce “${a.dataset.lval}” dalle tendine? I dati già salvati non vengono modificati.`, async () => {
      try {
        await api("/lookups/" + a.dataset.ldel, { method: "DELETE" });
        toast("Voce eliminata", "success");
        await loadLookups();
        render();
      } catch (err) { toast(err.message, "error"); }
    });
  });

  $("#settings-form").onsubmit = async e => {    e.preventDefault();
    const payload = Object.fromEntries(new FormData(e.target).entries());
    payload.default_tax_rate = num(payload.default_tax_rate);
    payload.default_payment_days = parseInt(payload.default_payment_days) || 0;
    try {
      await api("/settings", { method: "PUT", json: payload });
      await loadSettings();
      toast("Impostazioni salvate", "success");
    } catch (err) { toast(err.message, "error"); }
  };
  $("#pw-form").onsubmit = async e => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
      await api("/auth/change-password", {
        method: "POST",
        json: { old_password: fd.get("old_password"), new_password: fd.get("new_password") },
      });
      toast("Password aggiornata", "success");
      e.target.reset();
      CURRENT_USER.default_password = false;
    } catch (err) { toast(err.message, "error"); }
  };
  if ($("#btn-backup")) $("#btn-backup").onclick = () => downloadFile("/admin/backup", "cantiere_backup.db");

  if (isAdmin) {
    $("#add-user").onclick = () => {
      modalForm({
        title: "Nuovo utente",
        body: `
          <div class="form-grid">
            ${field("username", "Username", { required: true })}
            ${field("password", "Password (min 6)", { type: "password", required: true })}
            ${field("email", "Email", { type: "email" })}
            ${field("role", "Ruolo", { type: "select", options: `<option value="user">Operatore</option><option value="manager">Manager</option><option value="admin">Amministratore</option>` })}
          </div>`,
        onSubmit: async fd => {
          const payload = Object.fromEntries(fd.entries());
          await api("/users", { method: "POST", json: payload });
          closeModal(); toast("Utente creato", "success"); render();
        },
      });
    };
    $$("[data-urole]").forEach(b => b.onclick = () => {
      const u = users.find(x => x.id == b.dataset.urole);
      modalForm({
        title: `Account di ${esc(u.username)}`,
        body: `
          <div class="form-grid">
            ${field("email", "Email", { type: "email", value: u.email })}
            ${field("role", "Ruolo", { type: "select", options: `<option value="user" ${u.role === "user" ? "selected" : ""}>Operatore</option><option value="manager" ${u.role === "manager" ? "selected" : ""}>Manager</option><option value="admin" ${u.role === "admin" ? "selected" : ""}>Amministratore</option>` })}
          </div>`,
        onSubmit: async fd => {
          await api("/users/" + u.id, { method: "PUT", json: { role: fd.get("role"), email: fd.get("email") } });
          closeModal(); toast("Account aggiornato", "success"); render();
        },
      });
    });
    $$("[data-upw]").forEach(b => b.onclick = () => {
      const u = users.find(x => x.id == b.dataset.upw);
      modalForm({
        title: `Nuova password per ${esc(u.username)}`,
        body: field("new_password", "Password (min 6)", { type: "password", required: true }),
        submitLabel: "Imposta",
        onSubmit: async fd => {
          await api(`/users/${u.id}/set-password`, { method: "POST", json: { new_password: fd.get("new_password") } });
          closeModal(); toast("Password impostata", "success");
        },
      });
    });
    $$("[data-utoggle]").forEach(b => b.onclick = () => {
      const u = users.find(x => x.id == b.dataset.utoggle);
      api("/users/" + u.id, { method: "PUT", json: { active: !u.active } })
        .then(() => { toast(u.active ? "Utente disattivato" : "Utente attivato", "success"); render(); })
        .catch(err => toast(err.message, "error"));
    });
  }
});

/* ============ Avvio ============ */

(async function boot() {
  if (TOKEN) {
    try {
      CURRENT_USER = await api("/auth/me");
      await Promise.all([loadSettings(), loadLookups()]);
      showApp();
    } catch {
      doLogout(false);
    }
  }
  if (!CURRENT_USER) $("#login-screen").classList.remove("hidden");
  render();
})();
