"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
import json
import os
from datetime import datetime
class State(rx.State):
    transactions: list[dict] = []
    # Confirmation Dialog State
    confirm_open: bool = False
    transaction_to_delete: dict = {}

    # Form Fields
    amount: str = ""
    category: str = ""
    t_type: str = "Income"
    t_date: str = ""
    description: str = ""

    def set_amount(self, amount: str):
        self.amount = amount

    def set_category(self, category: str):
        self.category = category

    def set_t_type(self, t_type: str):
        self.t_type = t_type

    def set_t_date(self, t_date: str):
        self.t_date = t_date

    def set_description(self, description: str):
        self.description = description

    @rx.var
    def total_income(self) -> float:
        return sum(float(t["amount"]) for t in self.transactions if t["t_type"] == "Income")
    
    @rx.var
    def total_expenses(self) -> float:
        return sum(float(t["amount"]) for t in self.transactions if t["t_type"] == "Expense")
    
    @rx.var
    def balance(self) -> float:
        return self.total_income - self.total_expenses
    
    @rx.var
    def balance_label(self) -> str:
        return "Balance" if self.balance >= 0 else "Overspent"

    @rx.var
    def display_balance(self) -> float:
        return abs(self.balance)

    @rx.var
    def chart_data(self) -> list[dict]:
        """Data for the Income vs Expense Pie Chart."""
        return [
            {"name": "Income", "value": self.total_income, "fill": "green"},
            {"name": "Expenses", "value": self.total_expenses, "fill": "red"},
        ]

    @rx.var
    def category_data(self) -> list[dict]:
        """Data for the Spending by Category Bar Chart."""
        categories = {}
        for t in self.transactions:
            if t["t_type"] == "Expense":
                cat = t["category"]
                categories[cat] = categories.get(cat, 0) + float(t["amount"])
        
        return [{"category": k, "amount": v} for k, v in categories.items()]
    
    def add_transaction(self):
            # Check if required fields are present
            if not self.amount:
                return

            t_date = self.t_date
            if not t_date:
                t_date = datetime.now().strftime("%Y-%m-%d")

            new_t = {
            "amount": float(self.amount),
            "category": self.category.strip().capitalize(),
            "t_type": self.t_type,
            "date": t_date,
            "description": self.description.strip().capitalize(),
        }
        
            self.transactions.append(new_t)
            self.save_data()

            # Clear fields after adding
            self.amount = ""
            self.category = ""
            self.t_type = "Income"
            self.t_date = ""
            self.description = ""
            # Set focus back to the first input for convenience
            return rx.set_focus("amount_input")
    
    def open_delete_confirm(self, transaction: dict):
        self.transaction_to_delete = transaction
        self.confirm_open = True
    
    def close_delete_confirm(self):
        self.confirm_open = False
    
    def confirm_delete(self):
        if self.transaction_to_delete in self.transactions:
            self.transactions.remove(self.transaction_to_delete)
            self.save_data()
        self.confirm_open = False
    
    def handle_enter(self, key: str, next_id: str, submit: bool = False):
        if key == "Enter":
            if submit:
                return self.add_transaction()
            return rx.set_focus(next_id)

    def save_data(self):
        with open("finance_data.json", "w") as file:
            json.dump(self.transactions, file, indent=4)
    
    def load_data(self):
        if os.path.exists("finance_data.json"):
            with open("finance_data.json", "r") as file:
                self.transactions = json.load(file)

def render_transaction(transaction: dict):
    return rx.table.row(
        rx.table.cell(transaction["date"]),
        rx.table.cell(transaction["category"]),
        rx.table.cell(
            rx.badge(
                transaction["t_type"],
                color_scheme = rx.cond(transaction["t_type"] == "Income", "green", "red"),
                variant = "soft",
            ),
        ),
        rx.table.cell(
            rx.text(
                f"PKR {transaction['amount']}",
                color = rx.cond(transaction["t_type"] == "Income", "green", "red"),
                weight = "bold",
            )
        ),
        rx.table.cell(transaction["description"]),
        rx.table.cell(
            rx.button(
                "Delete",
                on_click = lambda: State.open_delete_confirm(transaction),
                color_scheme="red",
                size = "1"
            )
        ),
    )

def index() -> rx.Component:
    return rx.container(
        rx.center(
            rx.vstack(
                rx.heading("AeroLedger", size="9"),
                rx.text("Personal Finance Tracker", size="4", color_scheme="gray", margin_bottom="24px"),
                
                # Stats Section
                rx.hstack(
                    rx.card(
                        rx.vstack(
                            rx.text("Total Income", size="2", color_scheme="gray"),
                            rx.text(f"PKR {State.total_income}", size="6", weight="bold", color_scheme="green"),
                            align="center",
                        ),
                        width="200px",
                    ),
                    rx.card(
                        rx.vstack(
                            rx.text("Total Expenses", size="2", color_scheme="gray"),
                            rx.text(f"PKR {State.total_expenses}", size="6", weight="bold", color_scheme="red"),
                            align="center",
                        ),
                        width="200px",
                    ),
                    rx.card(
                        rx.vstack(
                            rx.text(State.balance_label, size="2", color_scheme="gray"),
                            rx.text(
                                f"PKR {State.display_balance}", 
                                size="6", 
                                weight="bold",
                                color = rx.cond(State.balance >= 0, "green", "red"),
                            ),
                            align="center",
                        ),
                        width="200px",
                    ),
                    spacing="8",
                    padding_y="6",
                    border_bottom="1px solid #eee",
                    width="100%",
                    justify="center",
                ),
                                # Visual Summary Section
                rx.hstack(
                    # Pie Chart: Income vs Expenses
                    rx.card(
                        rx.vstack(
                            rx.text("Income vs Expenses", size="3", weight="bold"),
                            rx.recharts.pie_chart(
                                rx.recharts.pie(
                                    data=State.chart_data,
                                    data_key="value",
                                    name_key="name",
                                    label=True,
                                ),
                                rx.recharts.legend(),
                                width="100%",
                                height=250,
                            ),
                        ),
                        width="50%",
                    ),
                    # Bar Chart: Spending by Category
                    rx.card(
                        rx.vstack(
                            rx.text("Spending by Category", size="3", weight="bold"),
                            rx.recharts.bar_chart(
                                rx.recharts.bar(
                                    data_key="amount",
                                    stroke="#8884d8",
                                    fill="#8884d8",
                                ),
                                rx.recharts.x_axis(data_key="category"),
                                rx.recharts.y_axis(),
                                rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                                data=State.category_data,
                                width="100%",
                                height=250,
                            ),
                        ),
                        width="50%",
                    ),
                    width="100%",
                    spacing="4",
                    padding_y="4",
                ),
                # Form Section (Reorganized into 4 Rows)
                rx.vstack(
                    # Row 1: Amount
                    rx.input(
                        placeholder="Amount", 
                        value=State.amount,
                        on_change=State.set_amount,
                        type="number", 
                        width="100%",
                        id="amount_input",
                        on_key_down=lambda key: State.handle_enter(key, "category_input"),
                    ),
                    # Row 2: Category
                    rx.input(
                        placeholder="Category (e.g. Food, Rent)", 
                        value=State.category,
                        on_change=State.set_category,
                        width="100%",
                        id="category_input",
                        on_key_down=lambda key: State.handle_enter(key, "type_input"),
                    ),
                    # Row 3: Type and Date (Side by side)
                    rx.hstack(
                        rx.select(
                            ["Income", "Expense"],
                            value=State.t_type,
                            on_change=lambda val: [State.set_t_type(val), rx.set_focus("date_input")],
                        ),
                        rx.input(
                            type="date",
                            value=State.t_date,
                            on_change=State.set_t_date,
                            width="50%",
                            id="date_input",
                            on_key_down=lambda key: State.handle_enter(key, "description_input"),
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    # Row 4: Description (Final row, Enter to submit)
                    rx.input(
                        placeholder="Description", 
                        value=State.description,
                        on_change=State.set_description,
                        width="100%",
                        id="description_input",
                        on_key_down=lambda key: State.handle_enter(key, "", submit=True),
                    ),
                    rx.button(
                        "Add Transaction", 
                        on_click=State.add_transaction, 
                        width="100%", 
                        color_scheme="blue"
                    ),
                    spacing="3",
                    width="100%",
                    max_width="800px",
                ),
                # Table Section
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Date"),
                            rx.table.column_header_cell("Category"),
                            rx.table.column_header_cell("Type"),
                            rx.table.column_header_cell("Amount"),
                            rx.table.column_header_cell("Description"),
                            rx.table.column_header_cell("Action"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(State.transactions, render_transaction)
                    ),
                    width="100%",
                    variant="surface",
                    margin_top="32px",
                ),
                # Delete Confirmation Dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Confirm Deletion"),
                        rx.alert_dialog.description(
                            "Are you sure you want to delete this transaction? This action cannot be undone."
                        ),
                        rx.hstack(
                            rx.alert_dialog.cancel(
                                rx.button("Cancel", on_click=State.close_delete_confirm, variant="soft", color_scheme="gray")
                            ),
                            rx.alert_dialog.action(
                                rx.button("Delete", on_click=State.confirm_delete, color_scheme="red")
                            ),
                            spacing="3",
                            margin_top="4",
                            justify="end",
                        ),
                    ),
                    open=State.confirm_open,
                ),
                spacing="5",
                align="center", # Centers items within the vstack
                width="100%",      # Makes the vstack take full width of center
                max_width="1000px", # But limits it so it doesn't get too wide
            ),
            width="100%",
            padding="40px",
        )
    )

app = rx.App()
app.add_page(index, on_load = State.load_data)
