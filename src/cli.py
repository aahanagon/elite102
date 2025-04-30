# src/cli.py
import getpass
import sqlite3
import os
from database import initialize_database

# ensure the DB path matches your setup
DB_NAME = os.path.join(os.getcwd(), 'data', 'bank.db')

from crud import (
    create_user, delete_user, update_user,
    check_balance, deposit, withdraw, get_transactions
)

def main_menu():
    print("""
=== Elite Bank CLI ===
1) Login
2) Register
0) Exit
""")

def user_menu():
    print("""
--- Account Menu ---
1) Check balance
2) Deposit
3) Withdraw
4) View transactions
5) Update my info
6) Delete my account
0) Logout
""")

def run():
    # make sure your tables exist
    initialize_database()

    while True:
        main_menu()
        choice = input("Select> ").strip()

        if choice == "1":
            email = input("Email: ").strip()
            pw    = getpass.getpass("Password: ").strip()
            user = None
            with sqlite3.connect(DB_NAME) as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, name, email, balance FROM users WHERE email=? AND password=?",
                    (email, pw)
                )
                row = cur.fetchone()
                if row:
                    user = {"id":row[0], "name":row[1], "email":row[2], "balance":row[3]}
            if not user:
                print("❌ Invalid credentials.\n")
                continue

            print(f"\n✅ Welcome, {user['name'] or user['email']}!\n")
            while True:
                user_menu()
                u = input("Choice> ").strip()

                if u == "1":
                    check_balance(user["id"])

                elif u == "2":
                    amt = float(input("Amount to deposit: "))
                    deposit(user["id"], amt)

                elif u == "3":
                    amt = float(input("Amount to withdraw: "))
                    withdraw(user["id"], amt)

                elif u == "4":
                    txs = get_transactions(user["id"])
                    if not txs:
                        print("No transactions yet.")
                    else:
                        print("\nType      Amount     Timestamp")
                        print("-"*40)
                        for ttype, amt, ts in txs:
                            print(f"{ttype:<10}  ${amt:>8.2f}  {ts}")
                        print()

                elif u == "5":
                    new_name  = input("New name (leave blank to skip): ").strip()
                    new_email = input("New email (leave blank to skip): ").strip()
                    new_pw    = getpass.getpass("New password (leave blank to skip): ").strip()
                    update_user(user["id"],
                                name=new_name or None,
                                email=new_email or None,
                                password=new_pw or None)

                elif u == "6":
                    confirm = input("Type DELETE to confirm account deletion: ")
                    if confirm == "DELETE":
                        delete_user(user["id"])
                        print("Your account has been deleted. Exiting.")
                        return
                    else:
                        print("Aborted delete.")

                elif u == "0":
                    print("Logging out.\n")
                    break

                else:
                    print("❌ Invalid option.")

        elif choice == "2":
            name  = input("Your name: ").strip()
            email = input("Your email: ").strip()
            pw    = getpass.getpass("Choose a password: ").strip()
            create_user(name, email, pw)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("❌ Invalid selection.\n")

if __name__ == "__main__":
    run()
