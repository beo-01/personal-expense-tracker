import streamlit as st
import matplotlib.pyplot as plt
from datetime import date

from supabase_client import get_supabase_client
from auth import (
    sign_up,
    sign_in,
    sign_out,
    reset_password,
    update_password
)


# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Connect to Supabase
supabase = get_supabase_client()



# Check for password recovery
if "code" in st.query_params:

    recovery_code = st.query_params["code"]

    try:
        response = supabase.auth.exchange_code_for_session(
            {"auth_code": recovery_code}
        )

        st.session_state["access_token"] = response.session.access_token
        st.session_state["refresh_token"] = response.session.refresh_token
        st.session_state["password_recovery"] = True

        st.query_params.clear()
        st.rerun()

    except Exception as error:
        st.error(f"Password recovery failed: {error}")


# Password recovery screen
if st.session_state.get("password_recovery"):

    st.title("Reset Your Password")

    st.write("Enter your new password below.")

    with st.form("new_password_form"):

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password"
        )

        submitted = st.form_submit_button("Update Password")

        if submitted:

            if len(new_password) < 8:
                st.error("Password must contain at least 8 characters.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:

                try:
                    update_password(supabase, new_password)

                    st.session_state.pop("access_token", None)
                    st.session_state.pop("refresh_token", None)
                    st.session_state.pop("password_recovery", None)

                    st.success("Password updated successfully!")
                    st.rerun()

                except Exception as error:
                    st.error(f"Could not update password: {error}")

    st.stop()




# Check whether the user is logged in
if "access_token" not in st.session_state:

    st.title("💰 Personal Expense Tracker")

    st.write("Welcome! Please log in or create an account.")

    login_tab, signup_tab = st.tabs(["Login", "Create Account"])

    # LOGIN SECTION
    with login_tab:

        st.subheader("Welcome Back")

        with st.form("login_form"):

            email = st.text_input("Email Address")

            password = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.form_submit_button("Login")

            if login_button:

                try:
                    response = sign_in(
                        supabase,
                        email,
                        password
                    )

                    session = response.session

                    if session:
                        st.session_state["access_token"] = session.access_token
                        st.session_state["refresh_token"] = session.refresh_token

                        st.success("Login successful!")
                        st.rerun()

                    else:
                        st.error("Login failed. Please try again.")

                except Exception as error:
                    st.error(f"Login failed: {error}")




        st.divider()

        st.write("Forgot your password?")

        with st.form("forgot_password_form"):

            reset_email = st.text_input(
                "Enter your registered email"
            )

            reset_button = st.form_submit_button(
                "Send Reset Link"
            )

            if reset_button:

                if not reset_email.strip():
                    st.error("Please enter your email address.")

                else:

                    try:
                        reset_password(
                            supabase,
                            reset_email.strip(),
                            "https://personal-expense-trackerr.streamlit.app/"
                        )

                        st.success(
                            "If an account exists for that email, "
                            "a password-reset email will be sent."
                        )

                    except Exception as error:
                        st.error(f"Password reset failed: {error}")


    # REGISTRATION SECTION
    with signup_tab:

        st.subheader("Create Your Account")

        with st.form("signup_form"):

            new_email = st.text_input("Email Address")

            new_password = st.text_input(
                "Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            signup_button = st.form_submit_button("Create Account")

            if signup_button:

                if not new_email.strip():
                    st.error("Please enter your email address.")

                elif len(new_password) < 8:
                    st.error("Password must contain at least 8 characters.")

                elif new_password != confirm_password:
                    st.error("Passwords do not match.")

                else:

                    try:
                        response = sign_up(
                            supabase,
                            new_email.strip(),
                            new_password
                        )

                        if response.session:
                            st.session_state["access_token"] = response.session.access_token
                            st.session_state["refresh_token"] = response.session.refresh_token

                            st.success("Account created successfully!")
                            st.rerun()

                        else:
                            st.success(
                                "Account created! Please check your email "
                                "to confirm your account before logging in."
                            )

                    except Exception as error:
                        st.error(f"Registration failed: {error}")

    st.stop()



# Logout section
with st.sidebar:

    st.success("You are logged in!")

    if st.button("Logout"):

        try:
            sign_out(supabase)

        finally:
            st.session_state.pop("access_token", None)
            st.session_state.pop("refresh_token", None)

            st.rerun()




# Restore the user's Supabase session after a rerun
if (
    "access_token" in st.session_state
    and "refresh_token" in st.session_state
):
    try:
        supabase.auth.set_session(
            st.session_state["access_token"],
            st.session_state["refresh_token"]
        )
    except Exception:
        st.session_state.pop("access_token", None)
        st.session_state.pop("refresh_token", None)




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

# Fetch transactions belonging to the logged-in user
def get_user_transactions():

    try:
        response = (
            supabase.table("transactions")
            .select("*")
            .order("transaction_date", desc=True)
            .order("id", desc=True)
            .execute()
        )

        return response.data or []

    except Exception as error:
        st.error(f"Database error: {error}")
        return []


# Get financial summary
def get_financial_summary():

    transactions = get_user_transactions()

    total_income = 0
    total_expenses = 0

    monthly_income = 0
    monthly_expenses = 0

    current_month = date.today().strftime("%Y-%m")

    for transaction in transactions:

        amount = float(transaction["amount"])

        transaction_type = transaction["transaction_type"]

        transaction_date = str(transaction["transaction_date"])

        if transaction_type == "income":
            total_income += amount

            if transaction_date.startswith(current_month):
                monthly_income += amount

        elif transaction_type == "expense":
            total_expenses += amount

            if transaction_date.startswith(current_month):
                monthly_expenses += amount

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": total_income - total_expenses,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "monthly_balance": monthly_income - monthly_expenses
    }


# Get expenses grouped by category
def get_expenses_by_category():

    transactions = get_user_transactions()

    category_totals = {}

    for transaction in transactions:

        if transaction["transaction_type"] == "expense":

            category = transaction["category"]

            amount = float(transaction["amount"])

            if category in category_totals:
                category_totals[category] += amount

            else:
                category_totals[category] = amount

    results = sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return results


# Save a new transaction
def save_transaction(
    transaction_type,
    category,
    amount,
    description,
    transaction_date
):

    try:

        supabase.table("transactions").insert({
            "transaction_type": transaction_type,
            "category": category,
            "amount": amount,
            "description": description,
            "transaction_date": transaction_date
        }).execute()

        return True

    except Exception as error:
        st.error(f"Could not save transaction: {error}")
        return False


# Get all transactions
def get_all_transactions():

    transactions = get_user_transactions()

    return [
        (
            transaction["id"],
            transaction["transaction_type"],
            transaction["category"],
            transaction["amount"],
            transaction["description"],
            transaction["transaction_date"]
        )
        for transaction in transactions
    ]





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
