"""
Financial Transactions TCG - Main Entry Point
Import tool for Excel-based transaction data
"""
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Financial Transactions TCG")
    app.setOrganizationName("HTL Pinkafeld")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
