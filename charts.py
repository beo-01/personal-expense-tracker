
import sqlite3
import matplotlib.pyplot as plt
from database import create_connection


def expense_by_category():

    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE transaction_type = 'expense'
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)

        results = cursor.fetchall()

        if not results:
            print("No expense records available.")
            return

        categories = [row[0] for row in results]
        amounts = [row[1] for row in results]

        plt.bar(categories, amounts)

        plt.title("Expenses by Category")
        plt.xlabel("Categories")
        plt.ylabel("Amount (₦)")

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        connection.close()


def income_vs_expenses():

    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                SUM(CASE WHEN transaction_type = 'income'
                    THEN amount ELSE 0 END),

                SUM(CASE WHEN transaction_type = 'expense'
                    THEN amount ELSE 0 END)

            FROM transactions
        """)

        income, expenses = cursor.fetchone()

        income = income or 0
        expenses = expenses or 0

        labels = ["Income", "Expenses"]
        amounts = [income, expenses]

        plt.bar(labels, amounts)

        plt.title("Income vs Expenses")
        plt.ylabel("Amount (₦)")

        plt.tight_layout()
        plt.show()

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        connection.close()


if __name__ == "__main__":

    print("1. View Expenses by Category")
    print("2. View Income vs Expenses")

    choice = input("Choose an option: ")

    if choice == "1":
        expense_by_category()

    elif choice == "2":
        income_vs_expenses()

    else:
        print("Invalid option.")
