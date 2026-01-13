# Financial Transactions TCG

Ein Python-Tool zur Verwaltung und Import von finanziellen Transaktionen aus Excel-Dateien in eine SQLite-Datenbank.

## 📋 Beschreibung

Dieses Tool ermöglicht den Import von Transaktionsdaten aus Excel-Dateien (z.B. monatliche Kassabücher) in eine SQLite-Datenbank. Es verarbeitet automatisch mehrere Sheets (01-12 für die Monate) und verhindert Duplikate durch ID-Prüfung.

## ✨ Features

- 📊 **Excel-Import**: Automatischer Import aus Excel-Dateien
- 🗄️ **SQLite-Datenbank**: Lokale Speicherung aller Transaktionen
- 🔢 **Duplikat-Prüfung**: Verhindert mehrfaches Einfügen derselben Transaktion
- 📅 **Monatliche Verarbeitung**: Verarbeitet Sheets 01-12 automatisch
- 🏷️ **Kategorien**: Unterstützung für Transaktionskategorien

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
- Python 3.x
- openpyxl

### Abhängigkeiten installieren
```bash
pip install openpyxl
```

## 💻 Verwendung

```bash
python transactions.py
```

Das Programm fragt nach dem Pfad zur Excel-Datei:
```
Bitte den Pfad zur Excel-Datei angeben: /pfad/zur/datei.xlsx
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
├── transactions.py      # Hauptskript
├── transactions.db      # SQLite-Datenbank (generiert)
├── .gitignore          # Git-Ignore Regeln
└── README.md           # Diese Datei
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'openpyxl'"
```bash
pip install openpyxl
```

### Datenbank zurücksetzen
Falls du die Datenbank neu erstellen möchtest:
```bash
rm transactions.db
python transactions.py
```

## 📄 Lizenz

Dieses Projekt ist für den internen Gebrauch an der HTL Pinkafeld.

## 👨‍💻 Autor

**Klaus Kirnbauer**  
HTL Pinkafeld

---

**Erstellt**: 2025
