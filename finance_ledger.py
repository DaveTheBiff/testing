import argparse
from typing import List, Dict, Union, Any, Literal

# --- Type Definitions for Strict Type Hinting ---
# A Transaction is a dictionary with specific required keys and types.
# For simplicity, we define the required structure using a type alias.
# Python >= 3.10 allows use of 'list' and 'dict' directly.
# Using older compatible syntax for broader support, but keeping modern types in comments.

# Type alias for a single transaction dictionary
Transaction = Dict[str, Union[str, float]]  # dict[str, str | float]
# Type alias for the entire ledger data structure
Ledger = List[Transaction]  # list[Transaction]
# Allowed transaction types (Category)
TransactionType = Literal["Income", "Expense"]  # Use Literal for string enums


class PersonalFinanceLedger:
    """
    Manages the financial ledger, handling adding transactions, viewing,
    and calculating summaries. Uses a list of dictionaries for internal storage.
    """

    def __init__(self, initial_transactions: Ledger | None = None) -> None:
        """Initializes the ledger with optional starting data."""
        self.transactions: Ledger = (
            initial_transactions if initial_transactions is not None else []
        )
        self.transaction_id_counter: int = 1

    def _get_next_id(self) -> int:
        """Increments and returns the next transaction ID."""
        next_id = self.transaction_id_counter
        self.transaction_id_counter += 1
        return next_id

    def add_transaction(
        self, type: TransactionType, amount: float, description: str, category: str
    ) -> Transaction:
        """
        Adds a new transaction to the ledger.

        :param type: "Income" or "Expense".
        :param amount: The monetary value (must be positive).
        :param description: Short text description.
        :param category: Classification (e.g., 'Groceries', 'Salary').
        :return: The newly created transaction dictionary.
        """
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        transaction: Transaction = {
            "id": self._get_next_id(),
            "type": type,
            "amount": amount,
            "description": description,
            "category": category,
        }
        self.transactions.append(transaction)
        return transaction

    def get_summary(self) -> Dict[str, float]:
        """
        Calculates the total income, total expenses, and net balance.

        :return: A dictionary containing 'total_income', 'total_expense', and 'net_balance'.
        """
        total_income: float = 0.0
        total_expense: float = 0.0

        for tx in self.transactions:
            # We use a runtime check to satisfy Mypy/static analysis tools
            tx_type = tx.get("type", "Expense")  # Default to Expense if missing type
            tx_amount = tx.get("amount", 0.0)

            if tx_type == "Income":
                total_income += float(tx_amount)  # Ensure arithmetic stability
            elif tx_type == "Expense":
                total_expense += float(tx_amount)

        net_balance: float = total_income - total_expense

        return {
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "net_balance": round(net_balance, 2),
        }

    def get_transactions(self) -> Ledger:
        """Returns the full list of transactions."""
        return self.transactions


# --- CLI Implementation ---


def _format_transaction(tx: Transaction) -> str:
    """Helper to format a single transaction for display."""
    sign = "+" if tx["type"] == "Income" else "-"
    color_code = "\033[92m" if tx["type"] == "Income" else "\033[91m"
    reset_code = "\033[0m"

    # Ensure amount is treated as float for formatting
    amount_value = float(tx.get("amount", 0.0))

    return (
        f"ID: {tx['id']} | "
        f"Type: {tx['type'].ljust(7)} | "
        f"Category: {tx['category'].ljust(12)} | "
        f"Amount: {color_code}{sign}${amount_value:.2f}{reset_code} | "
        f"Description: {tx['description']}"
    )


def cli_add_transaction(
    ledger: PersonalFinanceLedger, args: argparse.Namespace
) -> None:
    """Handles the 'add' subcommand."""
    try:
        # Validate and convert types based on user input
        amount_float: float = float(args.amount)
        tx_type: TransactionType = (
            args.type.capitalize()
        )  # Normalize 'income' to 'Income'

        if tx_type not in ["Income", "Expense"]:
            print(f"Error: Invalid type '{args.type}'. Must be 'income' or 'expense'.")
            return

        new_tx = ledger.add_transaction(
            type=tx_type,
            amount=amount_float,
            description=args.description,
            category=args.category,
        )
        print(f"\n✅ Transaction added successfully!")
        print(_format_transaction(new_tx))

    except ValueError as e:
        print(f"\n❌ Error adding transaction: {e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


def cli_view_transactions(
    ledger: PersonalFinanceLedger, args: argparse.Namespace
) -> None:
    """Handles the 'view' subcommand."""
    transactions = ledger.get_transactions()
    if not transactions:
        print("\n\tThe ledger is empty. Use 'add' to record a transaction.")
        return

    print("\n--- Transaction History ---")
    for tx in transactions:
        print(_format_transaction(tx))
    print("---------------------------\n")


def cli_get_summary(ledger: PersonalFinanceLedger, args: argparse.Namespace) -> None:
    """Handles the 'summary' subcommand."""
    summary = ledger.get_summary()

    # Use color codes for better visibility
    green = "\033[92m"
    red = "\033[91m"
    blue = "\033[94m"
    reset = "\033[0m"

    net_color = green if summary["net_balance"] >= 0 else red

    print("\n--- Financial Summary ---")
    print(f"Total Income:  {green}${summary['total_income']:.2f}{reset}")
    print(f"Total Expense: {red}-${summary['total_expense']:.2f}{reset}")
    print(f"Net Balance:   {blue}{net_color}${summary['net_balance']:.2f}{reset}")
    print("---------------------------\n")


def main() -> None:
    """Main entry point for the CLI application."""
    # Initialize the ledger (in a real app, this would load/save data from a file)
    ledger: PersonalFinanceLedger = PersonalFinanceLedger()

    parser = argparse.ArgumentParser(
        description="A simple Command Line Personal Finance Ledger.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- 'add' subcommand ---
    add_parser = subparsers.add_parser("add", help="Add a new transaction.")
    add_parser.add_argument(
        "type",
        type=str,
        choices=["income", "expense"],
        help="Transaction type: 'income' or 'expense'.",
    )
    add_parser.add_argument(
        "amount", type=str, help="The amount (e.g., 100.50). Must be a positive number."
    )
    add_parser.add_argument(
        "description",
        type=str,
        help="A brief description of the transaction (e.g., 'Freelance payment').",
    )
    add_parser.add_argument(
        "category", type=str, help="The category (e.g., 'Salary', 'Groceries', 'Rent')."
    )
    add_parser.set_defaults(func=cli_add_transaction)

    # --- 'view' subcommand ---
    view_parser = subparsers.add_parser("view", help="View all recorded transactions.")
    view_parser.set_defaults(func=cli_view_transactions)

    # --- 'summary' subcommand ---
    summary_parser = subparsers.add_parser(
        "summary", help="Get the current financial summary."
    )
    summary_parser.set_defaults(func=cli_get_summary)

    # Parse arguments and execute the corresponding function
    args = parser.parse_args()
    args.func(ledger, args)


if __name__ == "__main__":
    main()
