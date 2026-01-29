import json
import os
from datetime import datetime
import customtkinter as ctk

class Transaction():
    def __init__(self, amount, category, transaction_type, date = None, description = ""):
        self.amount = float(amount)
        self.category = category
        self.transaction_type = transaction_type
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.description = description

    def to_dict(self):
        return{
            "amount": self.amount,
            "category": self.category,
            "transaction_type": self.transaction_type,
            "date": self.date,
            "description": self.description
            }
        
class FinanceManager:
    def __init__(self, filename = "finance_data.json"):
        self.filename = filename
        self.transactions = []
        self.load_transactions()

    def add_transaction(self, amount, category, t_type, date = None, description = ""):
        
        new_t = Transaction(amount, category, t_type, date = date, description = description)
        self.transactions.append(new_t)
        return f"Added PKR.{amount} to {t_type} - {description}"

    def delete_transaction(self, index):
        if 0 <= index < len(self.transactions):
            removed = self.transactions.pop(index)

            self.save_data()
            return True, f"Removed: {removed.description}"
        return False, "Invalid index."
    
    def get_total_income(self):

        return sum(t.amount for t in self.transactions if t.transaction_type == "Income")

    def get_total_expenses(self):

        return sum(t.amount for t in self.transactions if t.transaction_type == "Expense")

    def get_balance(self):

        return self.get_total_income() - self.get_total_expenses()

    def save_data(self):

        with open(self.filename, "w") as file:
            data = [t.to_dict() for t in self.transactions]
            json.dump(data, file, indent = 4)
        print("Data saved successfully.")

    def load_transactions(self):

        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.transactions = [ Transaction(d["amount"], d["category"], d["transaction_type"], d["date"], d["description"]) for d in data]
                print("Data loaded successfully.")
            except (json.JSONDecodeError, KeyError):
                print("Note: Could not load previous data due to file corruption. Starting fresh!")

class FinanceApp(ctk.CTk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.title("Personal Finance Tracker")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        self.grid_columnconfigure(0, weight = 1)
        
        self.create_widgets()

    def create_widgets(self):
            
        self.title_label = ctk.CTkLabel(self, text = "My Finance Dashboard", font = ("Times New Roman", 32, "bold"))
        self.title_label.grid(row = 0, column = 0, pady = 40)

        balance = self.manager.get_balance()
        self.balance_label = ctk.CTkLabel(
            self,
            text = f"Total Balance: PKR.{balance:.2f}",
            font = ("Times New Roman", 24)
        )
        self.balance_label.grid(row = 1, column = 0, pady = 10)

if __name__ == "__main__":
    manager = FinanceManager()
    app = FinanceApp(manager)
    app.mainloop()
