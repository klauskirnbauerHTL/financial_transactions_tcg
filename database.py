"""
Database module for Financial Transactions TCG
Handles all database operations for transactions and categories
"""
import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional


class DatabaseManager:
    def __init__(self, db_path: str = "transactions.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create transactions and categories tables if they don't exist"""
        # Tabelle transactions erstellen
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            date DATE,
            description TEXT,
            category TEXT,
            income REAL,
            expense REAL,
            FOREIGN KEY (category) REFERENCES categories(categoryid)
        )
        ''')
        
        # Tabelle categories erstellen
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            categoryid TEXT PRIMARY KEY,
            label TEXT
        )
        ''')
        self.conn.commit()
    
    def transaction_exists(self, transaction_id: int) -> bool:
        """Check if a transaction with the given ID already exists"""
        self.cursor.execute('SELECT COUNT(*) FROM transactions WHERE id = ?', (transaction_id,))
        return self.cursor.fetchone()[0] > 0
    
    def insert_transaction(self, trans_id: int, date, description: str, 
                          category: str, income: float, expense: float) -> bool:
        """Insert a new transaction, returns True if successful"""
        try:
            if not self.transaction_exists(trans_id):
                self.cursor.execute('''
                INSERT INTO transactions (id, date, description, category, income, expense)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (trans_id, date, description, category, income, expense))
                self.conn.commit()
                return True
            return False
        except Exception as e:
            print(f"Error inserting transaction {trans_id}: {e}")
            return False
    
    def insert_category(self, category_id: str, label: str) -> bool:
        """Insert or update a category"""
        try:
            self.cursor.execute('''
            INSERT OR IGNORE INTO categories (categoryid, label)
            VALUES (?, ?)
            ''', (category_id, label))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting category {category_id}: {e}")
            return False
    
    def get_all_transactions(self) -> List[Tuple]:
        """Get all transactions from database"""
        self.cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
        return self.cursor.fetchall()
    
    def get_all_categories(self) -> List[Tuple]:
        """Get all categories from database"""
        self.cursor.execute('SELECT * FROM categories ORDER BY label')
        return self.cursor.fetchall()
    
    def get_transaction_count(self) -> int:
        """Get total number of transactions"""
        self.cursor.execute('SELECT COUNT(*) FROM transactions')
        return self.cursor.fetchone()[0]
    
    def get_statistics(self) -> dict:
        """Get statistics about transactions"""
        stats = {}
        
        # Total transactions
        stats['total_transactions'] = self.get_transaction_count()
        
        # Total income
        self.cursor.execute('SELECT SUM(income) FROM transactions')
        stats['total_income'] = self.cursor.fetchone()[0] or 0.0
        
        # Total expenses
        self.cursor.execute('SELECT SUM(expense) FROM transactions')
        stats['total_expenses'] = self.cursor.fetchone()[0] or 0.0
        
        # Balance
        stats['balance'] = stats['total_income'] - stats['total_expenses']
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed"""
        self.close()
