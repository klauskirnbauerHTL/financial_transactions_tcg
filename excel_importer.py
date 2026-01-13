"""
Excel Importer module for Financial Transactions TCG
Handles importing data from Excel files
"""
import openpyxl
from typing import Tuple, List
from database import DatabaseManager


class ExcelImporter:
    def __init__(self, db_manager: DatabaseManager):
        """Initialize Excel Importer with database manager"""
        self.db = db_manager
        self.imported_count = 0
        self.skipped_count = 0
        self.error_count = 0
    
    def import_file(self, file_path: str) -> Tuple[int, int, int]:
        """
        Import transactions and categories from Excel file
        Returns: (imported_count, skipped_count, error_count)
        """
        self.imported_count = 0
        self.skipped_count = 0
        self.error_count = 0
        
        try:
            wb = openpyxl.load_workbook(file_path)
            
            # Import transactions from monthly sheets (01-12)
            self._import_transactions(wb)
            
            # Import categories if "Kategorien" sheet exists
            self._import_categories(wb)
            
            wb.close()
            
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            self.error_count += 1
        
        return (self.imported_count, self.skipped_count, self.error_count)
    
    def _import_transactions(self, workbook):
        """Import transactions from monthly sheets (01-12)"""
        for month_num in range(1, 13):
            sheet_name = f"{month_num:02d}"
            
            if sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                
                for row in sheet.iter_rows(min_row=7, values_only=True):
                    # Skip rows without ID in first column
                    if not isinstance(row[0], (int, float)):
                        continue
                    
                    try:
                        trans_id = int(row[0])
                        date = row[1] if len(row) > 1 else None
                        description = row[2] if len(row) > 2 else ""
                        category = row[3] if len(row) > 3 else ""
                        income = float(row[4]) if len(row) > 4 and row[4] else 0.0
                        expense = float(row[5]) if len(row) > 5 and row[5] else 0.0
                        
                        if self.db.insert_transaction(trans_id, date, description, 
                                                     category, income, expense):
                            self.imported_count += 1
                        else:
                            self.skipped_count += 1
                            
                    except Exception as e:
                        print(f"Error importing row: {e}")
                        self.error_count += 1
    
    def _import_categories(self, workbook):
        """Import categories from 'Kategorien' sheet"""
        if "Kategorien" not in workbook.sheetnames:
            return
        
        sheet = workbook["Kategorien"]
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Skip rows without valid data in first two columns
            if not (row[0] and row[1]):
                continue
            
            try:
                category_id = str(row[0])
                label = str(row[1])
                self.db.insert_category(category_id, label)
            except Exception as e:
                print(f"Error importing category: {e}")
