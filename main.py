
from database import create_table
from transactions import add_transaction, view_transactions, search_transactions
from reports import show_financial_summary
from charts import expense_by_category, income_vs_expenses


def main():

    create_table()

    while True:

        print("\n========== PERSONAL EXPENSE TRACKER ==========")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Search Transactions")
        print("4. Financial Summary")
        print("5. Expenses by Category")
        print("6. Income vs Expenses")
        print("7. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_transaction()

        elif choice == "2":
            view_transactions()

        elif choice == "3":
            search_transactions()

        elif choice == "4":
            show_financial_summary()

        elif choice == "5":
            expense_by_category()

        elif choice == "6":
            income_vs_expenses()

        elif choice == "7":
            print("\nThank you for using Personal Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please select between 1 and 7.")


if __name__ == "__main__":
    main()
