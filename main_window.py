"""
Main Window for Financial Transactions TCG
PyQt6 GUI for importing Excel files and viewing statistics
"""
import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem,
    QGroupBox, QProgressBar, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from database import DatabaseManager
from excel_importer import ExcelImporter


class ImportThread(QThread):
    """Background thread for importing Excel files"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(int, int, int)
    
    def __init__(self, db_path, file_paths):
        super().__init__()
        self.db_path = db_path
        self.file_paths = file_paths
    
    def run(self):
        """Import all selected files"""
        total_imported = 0
        total_skipped = 0
        total_errors = 0
        
        # Create a NEW database manager in this thread (thread-safe)
        db_manager = DatabaseManager(self.db_path)
        
        # Create importer with progress callback
        importer = ExcelImporter(db_manager, progress_callback=lambda msg: self.progress.emit(msg))
        
        for i, file_path in enumerate(self.file_paths, 1):
            file_name = os.path.basename(file_path)
            self.progress.emit(f"Importiere {i}/{len(self.file_paths)}: {file_name}...")
            
            imported, skipped, errors = importer.import_file(file_path)
            total_imported += imported
            total_skipped += skipped
            total_errors += errors
        
        # Close the database connection
        db_manager.close()
        
        self.finished.emit(total_imported, total_skipped, total_errors)


class MainWindow(QMainWindow):
    def __init__(self, db_path="transactions.db"):
        super().__init__()
        self.db_path = db_path
        self.db_manager = DatabaseManager(db_path)
        self.import_thread = None
        self.init_ui()
        self.update_statistics()
        self.show_database_info()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Financial Transactions TCG - Import Tool")
        self.setMinimumSize(900, 700)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("💰 Financial Transactions Import Tool")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create Menu Bar
        self.create_menu()
        
        # Database Info Label
        self.db_info_label = QLabel()
        self.db_info_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #666;
                padding: 5px;
                background-color: #f8f8f8;
                border-radius: 3px;
            }
        """)
        self.db_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.db_info_label)
        
        # Statistics Group
        stats_group = self._create_statistics_group()
        main_layout.addWidget(stats_group)
        
        # Import Group
        import_group = self._create_import_group()
        main_layout.addWidget(import_group)
        
        # Log Group
        log_group = self._create_log_group()
        main_layout.addWidget(log_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Aktualisieren")
        self.refresh_btn.setMinimumHeight(40)
        self.refresh_btn.clicked.connect(self.update_statistics)
        
        self.view_data_btn = QPushButton("📊 Daten anzeigen")
        self.view_data_btn.setMinimumHeight(40)
        self.view_data_btn.clicked.connect(self.show_data_viewer)
        
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.view_data_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
    
    def create_menu(self):
        """Create menu bar with database and file options"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("📁 Datei")
        
        # Switch Database Action
        switch_db_action = file_menu.addAction("🔄 Datenbank wechseln...")
        switch_db_action.triggered.connect(self.switch_database)
        
        file_menu.addSeparator()
        
        # Exit Action
        exit_action = file_menu.addAction("❌ Beenden")
        exit_action.triggered.connect(self.close)
        
        # Help Menu
        help_menu = menubar.addMenu("❓ Hilfe")
        
        about_action = help_menu.addAction("ℹ️ Über")
        about_action.triggered.connect(self.show_about)
    
    def _create_statistics_group(self):
        """Create statistics display group"""
        group = QGroupBox("📈 Statistiken")
        layout = QVBoxLayout()
        
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                padding: 15px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.stats_label)
        
        group.setLayout(layout)
        return group
    
    def _create_import_group(self):
        """Create import controls group"""
        group = QGroupBox("📥 Excel-Dateien importieren")
        layout = QVBoxLayout()
        
        # Instructions
        info_label = QLabel(
            "Wähle eine oder mehrere Excel-Dateien zum Importieren aus.\n"
            "Die Dateien sollten Sheets mit Namen '01' bis '12' für Monate enthalten."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Import Button
        self.import_btn = QPushButton("📂 Excel-Dateien auswählen und importieren")
        self.import_btn.setMinimumHeight(50)
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.import_btn.clicked.connect(self.select_and_import_files)
        layout.addWidget(self.import_btn)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status Label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        group.setLayout(layout)
        return group
    
    def _create_log_group(self):
        """Create log display group"""
        group = QGroupBox("📋 Import-Log")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)
        
        group.setLayout(layout)
        return group
    
    def update_statistics(self):
        """Update statistics display"""
        stats = self.db_manager.get_statistics()
        
        stats_text = f"""
        <b>Anzahl Transaktionen:</b> {stats['total_transactions']}<br>
        <b>Gesamteinnahmen:</b> €{stats['total_income']:,.2f}<br>
        <b>Gesamtausgaben:</b> €{stats['total_expenses']:,.2f}<br>
        <b>Saldo:</b> <span style='color: {"green" if stats["balance"] >= 0 else "red"}'>
        €{stats['balance']:,.2f}</span>
        """
        
        self.stats_label.setText(stats_text)
    
    def show_database_info(self):
        """Display current database path and size"""
        if os.path.exists(self.db_path):
            file_size = os.path.getsize(self.db_path)
            size_kb = file_size / 1024
            size_text = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
            status = "✅ Vorhanden"
        else:
            size_text = "Neu"
            status = "🆕 Wird erstellt"
        
        db_name = os.path.basename(self.db_path)
        db_dir = os.path.dirname(self.db_path) or "Aktuelles Verzeichnis"
        
        info_text = f"📁 Datenbank: <b>{db_name}</b> | 📍 {db_dir} | {status} | 💾 {size_text}"
        self.db_info_label.setText(info_text)
    
    def select_and_import_files(self):
        """Select Excel files and start import"""
        # Show current database status before import
        current_count = self.db_manager.get_transaction_count()
        
        reply = QMessageBox.question(
            self,
            "Import starten",
            f"Aktuelle Datenbank: {os.path.basename(self.db_path)}\n"
            f"Vorhandene Transaktionen: {current_count}\n\n"
            f"Excel-Dateien zum Importieren auswählen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Excel-Dateien auswählen",
            "",
            "Excel Dateien (*.xlsx *.xls);;Alle Dateien (*.*)"
        )
        
        if not file_paths:
            return
        
        self.start_import(file_paths)
    
    def start_import(self, file_paths):
        """Start import process in background thread"""
        self.import_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.log_text.clear()
        
        self.log_text.append(f"Starte Import von {len(file_paths)} Datei(en)...\n")
        
        # Create and start import thread (pass db_path instead of db_manager for thread safety)
        self.import_thread = ImportThread(self.db_path, file_paths)
        self.import_thread.progress.connect(self.on_import_progress)
        self.import_thread.finished.connect(self.on_import_finished)
        self.import_thread.start()
    
    def on_import_progress(self, message):
        """Handle progress updates from import thread"""
        self.log_text.append(message)
        self.status_label.setText(message)
        # Auto-scroll to bottom
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def on_import_finished(self, imported, skipped, errors):
        """Handle import completion"""
        self.progress_bar.setVisible(False)
        self.import_btn.setEnabled(True)
        
        # Update statistics and database info
        self.update_statistics()
        self.show_database_info()
        
        # Get current transaction count
        total_transactions = self.db_manager.get_transaction_count()
        
        # Show results
        result_msg = f"""
Import abgeschlossen!

✅ Neu importiert: {imported}
⏭️ Übersprungen (bereits vorhanden): {skipped}
❌ Fehler: {errors}

📊 Gesamt in Datenbank: {total_transactions} Transaktionen
        """
        
        self.log_text.append("\n" + result_msg)
        self.status_label.setText("Import abgeschlossen!")
        
        # Show detailed message box
        if errors > 0:
            QMessageBox.warning(self, "Import mit Fehlern", result_msg)
        else:
            # Show success with option to view data
            reply = QMessageBox.information(
                self, 
                "Import erfolgreich", 
                result_msg + "\n\nMöchten Sie die Transaktionen anzeigen?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.show_data_viewer()
    
    def show_data_viewer(self):
        """Show data viewer window"""
        transactions = self.db_manager.get_all_transactions()
        
        if not transactions:
            QMessageBox.information(
                self, 
                "Daten anzeigen", 
                "Die Datenbank enthält keine Transaktionen."
            )
            return
        
        # Create a simple text display of transactions
        msg = f"Datenbank: {os.path.basename(self.db_path)}\n"
        msg += f"Anzahl Transaktionen: {len(transactions)}\n"
        msg += "="*60 + "\n\n"
        
        # Show first 10 transactions
        for i, trans in enumerate(transactions[:10], 1):
            trans_id, date, desc, cat, income, expense = trans
            msg += f"{i}. ID={trans_id} | {date} | {desc[:30]}\n"
            msg += f"   Kategorie: {cat} | E: €{income:.2f} | A: €{expense:.2f}\n\n"
        
        if len(transactions) > 10:
            msg += f"\n... und {len(transactions) - 10} weitere Transaktionen"
        
        # Create scrollable message box
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Transaktionen in Datenbank")
        dialog.setText(msg)
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        dialog.exec()
    
    def switch_database(self):
        """Allow user to switch to a different database"""
        dialog = QFileDialog()
        dialog.setWindowTitle("Datenbank wechseln")
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setNameFilter("SQLite Datenbank (*.db);;Alle Dateien (*.*)")
        dialog.setDefaultSuffix("db")
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setDirectory(os.path.dirname(self.db_path) or os.getcwd())
        
        if dialog.exec():
            selected_files = dialog.selectedFiles()
            if selected_files:
                new_db_path = selected_files[0]
                
                # Ask for confirmation if current database has unsaved changes
                reply = QMessageBox.question(
                    self,
                    "Datenbank wechseln",
                    f"Möchten Sie zur Datenbank wechseln:\n{new_db_path}",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Close current database
                    self.db_manager.close()
                    
                    # Open new database
                    self.db_path = new_db_path
                    self.db_manager = DatabaseManager(new_db_path)
                    
                    # Update UI
                    self.update_statistics()
                    self.show_database_info()
                    self.log_text.clear()
                    self.log_text.append(f"✅ Datenbank gewechselt zu:\n{new_db_path}\n")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>Financial Transactions TCG</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Autor:</b> Klaus Kirnbauer</p>
        <p><b>Organisation:</b> HTL Pinkafeld</p>
        <hr>
        <p>Import-Tool für Excel-basierte Transaktionsdaten</p>
        <p>
        <b>Features:</b><br>
        • Multi-File Excel-Import<br>
        • Live-Statistiken<br>
        • SQLite-Datenbank<br>
        • Duplikat-Prüfung<br>
        • Datenbank-Verwaltung
        </p>
        """
        QMessageBox.about(self, "Über Financial Transactions TCG", about_text)
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.db_manager.close()
        event.accept()
