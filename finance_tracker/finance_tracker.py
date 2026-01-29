"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
import json
import os
from datetime import datetime
class State(rx.State):
    transactions: list[dict] = []
    @rx.var

    def total_income(self) -> float:
        return sum(float(t["amount"]) for t in self.transactions if t["transaction_type"] == "Income")
    @rx.var

    def total_expenses(self) -> float:
        return sum(float(t["amount"]) for t in self.transactions if t["transaction_type"] == "Expense")
    @rx.var

    def balance(self) -> float:
        return self.total_income - self.total_expenses
    
    def add_transaction(self, form_data: dict):
            amount = form_data.get("amount", "0.00")
            category = form_data.get("category", "")
            t_type = form_data.get("transaction_type", "")
            description = form_data.get("description", "")

            new_t = {
            "amount": float(amount),
            "category": category,
            "transaction_type": t_type,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": description,
        }
        
            self.transactions.append(new_t)
            self.save_data()
    
    def delete_transaction(self, index: int):
        self.transactions.pop(index)
        self.save_data()
    
    def save_data(self):
        with open("finance_data.json", "w") as file:
            json.dump(self.transactions, file, indent=4)
    
    def load_data(self):
        if os.path.exists("finance_data.json"):
            with open("finance_data.json", "r") as file:
                self.transactions = json.load(file)

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Finance Tracker",  size = "9"),
            rx.hstack(
                rx.stat(
                    rx.stat_label("Balance"),
                    rx.stat_number(f"PKR {State.balance}"),
                ),
                rx.stat(
                    rx.stat_label("Income"),
                    rx.stat_number(f"PKR {State.total_income}"),
                    color_scheme="green",
                ),
                spacing="4",
            ),
            # Input Form
            rx.form(
                rx.vstack(
                    rx.input(placeholder="Amount", name="amount", type="number"),
                    rx.input(placeholder="Category (e.g. Food, Rent)", name="category"),
                    rx.select(
                        ["Income", "Expense"],
                        placeholder="Select Type",
                        name="t_type",
                    ),
                    rx.input(placeholder="Description", name="description"),
                    rx.button("Add Transaction", type="submit"),
                    spacing="3",
                ),
                # When submitted, call add_transaction with form data
                on_submit=State.add_transaction,
                reset_on_submit=True,
            ),
            spacing="5",
            align="center",
        )
    )


app = rx.App()
app.add_page(index)
