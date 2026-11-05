
import sqlite3
from datetime import date
from database import create_connection


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return amount

        except ValueError:
            print("Please enter a valid number.")

#add transaction
def add_transaction():

    print("\n--- ADD TRANSACTION ---")

    # Get transaction type
    while True:
        transaction_type = input(
            "Enter type (income/expense): "
        ).strip().lower()

        if transaction_type in ["income", "expense"]:
            break

        print("Please enter either income or expense.")

    # Get category
    while True:
        category = input("Enter category: ").strip()

        if category:
            break

        print("Category cannot be empty.")

    # Get amount
    amount = get_valid_amount()

    # Get description
    description = input("Enter description: ").strip()

    # Get today's date automatically
    transaction_date = date.today().isoformat()

    # Save to database
    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (transaction_type, category, amount, description, transaction_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        ))

        connection.commit()

        print("\nTransaction added successfully!")

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        connection.close()

if __name__ == "__main__":
    add_transaction()        





#veiw tansaction

def view_transactions():

    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM transactions
            ORDER BY transaction_date DESC, id DESC
        """)

        transactions = cursor.fetchall()

        if not transactions:
            print("\nNo transactions found.")
            return

        print("\n========== ALL TRANSACTIONS ==========")

        print(
            f"{'ID':<5} {'TYPE':<12} {'CATEGORY':<15} "
            f"{'AMOUNT':<15} {'DATE':<15} {'DESCRIPTION'}"
        )

        print("-" * 85)

        for transaction in transactions:

            transaction_id = transaction[0]
            transaction_type = transaction[1]
            category = transaction[2]
            amount = transaction[3]
            description = transaction[4]
            transaction_date = transaction[5]

            print(
                f"{transaction_id:<5} "
                f"{transaction_type:<12} "
                f"{category:<15} "
                f"{amount:<15.2f} "
                f"{transaction_date:<15} "
                f"{description}"
            )

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        connection.close()

if __name__ == "__main__":
    view_transactions()




def search_transactions():

    print("\n--- SEARCH TRANSACTIONS ---")
    print("1. Search by category")
    print("2. Filter by transaction type")
    print("3. Search by date")

    choice = input("Choose an option: ").strip()

    connection = create_connection()

    try:
        cursor = connection.cursor()

        if choice == "1":
            category = input("Enter category: ").strip()

            if not category:
                print("Category cannot be empty.")
                return

            cursor.execute("""
                SELECT * FROM transactions
                WHERE category LIKE ? COLLATE NOCASE
                ORDER BY transaction_date DESC, id DESC
            """, (f"%{category}%",))

        elif choice == "2":
            transaction_type = input(
                "Enter type (income/expense): "
            ).strip().lower()

            if transaction_type not in ["income", "expense"]:
                print("Invalid transaction type.")
                return

            cursor.execute("""
                SELECT * FROM transactions
                WHERE transaction_type = ?
                ORDER BY transaction_date DESC, id DESC
            """, (transaction_type,))

        elif choice == "3":
            search_date = input("Enter date (YYYY-MM-DD): ").strip()

            try:
                date.fromisoformat(search_date)
            except ValueError:
                print("Invalid date format.")
                return

            cursor.execute("""
                SELECT * FROM transactions
                WHERE transaction_date = ?
                ORDER BY id DESC
            """, (search_date,))

        else:
            print("Invalid option.")
            return

        transactions = cursor.fetchall()

        if not transactions:
            print("\nNo matching transactions found.")
            return

        print("\n========== SEARCH RESULTS ==========")

        print(
            f"{'ID':<5} {'TYPE':<12} {'CATEGORY':<15} "
            f"{'AMOUNT':<15} {'DATE':<15} {'DESCRIPTION'}"
        )

        print("-" * 85)

        for transaction in transactions:
            print(
                f"{transaction[0]:<5} "
                f"{transaction[1]:<12} "
                f"{transaction[2]:<15} "
                f"{transaction[3]:<15.2f} "
                f"{transaction[5]:<15} "
                f"{transaction[4]}"
            )

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        connection.close()

if __name__ == "__main__":
    search_transactions()


