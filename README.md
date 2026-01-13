# Financial ## ✨ Features

- 🖥️ **Moderne GUI**: Benutzerfreundliche PyQt6-Oberfläche
- 🗄️ **Datenbank-Auswahl**: Wähle beim Start eine vorhandene DB oder erstelle eine neue
- 🔄 **Datenbank wechseln**: Wechsle während der Laufzeit zwischen verschiedenen Datenbanken
- 📂 **Multi-File-Import**: Importiere mehrere Excel-Dateien gleichzeitig
- 📊 **Live-Statistiken**: Zeigt Einnahmen, Ausgaben und Saldo in Echtzeit
- 💾 **Datenbankinfo**: Zeigt aktuellen Pfad, Größe und Status der Datenbank
- 🗄️ **SQLite-Datenbank**: Lokale Speicherung aller Transaktionen
- 🔢 **Duplikat-Prüfung**: Verhindert mehrfaches Einfügen derselben Transaktion
- 📅 **Monatliche Verarbeitung**: Verarbeitet Sheets 01-12 automatisch
- 🏷️ **Kategorien**: Unterstützung für Transaktionskategorien
- ⚡ **Background-Import**: Import läuft im Hintergrund ohne UI-Freeze
- 📋 **Import-Log**: Detaillierte Protokollierung des Import-Vorgangss TCG

Ein Python-Tool mit GUI zur Verwaltung und Import von finanziellen Transaktionen aus Excel-Dateien in eine SQLite-Datenbank.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6%2B-green)

## 📋 Beschreibung

Dieses Tool ermöglicht den Import von Transaktionsdaten aus Excel-Dateien (z.B. monatliche Kassabücher) in eine SQLite-Datenbank über eine benutzerfreundliche grafische Oberfläche. Es verarbeitet automatisch mehrere Sheets (01-12 für die Monate) und verhindert Duplikate durch ID-Prüfung.

## ✨ Features

- �️ **Moderne GUI**: Benutzerfreundliche PyQt6-Oberfläche
- 📂 **Multi-File-Import**: Importiere mehrere Excel-Dateien gleichzeitig
- 📊 **Live-Statistiken**: Zeigt Einnahmen, Ausgaben und Saldo in Echtzeit
- 🗄️ **SQLite-Datenbank**: Lokale Speicherung aller Transaktionen
- 🔢 **Duplikat-Prüfung**: Verhindert mehrfaches Einfügen derselben Transaktion
- 📅 **Monatliche Verarbeitung**: Verarbeitet Sheets 01-12 automatisch
- 🏷️ **Kategorien**: Unterstützung für Transaktionskategorien
- ⚡ **Background-Import**: Import läuft im Hintergrund ohne UI-Freeze
- 📋 **Import-Log**: Detaillierte Protokollierung des Import-Vorgangs

## 🗂️ Datenbankstruktur

### Tabelle: transactions
- `id` (NUMBER, Primary Key) - Eindeutige Transaktions-ID
- `date` (DATE) - Datum der Transaktion
- `description` (TEXT) - Beschreibung der Transaktion
- `category` (TEXT) - Kategorie (Foreign Key zu categories)
- `income` (REAL) - Einnahmen
- `expense` (REAL) - Ausgaben

### Tabelle: categories
- `categoryid` (TEXT, Primary Key) - Eindeutige Kategorie-ID
- `label` (TEXT) - Bezeichnung der Kategorie

## 🚀 Installation

### Voraussetzungen
- Python 3.9 oder höher
- PyQt6
- openpyxl

### Virtuelle Umgebung erstellen (empfohlen)

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

## 💻 Verwendung

### GUI-Version (empfohlen)
```bash
python main.py
```

**Beim Start:**
1. Ein Dialog öffnet sich zur Datenbankauswahl
2. Wähle eine vorhandene `.db` Datei ODER
3. Gib einen neuen Dateinamen ein, um eine neue Datenbank zu erstellen
4. Die Anwendung öffnet sich mit der gewählten Datenbank

**Datenbank wechseln während der Laufzeit:**
- Menü: `Datei → Datenbank wechseln...`
- Wähle eine andere Datenbank aus oder erstelle eine neue

**Excel-Dateien importieren:**
1. Klicke auf "📂 Excel-Dateien auswählen und importieren"
2. Wähle eine oder mehrere Excel-Dateien aus
3. Der Import läuft automatisch im Hintergrund
4. Statistiken und Log werden live aktualisiert

### Alte Kommandozeilen-Version
```bash
python transactions_old.py
```

## 📦 Vorkompilierte Downloads

Für Windows und macOS stehen vorkompilierte ausführbare Dateien zur Verfügung:

👉 [Releases herunterladen](https://github.com/klauskirnbauerHTL/financial_transactions_tcg/releases)

- **macOS**: `.zip` mit `.app` Bundle
- **Windows**: `.exe` Datei

### ⚠️ macOS Sicherheitshinweis

Da die App nicht von Apple signiert ist, müssen Sie beim ersten Start:

**Rechtsklick → Öffnen → Im Dialog "Öffnen" bestätigen**

Oder im Terminal:
```bash
xattr -cr FinancialTransactionsTCG.app
open FinancialTransactionsTCG.app
```

### Excel-Format

Die Excel-Datei sollte folgende Struktur haben:
- Sheets benannt als "01", "02", ..., "12" (für jeden Monat)
- Daten beginnen ab Zeile 7
- Spalten A-F enthalten:
  - A: ID (Nummer)
  - B: Datum
  - C: Beschreibung
  - D: Kategorie
  - E: Einnahmen
  - F: Ausgaben

## 📝 Hinweise

- Die Datenbank `transactions.db` wird automatisch erstellt
- Bereits importierte Transaktionen (anhand ID) werden übersprungen
- Kategorien müssen in der `categories`-Tabelle vorhanden sein

## 🔧 Entwicklung

### Projekt-Struktur
```
financial_transactions_tcg/
├── main.py                  # Haupteinstiegspunkt (GUI)
├── main_window.py           # PyQt6 Hauptfenster
├── database.py              # Datenbank-Manager
├── excel_importer.py        # Excel-Import-Logik
├── transactions_old.py      # Alte CLI-Version (Legacy)
├── transactions.db          # SQLite-Datenbank (generiert)
├── requirements.txt         # Python-Abhängigkeiten
├── build.spec              # PyInstaller-Konfiguration
├── .github/workflows/       # CI/CD Pipeline
└── README.md               # Diese Datei
```

### Eigene Builds erstellen

#### Mit PyInstaller
```bash
pip install pyinstaller
pyinstaller build.spec
```

Die ausführbare Datei findet sich dann in `dist/`.

#### macOS App Bundle
```bash
pyinstaller build.spec
# Ausgabe: dist/FinancialTransactionsTCG.app
```

#### Windows Executable
```bash
pyinstaller build.spec
# Ausgabe: dist/FinancialTransactionsTCG.exe
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'PyQt6'"
```bash
pip install PyQt6
```

### "ModuleNotFoundError: No module named 'openpyxl'"
```bash
pip install openpyxl
```

### Virtuelle Umgebung nicht gefunden
Stelle sicher, dass die virtuelle Umgebung aktiviert ist:
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Datenbank zurücksetzen
Falls du die Datenbank neu erstellen möchtest:
```bash
rm transactions.db
python main.py
```

### Windows: "Kein gültiges Win32-Programm"
Stelle sicher, dass du die richtige Python-Version (64-bit) verwendest.

## 📄 Lizenz

Dieses Projekt ist für den internen Gebrauch an der HTL Pinkafeld.

## 👨‍💻 Autor

**Klaus Kirnbauer**  
HTL Pinkafeld

---

**Erstellt**: 2025
