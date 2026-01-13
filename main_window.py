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
    
    def __init__(self, db_manager, file_paths):
        super().__init__()
        self.db_manager = db_manager
        self.file_paths = file_paths
    
    def run(self):
        """Import all selected files"""
        total_imported = 0
        total_skipped = 0
        total_errors = 0
        
        importer = ExcelImporter(self.db_manager)
        
        for i, file_path in enumerate(self.file_paths, 1):
            file_name = os.path.basename(file_path)
            self.progress.emit(f"Importiere {i}/{len(self.file_paths)}: {file_name}...")
            
            imported, skipped, errors = importer.import_file(file_path)
            total_imported += imported
            total_skipped += skipped
            total_errors += errors
        
        self.finished.emit(total_imported, total_skipped, total_errors)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.import_thread = None
        self.init_ui()
        self.update_statistics()
    
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
    
    def select_and_import_files(self):
        """Select Excel files and start import"""
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
        
        # Create and start import thread
        self.import_thread = ImportThread(self.db_manager, file_paths)
        self.import_thread.progress.connect(self.on_import_progress)
        self.import_thread.finished.connect(self.on_import_finished)
        self.import_thread.start()
    
    def on_import_progress(self, message):
        """Handle progress updates from import thread"""
        self.log_text.append(message)
        self.status_label.setText(message)
    
    def on_import_finished(self, imported, skipped, errors):
        """Handle import completion"""
        self.progress_bar.setVisible(False)
        self.import_btn.setEnabled(True)
        
        # Update statistics
        self.update_statistics()
        
        # Show results
        result_msg = f"""
Import abgeschlossen!

✅ Neu importiert: {imported}
⏭️ Übersprungen (bereits vorhanden): {skipped}
❌ Fehler: {errors}
        """
        
        self.log_text.append("\n" + result_msg)
        self.status_label.setText("Import abgeschlossen!")
        
        # Show message box
        if errors > 0:
            QMessageBox.warning(self, "Import mit Fehlern", result_msg)
        else:
            QMessageBox.information(self, "Import erfolgreich", result_msg)
    
    def show_data_viewer(self):
        """Show data viewer window (placeholder for future implementation)"""
        transactions = self.db_manager.get_all_transactions()
        
        msg = f"Datenbank enthält {len(transactions)} Transaktionen.\n\n"
        msg += "Ein Daten-Viewer ist in einer zukünftigen Version geplant."
        
        QMessageBox.information(self, "Daten anzeigen", msg)
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.db_manager.close()
        event.accept()
