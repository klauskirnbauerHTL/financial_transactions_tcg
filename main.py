"""
Financial Transactions TCG - Main Entry Point
Import tool for Excel-based transaction data
"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from main_window import MainWindow


def select_database():
    """Let user select or create a database file at startup"""
    dialog = QFileDialog()
    dialog.setWindowTitle("Datenbank wählen oder erstellen")
    dialog.setFileMode(QFileDialog.FileMode.AnyFile)
    dialog.setNameFilter("SQLite Datenbank (*.db);;Alle Dateien (*.*)")
    dialog.setDefaultSuffix("db")
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    
    # Set default directory to current directory
    dialog.setDirectory(os.getcwd())
    
    if dialog.exec():
        selected_files = dialog.selectedFiles()
        if selected_files:
            return selected_files[0]
    
    return None


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Financial Transactions TCG")
    app.setOrganizationName("HTL Pinkafeld")
    
    # Let user select database file
    db_path = select_database()
    
    if not db_path:
        # User cancelled - show message and exit
        QMessageBox.warning(
            None, 
            "Keine Datenbank gewählt", 
            "Es wurde keine Datenbank ausgewählt. Das Programm wird beendet."
        )
        sys.exit(0)
    
    # Create and show main window with selected database
    window = MainWindow(db_path=db_path)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
