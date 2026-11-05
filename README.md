# Personal Expense Tracker

A Python-based personal finance application that helps users record income and expenses, monitor their financial balance, and visualize spending patterns. The project includes a command-line interface (CLI) and an interactive web dashboard built with Streamlit.

## Features

### CLI Application
- Add income and expense transactions.
- View all recorded transactions.
- Search transactions.
- View financial summaries.
- Generate expense category charts.
- Compare income and expenses.

### Streamlit Dashboard
- View total income, expenses, and balance.
- Monitor current-month financial activity.
- Visualize expenses by category.
- Compare income and expenses using charts.
- Add new transactions through a web form.
- View and filter transaction history.
- Display transaction amounts in Nigerian Naira.

## Technologies Used

- Python
- SQLite
- Streamlit
- Matplotlib

## Project Structure

```text
personal-expense-tracker/
│
├── app.py
├── main.py
├── database.py
├── transactions.py
├── reports.py
├── charts.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/beo-01/personal-expense-tracker.git
```

2. Navigate into the project folder:

```bash
cd personal-expense-tracker
```

3. Create and activate a virtual environment:

```bash
python -m venv .expense_env
```

Windows PowerShell:

```powershell
.\.expense_env\Scripts\Activate.ps1
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Run the CLI version

```bash
python main.py
```

### Run the Streamlit dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

## Database

The application uses SQLite to store transaction records. The database is created locally when the database setup is run. The database file is excluded from Git tracking.

## Author

**Bolaji Olatunji**

GitHub: [beo-01](https://github.com/beo-01)
