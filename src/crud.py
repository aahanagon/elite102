
# point this at the same file your database initializer uses:
import sqlite3
import os

DB_FILE = os.path.join(os.getcwd(), 'data', 'bank.db')

def create_user(name, email, password):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, password)
        )
        conn.commit()
        print(f"User {name!r} created successfully.")

def delete_user(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        print(f"User {user_id} deleted.")

def update_user(user_id, name=None, email=None, password=None):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        if name:
            c.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
        if email:
            c.execute('UPDATE users SET email = ? WHERE id = ?', (email, user_id))
        if password:
            c.execute('UPDATE users SET password = ? WHERE id = ?', (password, user_id))
        conn.commit()
        print(f"User {user_id} updated.")

def check_balance(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
        row = c.fetchone()
        if row:
            print(f"User {user_id} balance: ${row[0]:.2f}")
        else:
            print("User not found.")

def deposit(user_id, amount):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))
        c.execute(
            'INSERT INTO transactions (user_id, type, amount) VALUES (?, "deposit", ?)',
            (user_id, amount)
        )
        conn.commit()
        print(f"Deposited ${amount:.2f} to user {user_id}.")

def withdraw(user_id, amount):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
        balance = c.fetchone()
        if balance and balance[0] >= amount:
            c.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, user_id))
            c.execute(
                'INSERT INTO transactions (user_id, type, amount) VALUES (?, "withdrawal", ?)',
                (user_id, amount)
            )
            conn.commit()
            print(f"Withdrew ${amount:.2f} from user {user_id}.")
        else:
            print("Insufficient funds or user not found.")

def get_transactions(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            'SELECT type, amount, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC',
            (user_id,)
        )
        return c.fetchall()
