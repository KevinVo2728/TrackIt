import os
import json
from datetime import datetime

transactions = []
balance = 0.0

def TrackIt_Intro():
    print("=" * 35)
    print("    Welcome to TrackIT 💸")
    print("    A Tracker for your finances")
    print("    Track income, expenses, and balance")
    print("=" * 35 + "\n")

def Menu():
    print("Main Menu:")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Balance")
    print("4. View Transaction History")
    print("5. View Category Summary")
    print("6. View Income Summary")
    print("7. Reset All Data")
    print("8. Exit\n")

def save_info(transactions, balance):
    data = {"balance": round(balance, 2), "transactions": transactions}
    temp_file = "TrackIt_data_temp.json"
    final_file = "TrackIt_data.json"
    with open(temp_file, "w") as file:
        json.dump(data, file, indent=4)
    os.replace(temp_file, final_file)
    print("Data Saved Safely! ✅\n")

def load_info():
    transactions = []
    balance = 0.0
    try: 
        with open("TrackIt_data.json", "r") as file:
            data = json.load(file)
            balance = data["balance"]
            transactions = data["transactions"]
    except FileNotFoundError:
        print("No previous file found. Starting New.\n")
    return transactions, balance

def add_income(transactions, balance):
    while True:
        amount_input = input("Enter Income Amount (or 'b' to go back): $")
        if amount_input.lower() == 'b':
            return transactions, balance, "Cancelled adding income."
        try:
            amount = float(amount_input)
            desc = input("Description: ")
            transaction = { "type": "income", "amount": amount, "description": desc, "category": "", "date": str(datetime.now())}
            transactions.append(transaction)
            balance += round(amount, 2)
            save_info(transactions, balance)
            return transactions, balance, f"Added income of ${amount:.2f} ({desc})"
        except ValueError:
            print("⚠️ That's not a valid number. Please try again.\n")

def add_expense(transactions, balance, categories):
    while True:
        amount_input = input("Enter expense amount (or 'b' to go back): $")
        if amount_input.lower() == 'b':
            return transactions, balance, "Cancelled adding expense."
        try: 
            amount = float(amount_input)
            description = input("Description: ")
            valid_category = False
            category = "other"
            while not valid_category:
                print("Select a category (or 'b' to go back):")
                for i, cat in enumerate(categories):
                    print(f"{i + 1}. {cat}")
                choice = input("Choose a category number: ")
                if choice.lower() == 'b':
                    return transactions, balance, "Cancelled adding expense."
                if choice.isdigit() and 0 < int(choice) <= len(categories):
                    category = categories[int(choice) - 1]
                    valid_category = True
                else:
                    print("Invalid choice. Please Try Again.")
            transaction = {"type": "expense", "amount": round(amount, 2), "description": description, "category": category, "date": str(datetime.now())}
            transactions.append(transaction)
            balance -= round(amount, 2)
            save_info(transactions, balance)
            return transactions, balance, f"Added expense of ${amount:.2f} ({description}, {category})"
        except ValueError:
            print("⚠️ Invalid number. Please try again.\n")

def view_balance(balance):
    print(f"Current balance: ${balance:.2f}\n")
    input("Press Enter to return to the menu...")      

def view_history(transactions):
    print("Transaction History (Newest First):")
    if len(transactions) == 0:
        print("No transactions yet. \n")
        return
    for t in transactions[::-1]:
        date = t["date"].split(" ")[0]
        line = f"{date} | {t['type'].capitalize():7} | ${t['amount']:8.2f} | {t['description']}"
        if t["category"]:
            line += f" ({t['category']})"
        print(line)
    input("Press Enter to return to the menu...")

def view_category_summary(transactions, categories):
    print("Category Summary (Expenses):")
    summary = {cat: 0 for cat in categories}
    for t in transactions:
        if t["type"] == "expense":
            cat = t["category"] if t["category"] in categories else "other"
            summary[cat] += t["amount"]
    for cat in categories:
        print(f"{cat.capitalize():13}: ${summary[cat]:.2f}")
    total = sum(summary.values())
    print(f"{'Total':13}: ${total:.2f}\n")
    input("Press Enter to return to the menu...")

def view_income_summary(transactions):
    print("Income Summary:")
    total_income = 0.0
    for t in transactions:
        if t["type"] == "income":
            total_income += t["amount"]
    print("Total Income: $" + str(round(total_income, 2)))
    input("Press Enter to return to the menu...")

def reset_data():
    confirm = input("⚠️ Are you sure you want to reset all data? This cannot be undone. (y/n): ")
    if confirm.lower() == "y":
        global transactions, balance
        transactions = []
        balance = 0.0
        with open("TrackIt_data.json", "w") as file:
            json.dump({"balance": balance, "transactions": transactions}, file, indent=4)
        temp_file = "TrackIt_data_temp.json"
        if os.path.exists(temp_file):
            os.remove(temp_file)
        print("✅ All data has been reset!\n")
        input("Press Enter to return to the menu...")
    else:
        print("Reset cancelled.\n")
        input("Press Enter to return to the menu...")

def run_TrackIT():
    transactions, balance = load_info()
    categories = ["food", "rent", "entertainment", "shopping", "other"]
    last_action = ""
    TrackIt_Intro()
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n")
        if last_action:
            print(f"Last action: {last_action}\n")
        Menu()
        choice = input("Select an option from 1 to 8:? ")
        if choice == "1":
            transactions, balance, action_msg = add_income(transactions, balance)
            last_action = action_msg
        elif choice == "2":
            transactions, balance, action_msg = add_expense(transactions, balance, categories)
            last_action = action_msg
        elif choice == "3":
            view_balance(balance)
            last_action = f"Viewed balance: ${balance:.2f}"
        elif choice == "4":
            view_history(transactions)
            last_action = "Viewed transaction history."
        elif choice == "5":
            view_category_summary(transactions, categories)
            last_action = "Viewed category summary."
        elif choice == "6":
            view_income_summary(transactions)
            last_action = "Viewed income summary."
        elif choice == "7":
            reset_data()
            last_action = "All data reset."
        elif choice == "8":
            print("Thank you for using TrackIT. Hopefully Today Was Another Step To Your Goals!")
            return
        else:
            print("Invalid Option. Press Enter to return to Main Menu.\n")
            input()
            last_action = "Invalid menu choice."

run_TrackIT()