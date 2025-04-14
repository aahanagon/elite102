import sqlite3

DB_NAME = 'bank.db'

def create_user(name, email, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        ''', (name, email, password))
        conn.commit()
        print(f"User {name} created successfully.")


def delete_user(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        print(f"User {user_id} deleted.")


def update_user(user_id, name=None, email=None, password=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        if name:
            cursor.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
        if email:
            cursor.execute('UPDATE users SET email = ? WHERE id = ?', (email, user_id))
        if password:
            cursor.execute('UPDATE users SET password = ? WHERE id = ?', (password, user_id))
        conn.commit()
        print(f"User {user_id} updated.")


def check_balance(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        if result:
            print(f"User {user_id} balance: ${result[0]:.2f}")
        else:
            print("User not found.")


def deposit(user_id, amount):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))
        cursor.execute('INSERT INTO transactions (user_id, type, amount) VALUES (?, "deposit", ?)', (user_id, amount))
        conn.commit()
        print(f"Deposited ${amount:.2f} to user {user_id}.")


def withdraw(user_id, amount):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
        balance = cursor.fetchone()
        if balance and balance[0] >= amount:
            cursor.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, user_id))
            cursor.execute('INSERT INTO transactions (user_id, type, amount) VALUES (?, "withdrawal", ?)', (user_id, amount))
            conn.commit()
            print(f"Withdrew ${amount:.2f} from user {user_id}.")
        else:
            print("Insufficient funds or user not found.")


# Example test run
if __name__ == "__main__":
    create_user("Alice", "alice@example.com", "pass123")
    deposit(1, 500)
    withdraw(1, 200)
    check_balance(1)
    update_user(1, email="alice@bank.com")
    delete_user(1)
