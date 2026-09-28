"""
Personal Expense Tracker in Python
Experiential Learning - Project Assessment-I
Student: Ayush Nimbarte (CD25005)
Guide: Prof. Ashwini Yerlewar
"""

import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
HEADERS = ["id", "date", "type", "category", "amount", "note"]

def load_transactions():
    """Load existing financial transactions from CSV file."""
    transactions = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["id"] = int(row["id"])
                row["amount"] = float(row["amount"])
                transactions.append(row)
    return transactions

def save_transactions(transactions):
    """Write all in-memory transactions back to CSV file."""
    with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(transactions)
    print(">> All records saved successfully to " + FILE_NAME)

def add_transaction(transactions):
    """Prompt user to add an income or expense record."""
    print("\n--- Add New Transaction ---")
    t_type = input("Enter Type (1: Income, 2: Expense): ").strip()
    t_type = "income" if t_type == "1" else "expense"
    
    try:
        amount = float(input("Enter Amount (₹): "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount! Please enter a numeric value.")
        return

    category = input("Enter Category (e.g., Food, Travel, Salary, Bills): ").strip()
    note = input("Enter Short Note / Description: ").strip()
    date_str = datetime.now().strftime("%Y-%m-%d")

    new_id = 101 if not transactions else max(t["id"] for t in transactions) + 1
    new_record = {
        "id": new_id,
        "date": date_str,
        "type": t_type,
        "category": category.title(),
        "amount": amount,
        "note": note
    }
    transactions.append(new_record)
    print(f">> Transaction #{new_id} added successfully!")

def view_transactions(transactions):
    """Display all transaction records in a formatted tabular layout."""
    if not transactions:
        print("\n>> No transactions found.")
        return
    print("\n" + "="*75)
    print(f"{'ID':<6}{'Date':<12}{'Type':<10}{'Category':<18}{'Amount (₹)':<12}{'Note'}")
    print("="*75)
    for t in transactions:
        sign = "+" if t["type"] == "income" else "-"
        print(f"{t['id']:<6}{t['date']:<12}{t['type'].upper():<10}{t['category']:<18}{sign + str(t['amount']):<12}{t['note']}")
    print("="*75)

def calculate_balance(transactions):
    """Calculate and display total income, total expenses, and current balance."""
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense

    print("\n" + "="*45)
    print("         FINANCIAL SUMMARY REPORT")
    print("="*45)
    print(f"Total Income   : ₹{total_income:>12.2f}")
    print(f"Total Expenses : ₹{total_expense:>12.2f}")
    print("-" * 45)
    print(f"Current Balance: ₹{balance:>12.2f}")
    print("="*45)

def category_report(transactions):
    """Aggregate expenses by category and display breakdown."""
    expenses = [t for t in transactions if t["type"] == "expense"]
    if not expenses:
        print("\n>> No expenses recorded yet.")
        return
    
    totals = {}
    for t in expenses:
        totals[t["category"]] = totals.get(t["category"], 0.0) + t["amount"]

    grand_total = sum(totals.values())
    print("\n--- Category-Wise Expense Breakdown ---")
    for cat, amt in totals.items():
        pct = (amt / grand_total) * 100
        print(f"• {cat:<18}: ₹{amt:>9.2f} ({pct:>5.1f}%)")
    print(f"Total Expenses     : ₹{grand_total:>9.2f}")

def main():
    """Main execution menu loop."""
    transactions = load_transactions()
    print("\n============================================")
    print("      PERSONAL EXPENSE TRACKER (PYTHON)     ")
    print("============================================")

    while True:
        print("\n[1] Add Transaction")
        print("[2] View All Transactions")
        print("[3] Calculate Balance & Summary")
        print("[4] Category-Wise Expense Report")
        print("[5] Delete Transaction")
        print("[6] Save & Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            calculate_balance(transactions)
        elif choice == "4":
            category_report(transactions)
        elif choice == "5":
            try:
                tid = int(input("Enter Transaction ID to delete: "))
                transactions = [t for t in transactions if t["id"] != tid]
                print(f">> Transaction #{tid} deleted if existed.")
            except ValueError:
                print("Invalid ID.")
        elif choice == "6":
            save_transactions(transactions)
            print("\nThank you for using Personal Expense Tracker!")
            break
        else:
            print("Invalid choice! Please select 1 to 6.")

if __name__ == "__main__":
    main()
