import sqlite3
import os
import logging
from config.config import DATABASE_PATH
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        self.conn = None
        self.setup_database()

    def setup_database(self):
        """Initialize the database and create tables if they don't exist"""
        try:
            self.conn = sqlite3.connect(DATABASE_PATH)
            cursor = self.conn.cursor()

            # Create tables
            cursor.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    account_balance REAL DEFAULT 0.0
                );

                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    transaction_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );

                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    user_input TEXT,
                    bot_response TEXT,
                    intent TEXT,
                    confidence REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
            ''')

            # Insert demo user if not exists
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, account_balance)
                VALUES (1, 'demo_user', 1000.00)
            ''')

            self.conn.commit()
            logging.info("Database setup completed successfully.")

        except Exception as e:
            logging.error(f"Database setup error: {str(e)}")

    def _get_user_details(self, username):
        """Helper function to get user details by username"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT user_id, account_balance FROM users WHERE username = ?', (username,))
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error fetching user details: {str(e)}")
            return None

    def get_balance(self, user_id):
        """Get account balance for a user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT account_balance FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            logging.error(f"Error getting balance: {str(e)}")
            return None

    def get_transactions(self, user_id, limit=5):
        """Get recent transactions for a user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT transaction_type, amount, timestamp 
                FROM transactions 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (user_id, limit))
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error getting transactions: {str(e)}")
            return []

    def log_conversation(self, user_id, user_input, bot_response, intent, confidence):
        """Log conversation history"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO conversation_history 
                (user_id, user_input, bot_response, intent, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, user_input, bot_response, intent, confidence))
            self.conn.commit()
            logging.info("Conversation logged successfully.")
        except Exception as e:
            logging.error(f"Error logging conversation: {str(e)}")

    def add_transaction(self, user_id, transaction_type, amount):
        """
        Add a new transaction and update account balance
        Args:
            user_id: User's ID
            transaction_type: 'deposit' or 'withdrawal'
            amount: Transaction amount
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure valid transaction type
            if transaction_type.lower() not in ['deposit', 'withdrawal']:
                logging.error(f"Invalid transaction type: {transaction_type}")
                return False

            cursor = self.conn.cursor()

            # First check if user exists and get current balance
            cursor.execute('SELECT account_balance FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if not result:
                logging.error(f"User {user_id} not found")
                return False

            current_balance = result[0]

            # For withdrawals, check if sufficient balance exists
            if transaction_type.lower() == 'withdrawal' and current_balance < amount:
                logging.error("Insufficient balance for withdrawal")
                return False

            new_balance = current_balance + amount if transaction_type.lower() == 'deposit' else current_balance - amount

            # Begin transaction
            cursor.execute('BEGIN TRANSACTION')

            # Add transaction record
            cursor.execute('''
                INSERT INTO transactions (user_id, transaction_type, amount)
                VALUES (?, ?, ?)
            ''', (user_id, transaction_type.lower(), amount))

            # Update user balance
            cursor.execute('''
                UPDATE users 
                SET account_balance = ?
                WHERE user_id = ?
            ''', (new_balance, user_id))

            # Commit transaction
            self.conn.commit()
            logging.info(f"Transaction successful for user {user_id}: {transaction_type} of {amount}")
            return True

        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logging.error(f"Error adding transaction: {str(e)}")
            return False

    def create_user(self, username, initial_balance=0.0):
        """Create a new user account"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, account_balance)
                VALUES (?, ?)
            ''', (username, initial_balance))
            self.conn.commit()
            logging.info(f"User created successfully: {username}")
            return cursor.lastrowid  # Returns the new user_id
        except sqlite3.IntegrityError:
            logging.error(f"User {username} already exists")
            return None
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            return None

    def get_user_by_username(self, username):
        """Get user details by username"""
        user = self._get_user_details(username)
        if user:
            return {"user_id": user[0], "username": username, "account_balance": user[1]}
        return None

    def transfer_money(self, from_username, to_username, amount):
        """Transfer money between users"""
        try:
            from_user = self._get_user_details(from_username)
            to_user = self._get_user_details(to_username)

            if not from_user or not to_user:
                return "One or both users not found"

            if from_user[1] < amount:
                return "Insufficient balance for transfer"

            # Begin transaction
            cursor = self.conn.cursor()
            cursor.execute('BEGIN TRANSACTION')

            # Deduct from sender
            cursor.execute('''
                UPDATE users 
                SET account_balance = account_balance - ?
                WHERE username = ?
            ''', (amount, from_username))

            # Add to receiver
            cursor.execute('''
                UPDATE users 
                SET account_balance = account_balance + ?
                WHERE username = ?
            ''', (amount, to_username))

            # Log transfer transaction for both users
            cursor.execute('''
                INSERT INTO transactions (user_id, transaction_type, amount)
                VALUES (?, ?, ?)
            ''', (from_user[0], f'transfer_to_{to_username}', -amount))

            cursor.execute('''
                INSERT INTO transactions (user_id, transaction_type, amount)
                VALUES (?, ?, ?)
            ''', (to_user[0], f'transfer_from_{from_username}', amount))

            self.conn.commit()
            logging.info(f"Transfer successful: {from_username} to {to_username} for {amount}")
            return "Transfer successful"

        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logging.error(f"Error in transfer: {str(e)}")
            return "Transfer failed"

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")
