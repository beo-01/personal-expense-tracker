
from datetime import date
import sqlite3
from database import create_connection


def show_financial_summary():

    connection = create_connection()

    try:
        cursor = connection.cursor()

        # Calculate overall income and expenses
        cursor.execute("""
            SELECT
                COALESCE(SUM(CASE
                    WHEN transaction_type = 'income'
                    THEN amount ELSE 0 END), 0),

                COALESCE(SUM(CASE
                    WHEN transaction_type = 'expense'
                    THEN amount ELSE 0 END), 0)

            FROM transactions
        """)

        total_income, total_expenses = cursor.fetchone()

        balance = total_income - total_expenses

        # Calculate current month's income and expenses
        current_month = date.today().strftime("%Y-%m")

        cursor.execute("""
            SELECT
                COALESCE(SUM(CASE
                    WHEN transaction_type = 'income'
                    THEN amount ELSE 0 END), 0),

                COALESCE(SUM(CASE
                    WHEN transaction_type = 'expense'
                    THEN amount ELSE 0 END), 0)

            FROM transactions
            WHERE strftime('%Y-%m', transaction_date) = ?
        """, (current_month,))

        monthly_income, monthly_expenses = cursor.fetchone()

        monthly_balance = monthly_income - monthly_expenses

        # Display overall summary
        print("\n========== FINANCIAL SUMMARY ==========")

        print(f"Total Income:    ₦{total_income:,.2f}")
        print(f"Total Expenses:  ₦{total_expenses:,.2f}")
        print(f"Available Balance: ₦{balance:,.2f}")

        # Display monthly summary
        print("\n========== MONTHLY SUMMARY ==========")

        print(f"Month: {current_month}")
        print(f"Monthly Income:   ₦{monthly_income:,.2f}")
        print(f"Monthly Expenses: ₦{monthly_expenses:,.2f}")
        print(f"Monthly Balance:  ₦{monthly_balance:,.2f}")

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        connection.close()


if __name__ == "__main__":
    show_financial_summary()
