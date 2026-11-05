
import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
from datetime import date
from database import create_connection, create_table


# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Create the database table if it doesn't exist
create_table()


st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stMetric"] {
            background-color: #f0f4f8;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #dce3ea;
        }

        [data-testid="stMetricLabel"] {
            color: #52616b;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: #16324f;
            font-weight: bold;
        }

        [data-testid="stSidebar"] {
            background-color: #16324f;
        }

        [data-testid="stSidebar"] * {
            color: white;
        }

        h1, h2, h3 {
            color: #16324f;
        }

        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)



# Get financial summary
def get_financial_summary():

    connection = create_connection()

    try:
        cursor = connection.cursor()

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

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": total_income - total_expenses,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "monthly_balance": monthly_income - monthly_expenses
        }

    except sqlite3.Error as error:
        st.error(f"Database error: {error}")
        return None

    finally:
        connection.close()


# Get expenses grouped by category
def get_expenses_by_category():

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

        return cursor.fetchall()

    except sqlite3.Error as error:
        st.error(f"Database error: {error}")
        return []

    finally:
        connection.close()



def save_transaction(transaction_type, category, amount, description, transaction_date):

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

        return True

    except sqlite3.Error as error:
        st.error(f"Database error: {error}")
        return False

    finally:
        connection.close()



def get_all_transactions():

    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, transaction_type, category, amount,
                   description, transaction_date
            FROM transactions
            ORDER BY transaction_date DESC, id DESC
        """)

        transactions = cursor.fetchall()

        return transactions

    except sqlite3.Error as error:
        st.error(f"Database error: {error}")
        return []

    finally:
        connection.close()




# Sidebar navigation
st.sidebar.title("💰 Expense Tracker")

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Add Transaction", "Transaction History"]
)


# Overview page
if page == "Overview":

    st.title("💰 Personal Finance Dashboard")

    st.caption(
        "Track your income, monitor expenses, "
        "and stay in control of your finances."
    )

    st.divider()

    summary = get_financial_summary()

    if summary is not None:

        # Overall summary
        st.subheader("Overall Financial Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Income",
            f"₦{summary['total_income']:,.2f}"
        )

        col2.metric(
            "Total Expenses",
            f"₦{summary['total_expenses']:,.2f}"
        )

        col3.metric(
            "Available Balance",
            f"₦{summary['balance']:,.2f}"
        )

        st.divider()

        # Monthly summary
        st.subheader("Monthly Financial Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Monthly Income",
            f"₦{summary['monthly_income']:,.2f}"
        )

        col2.metric(
            "Monthly Expenses",
            f"₦{summary['monthly_expenses']:,.2f}"
        )

        col3.metric(
            "Monthly Balance",
            f"₦{summary['monthly_balance']:,.2f}"
        )

        st.divider()

        # Charts
        st.subheader("Financial Analytics")

        chart_col1, chart_col2 = st.columns(2)

        # Expenses by category
        with chart_col1:

            st.write("**Expenses by Category**")

            results = get_expenses_by_category()

            if results:

                categories = [row[0] for row in results]
                amounts = [row[1] for row in results]

                fig, ax = plt.subplots()

                ax.bar(categories, amounts)

                ax.set_xlabel("Categories")
                ax.set_ylabel("Amount (₦)")
                ax.set_title("Spending by Category")

                plt.xticks(rotation=45)
                fig.tight_layout()

                st.pyplot(fig)
                plt.close(fig)

            else:
                st.info("No expense records available.")

        # Income vs expenses
        with chart_col2:

            st.write("**Income vs Expenses**")

            labels = ["Income", "Expenses"]

            amounts = [
                summary["total_income"],
                summary["total_expenses"]
            ]

            fig, ax = plt.subplots()

            ax.bar(labels, amounts)

            ax.set_ylabel("Amount (₦)")
            ax.set_title("Income vs Expenses")

            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)


# Add Transaction page

elif page == "Add Transaction":

    st.title("Add New Transaction")

    st.write("Record your income and expenses here.")

    with st.form("transaction_form", clear_on_submit=True):

        transaction_type = st.selectbox(
            "Transaction Type",
            ["income", "expense"]
        )

        category = st.text_input(
            "Category",
            placeholder="e.g. Food, Salary, Transport"
        )

        amount = st.number_input(
            "Amount (₦)",
            min_value=0.01,
            step=100.0
        )

        description = st.text_area(
            "Description",
            placeholder="Enter transaction details"
        )

        transaction_date = st.date_input(
            "Transaction Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Save Transaction"
        )

        if submitted:

            if not category.strip():
                st.error("Please enter a category.")

            else:

                success = save_transaction(
                    transaction_type,
                    category.strip(),
                    amount,
                    description.strip(),
                    transaction_date.isoformat()
                )

                if success:
                    st.success("Transaction saved successfully!")

# Transaction History page

elif page == "Transaction History":

    st.title("Transaction History")

    transactions = get_all_transactions()

    if transactions:

        transaction_filter = st.selectbox(
            "Filter by Transaction Type",
            ["All", "income", "expense"]
        )

        # Apply the selected filter
        if transaction_filter != "All":
            transactions = [
                transaction for transaction in transactions
                if transaction[1] == transaction_filter
            ]

        # Prepare transactions for display
        transaction_data = []

        for transaction in transactions:
            transaction_data.append({
                "ID": transaction[0],
                "Type": transaction[1].title(),
                "Category": transaction[2],
                "Amount (₦)": transaction[3],
                "Description": transaction[4],
                "Date": transaction[5]
            })

        if transaction_data:
            
            st.dataframe(
                transaction_data,
                use_container_width=True,
                hide_index=True,

                column_config={
                    "ID": st.column_config.NumberColumn(
                        "Transaction ID",
                        format="%d"
                    ),

                    "Type": st.column_config.TextColumn(
                        "Transaction Type"
                    ),

                    "Category": st.column_config.TextColumn(
                        "Category"
                    ),

                    "Amount (₦)": st.column_config.NumberColumn(
                        "Amount",
                        format="₦%.2f"
                    ),

                    "Description": st.column_config.TextColumn(
                        "Description"
                    ),

                    "Date": st.column_config.DateColumn(
                        "Transaction Date",
                        format="DD MMM YYYY"
                    )
                }
            )

        else:
            st.info("No transactions found for this filter.")

    else:
        st.info("You haven't recorded any transactions yet.")
