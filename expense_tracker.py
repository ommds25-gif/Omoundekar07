"""
Personal Expense Tracker in Python
Experiential Learning - Project Assessment-I
Student: Om Mohan Moundekar (CD25026)
Guide: Prof. Ashwini Yerlewar
"""
"""
Personal Expense Tracker
------------------------
A menu-driven Python program to record, organize and monitor income and expenses.
Features : Add / View / Update / Delete transactions, summary, monthly report,
           category-wise report.
Storage  : transactions.json (created automatically in the same folder).
"""

import json
import os
from datetime import datetime

FILE = "transactions.json"

EXPENSE_CATEGORIES = ["Food", "Travel", "Rent", "Bills", "Shopping",
                      "Health", "Education", "Entertainment", "Other"]
INCOME_CATEGORIES = ["Salary", "Freelance", "Pocket Money", "Gifts",
                     "Investments", "Other"]


# ---------------------------------------------------------------- storage ----
def load_data():
    """Read all transactions from the file (empty list if file is missing/broken)."""
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: data file unreadable. Starting with an empty list.")
        return []


def save_data(data):
    """Write all transactions to the file."""
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ----------------------------------------------------------- input helpers ----
def get_amount(prompt="Enter amount: "):
    while True:
        try:
            amount = float(input(prompt))
            if amount > 0:
                return round(amount, 2)
            print("  Amount must be greater than 0.")
        except ValueError:
            print("  Please enter a valid number.")


def get_date(prompt="Enter date (YYYY-MM-DD, Enter = today): "):
    while True:
        text = input(prompt).strip()
        if text == "":
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("  Invalid date. Use the format YYYY-MM-DD.")


def get_type():
    while True:
        t = input("Type (1 = Income, 2 = Expense): ").strip()
        if t == "1":
            return "income"
        if t == "2":
            return "expense"
        print("  Please enter 1 or 2.")


def get_category(t_type):
    options = INCOME_CATEGORIES if t_type == "income" else EXPENSE_CATEGORIES
    print("Categories:")
    for i, c in enumerate(options, 1):
        print(f"  {i}. {c}")
    while True:
        choice = input("Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("  Invalid choice. Try again.")


def get_month(prompt="Enter month (YYYY-MM): "):
    while True:
        text = input(prompt).strip()
        try:
            datetime.strptime(text, "%Y-%m")
            return text
        except ValueError:
            print("  Invalid month. Use the format YYYY-MM.")


def find_by_id(data, t_id):
    for t in data:
        if t["id"] == t_id:
            return t
    return None


def get_id(prompt="Enter transaction ID: "):
    while True:
        text = input(prompt).strip()
        if text.isdigit():
            return int(text)
        print("  ID must be a number.")


# ------------------------------------------------------------- operations ----
def add_transaction(data):
    print("\n--- Add Transaction ---")
    t_type = get_type()
    category = get_category(t_type)
    amount = get_amount()
    date = get_date()
    note = input("Note (optional): ").strip()
    new_id = max((t["id"] for t in data), default=100) + 1   # unique ID
    data.append({"id": new_id, "date": date, "type": t_type,
                 "category": category, "amount": amount, "note": note})
    save_data(data)
    print(f"Transaction saved with ID {new_id}.")


def print_table(records):
    if not records:
        print("No transactions found.")
        return
    print(f"\n{'ID':<5}{'Date':<12}{'Type':<9}{'Category':<15}{'Amount':>10}  Note")
    print("-" * 70)
    for t in sorted(records, key=lambda x: x["date"]):
        print(f"{t['id']:<5}{t['date']:<12}{t['type']:<9}{t['category']:<15}"
              f"{t['amount']:>10.2f}  {t['note']}")


def view_transactions(data):
    print("\n--- View Transactions ---")
    print("1. All   2. By month   3. By category")
    choice = input("Choose: ").strip()
    if choice == "2":
        month = get_month()
        print_table([t for t in data if t["date"].startswith(month)])
    elif choice == "3":
        cat = input("Enter category name: ").strip().lower()
        print_table([t for t in data if t["category"].lower() == cat])
    else:
        print_table(data)


def update_transaction(data):
    print("\n--- Update Transaction ---")
    t = find_by_id(data, get_id())
    if t is None:
        print("ID not found.")
        return
    print_table([t])
    print("Press Enter to keep the old value.")

    new_type = input(f"Type [{t['type']}] (1 = income, 2 = expense): ").strip()
    if new_type in ("1", "2"):
        t["type"] = "income" if new_type == "1" else "expense"
        print("  Type changed, please pick a matching category.")
        t["category"] = get_category(t["type"])
    else:
        if input(f"Change category [{t['category']}]? (y/n): ").lower() == "y":
            t["category"] = get_category(t["type"])

    amt = input(f"Amount [{t['amount']}]: ").strip()
    if amt:
        try:
            if float(amt) > 0:
                t["amount"] = round(float(amt), 2)
            else:
                print("  Invalid amount, old value kept.")
        except ValueError:
            print("  Invalid amount, old value kept.")

    date = input(f"Date [{t['date']}]: ").strip()
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            t["date"] = date
        except ValueError:
            print("  Invalid date, old value kept.")

    note = input(f"Note [{t['note']}]: ").strip()
    if note:
        t["note"] = note

    save_data(data)
    print("Transaction updated.")


def delete_transaction(data):
    print("\n--- Delete Transaction ---")
    t = find_by_id(data, get_id())
    if t is None:
        print("ID not found.")
        return
    print_table([t])
    if input("Delete this record? (y/n): ").strip().lower() == "y":
        data.remove(t)
        save_data(data)
        print("Transaction deleted.")
    else:
        print("Delete cancelled.")


def calculate_summary(records):
    income = sum(t["amount"] for t in records if t["type"] == "income")
    expense = sum(t["amount"] for t in records if t["type"] == "expense")
    return income, expense, income - expense


def show_summary(data):
    income, expense, balance = calculate_summary(data)
    print("\n--- Summary ---")
    print(f"Total Income   : {income:>12.2f}")
    print(f"Total Expenses : {expense:>12.2f}")
    print(f"Balance        : {balance:>12.2f}")
    if balance < 0:
        print("Warning: you are spending more than you earn!")


def monthly_report(data):
    print("\n--- Monthly Report ---")
    month = get_month()
    records = [t for t in data if t["date"].startswith(month)]
    if not records:
        print("No transactions in that month.")
        return
    income, expense, balance = calculate_summary(records)
    print_table(records)
    print(f"\nReport for {month}")
    print(f"  Income  : {income:.2f}")
    print(f"  Expense : {expense:.2f}")
    print(f"  Savings : {balance:.2f}")


def category_report(data):
    print("\n--- Category-wise Expense Report ---")
    month = input("Month (YYYY-MM) or Enter for all time: ").strip()
    totals = {}
    for t in data:
        if t["type"] == "expense" and t["date"].startswith(month):
            totals[t["category"]] = totals.get(t["category"], 0) + t["amount"]
    if not totals:
        print("No expenses found.")
        return
    grand = sum(totals.values())
    print(f"\n{'Category':<15}{'Total':>10}{'Share':>9}")
    print("-" * 34)
    for cat, amt in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f"{cat:<15}{amt:>10.2f}{amt / grand * 100:>8.1f}%")
    print("-" * 34)
    print(f"{'Total':<15}{grand:>10.2f}")


# ------------------------------------------------------------------- menu ----
def show_menu():
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Update Transaction")
    print("4. Delete Transaction")
    print("5. Show Summary")
    print("6. Reports (Monthly / Category)")
    print("7. Exit")


def main():
    data = load_data()
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_transaction(data)
        elif choice == "2":
            view_transactions(data)
        elif choice == "3":
            update_transaction(data)
        elif choice == "4":
            delete_transaction(data)
        elif choice == "5":
            show_summary(data)
        elif choice == "6":
            print("\n1. Monthly report   2. Category report")
            sub = input("Choose: ").strip()
            if sub == "1":
                monthly_report(data)
            elif sub == "2":
                category_report(data)
            else:
                print("Invalid choice.")
        elif choice == "7":
            save_data(data)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
