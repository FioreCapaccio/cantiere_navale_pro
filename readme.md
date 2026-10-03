# ⚓ Cantiere Navale Pro

Gestionale per cantieri navali: clienti, imbarcazioni, commesse con lavori e allegati,
magazzino multi-sede, documenti (DDT / Proforma / Fattura), fatturazione elettronica
(XML FatturaPA) e stampa documenti.

È un'applicazione web locale: il server parte sul tuo computer e l'interfaccia
si apre nel browser (nessun dato lascia la macchina, salvo configurazione diversa).

---

## AVVIO RAPIDO — macOS (Apple Silicon)

1. Apri la cartella `release/mac` e fai doppio clic su **CantiereNavalePro-macOS.dmg**
2. Trascina **CantiereNavalePro.app** dove vuoi (es. Applicazioni) e aprila
   - *Puoi anche lanciarla direttamente dal DMG: in quel caso i dati vengono
     salvati in `~/Library/Application Support/CantiereNavalePro`. Se invece
     copi l'app su disco Mac (Applicazioni o Desktop), i dati restano accanto
     all'app nella cartella `CantiereNavaleData`: trascina quella insieme
     all'app per spostare anche i dati.*
   - *Se macOS segnala che l'app "non può essere aperta" perché non verificata:
     clic destro sull'app → Apri → Apri (una volta sola), oppure nel Terminale:
     `xattr -cr /Applications/CantiereNavalePro.app`*
3. Il browser si apre da solo su `http://127.0.0.1:8765`
4. Accedi con **admin / admin123** (poi cambiala da Impostazioni)

I dati (database + allegati) sono nella cartella **CantiereNavaleData** accanto
all'app: per il backup basta copiare quella cartella.

## AVVIO RAPIDO — Windows (portabile, senza installazione)

1. Copia su Windows il file `release/windows/CantiereNavalePro-Windows.zip`
   ed estrailo in una cartella qualsiasi
2. Fai doppio clic su **Avvia Cantiere Navale Pro.bat**
   (SmartScreen: "Ulteriori informazioni" → "Esegui comunque")
3. Il browser si apre da solo su `http://127.0.0.1:8765`
4. Accedi con **admin / admin123**

I dati sono nella cartella `data` dentro la cartella del programma.
Il pacchetto include Python: sul PC Windows **non serve installare nulla**.

---

## Funzionalità

- **Dashboard** con statistiche: clienti attivi, imbarcazioni, commesse aperte, fatturato / incassato / da incassare, valore del magazzino, fatture scadute e commesse in scadenza
- **Anagrafiche dettagliate**: scheda cliente completa (codice automatico, tipo, referente, PEC, cellulare, indirizzo strutturato, indirizzo di spedizione per i DDT, IBAN, condizioni di pagamento, sconto abituale, note) con storico imbarcazioni / commesse / documenti e totali per cliente
- **Scheda imbarcazione** estesa: tipo, lunghezza, anno di costruzione, numero di scafo (HIN), motore, **scadenza assicurazione con avviso automatico**, storico commesse e documenti
- **Commesse** numerate automaticamente (COMM-ANNO-NNNNN) con stato, scadenze, **lavori** (categoria, quantità, costo/prezzo, margine, assegnatario) e **allegati** (foto, PDF…)
- **Magazzino** multi-sede con magazzini modificabili: articoli, giacenze, movimenti di carico/scarico/reso correggibili o eliminabili con ricalcolo automatico delle giacenze (mai sotto zero)
- **Documenti**: DDT (con dati trasporto e indirizzo di spedizione del cliente), Proforma e Fattura con righe modificabili, sconti (anche sconto abituale del cliente precompilato), IVA, pagamenti, conversione Proforma/DDT → Fattura, **archiviazione** dei documenti. Intestazione e righe sono correggibili dopo la creazione (sui documenti già pagati restano modificabili solo note e scadenza)
- **Scadenzario**: fatture non saldate ordinate per scadenza, giorni di ritardo e registrazione rapida dei pagamenti
- **Acquisti**: anagrafica fornitori, fatture di acquisto (con stato da pagare/pagata), **ordini di acquisto** con righe e **ricezione in magazzino** che genera automaticamente i carichi, **registro IVA** (IVA a debito/credito e saldo annuale) con export CSV
- **Agenda scalo**: postazioni (viaggi, botteghe, seul, moli) con **calendario mensile**, prenotazioni collegate a imbarcazione e commessa, controllo sovrapposizioni e promemoria in dashboard
- **Timesheet**: ore lavorative per persona e per commessa, confronto con le ore preventivate dei lavori
- **Scorte**: scorta minima per articolo con **alert automatico** in dashboard e nell'elenco articoli quando la giacenza scende sotto
- **Archivio documentale**: cartelle (Contratti, Certificati, Assicurazioni, Pratiche…) rinominabili, per conservare qualsiasi file con note, ricerca e download
- **Fattura elettronica**: generazione XML FatturaPA (FPR12) per le fatture
- **Ricerca globale** nella barra superiore: clienti, imbarcazioni, commesse e documenti in un solo campo
- **Gestione utenti** (ruoli admin / manager / operatore) e **backup del database** scaricabile dall'app
- **Export CSV** di clienti e documenti, **stampa** di ogni documento (anche in PDF dal browser) con i dati azienda
- **API REST** complete su `http://127.0.0.1:8765/docs` (Swagger UI)
- **Migrazione automatica del database**: aggiornando l'app, i dati esistenti vengono estesi senza perdite

## Novità della versione 2.2

- **Calcoli a prova di centesimo**: tutti gli importi usano l'aritmetica decimale con arrotondamento
  commerciale riga per riga (stesse regole della fattura elettronica); sconto in % (preso dalla scheda
  cliente) e in euro, mai superiore al subtotale; pagamenti che non possono superare il residuo.
- **Numerazione sicura**: i progressivi (fatture, DDT, commesse, ordini) ripartono dal massimo esistente,
  quindi eliminare un documento non crea più duplicati.
- **Fattura elettronica completa**: riepilogo IVA, dati di pagamento, natura IVA per le operazioni
  a aliquota 0 (es. N3.4 per la nautica), codice destinatario SdI/PEC, controllo della partita IVA.
- **Redditività della commessa** calcolata dal server: ricavi, costi (ore registrate, materiali scaricati,
  subappalti), margine, importo ancora da fatturare.
- **Magazzino**: costo medio ponderato aggiornato a ogni carico e alla ricezione degli ordini d'acquisto.
- **Meno passaggi**: dalla commessa, un clic crea Proforma / Fattura / DDT (con IVA, sconto cliente e
  scadenza già impostati); il registro IVA mostra il riepilogo per aliquota.
- **Sicurezza e affidabilità**: blocco dopo 5 password errate, password minime di 8 caratteri,
  eliminazioni riservate a manager e amministratori, backup automatico giornaliero (ultimi 14) in
  `backups/`, limite di 100 MB sui file caricati, allegati ritrovati anche se sposti la cartella dati.

## Archivio e temi

- **Archivio**: ogni file ha una casella di selezione (più "seleziona tutti"): si possono eliminare solo
  i file scelti con un clic. Una cartella con file si elimina insieme al contenuto, dopo conferma.
  Le cancellazioni sono riservate a manager e amministratori.
- **Temi**: dal selettore in alto a destra si passa tra **Chiaro**, **Scuro** e **Blu marine**;
  la scelta resta memorizzata nel browser.

## Test

```bash
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest tests
```

I test usano un database temporaneo e coprono totali, arrotondamenti, pagamenti, numerazione, XML,
magazzino, redditività commessa, registro IVA e permessi.

## Accesso da altri dispositivi (opzionale)

Di default il server risponde solo sul computer locale. Per usarlo anche da
telefono/tablet in rete locale:

1. Nella cartella dati (o accanto a `main.py` in sviluppo) crea un file `.env` con:
   ```
   HOST=0.0.0.0
   ```
2. Riavvia l'app e apri il firewall sulla porta 8765
3. Da altri dispositivi: `http://<IP-del-computer>:8765`

## Configurazione (file `.env`, tutti i valori sono opzionali)

| Variabile        | Default                    | Descrizione                                  |
|------------------|----------------------------|----------------------------------------------|
| `HOST`           | `127.0.0.1`                | Indirizzo di ascolto (`0.0.0.0` = rete)      |
| `PORT`           | `8765`                     | Porta web                                    |
| `ADMIN_USERNAME` | `admin`                    | Utente amministratore creato al primo avvio  |
| `ADMIN_PASSWORD` | `admin123`                 | Password iniziale (cambiala dopo!)           |
| `OPEN_BROWSER`   | `1` nell'app pacchettizzata| Apre il browser all'avvio                    |
| `SECRET_KEY`     | generata e salvata nei dati| Chiave firma dei token di sessione           |

I dati azienda e gli altri utenti si gestiscono direttamente dall'app, pagina **Impostazioni**.

## Sviluppo (da sorgenti)

Serve Python 3.12+:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py          # server su http://127.0.0.1:8765
```

In sviluppo il database è in `data/shipyard.db` e gli allegati in `data/uploads/`.

### Ricreare i pacchetti standalone

- **Su GitHub (consigliato)**: scheda *Actions* → *Build* → *Run workflow*. A build
  finita i file sono scaricabili dalla pagina della run nella sezione *Artifacts*:
  DMG macOS, ZIP Windows portabile e **CantiereNavalePro-Setup.exe** (installazione
  classica con Avanti/Avanti/Fine, collegamenti e disinstallazione). Su un **tag**
  `v…` (es. `v2.1`) i tre file vengono inoltre allegati a una *Release* pronta da
  condividere; la versione del setup la prende dal numero del tag.
- **macOS in locale**: `./build_mac.sh` → produce `CantiereNavalePro.app` (serve una
  Mac arm64; PyInstaller non cross-compila)
- **Windows in locale**: `./build_windows.sh` → produce `CantiereNavalePro-Windows/`
  con Python embedded, avviabile su qualsiasi PC Windows 64 bit senza installazioni

## Struttura del progetto

```
main.py                 Server FastAPI + API + modello dati
tests/                  Test automatici (pytest)
static/                 Interfaccia web (HTML/CSS/JS, nessuna dipendenza)
data/                   Database SQLite e allegati (creata al primo avvio)
legacy/                 Precedente versione Flask (non più mantenuta)
release/mac             DMG pronta per macOS Apple Silicon
release/windows         ZIP portabile pronto per Windows
build_mac.sh            Build app macOS (PyInstaller)
build_windows.sh        Build pacchetto Windows (Python embeddable)
make_icon.py            Genera l'icona dell'app
requirements.txt        Dipendenze Python
```

## Note

- Password predefinita **admin/admin123**: cambiala al primo accesso (Impostazioni → Cambia password).
- Le fatture XML usano il codice destinatario `0000000` (fornitori esteri/pubblica amm.
  richiedono configurazioni dedicate) e vanno firmate/inviate con il propriogestionale SdI.
- Backup: copia la cartella dati (`CantiereNavaleData` su Mac, `data` su Windows).
