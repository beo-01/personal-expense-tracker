# Personal Expense Tracker

A command-line application built with Python and SQLite for managing personal income and expenses. It allows users to record transactions, monitor their spending, calculate their balance, and visualise financial activities using charts.

## Features

- Add income and expense transactions.
- View all recorded transactions.
- Search transactions by category, type, or date.
- Calculate total income, expenses, and available balance.
- View monthly financial summaries.
- Visualise expenses by category.
- Compare total income against expenses.
- Input validation and error handling.
- Persistent data storage using SQLite.

## Technologies Used

- Python
- SQLite
- Matplotlib

## Project Structure

```text
personal-expense-tracker/
│
├── main.py
├── database.py
├── transactions.py
├── reports.py
├── charts.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/beo-01/personal-expense-tracker.git
```

2. Navigate into the project folder:

```bash
cd personal-expense-tracker
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the virtual environment:

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
python main.py
```

## Database

The application uses SQLite to store transaction records. The database and its table are automatically created when the application starts.

## Future Improvements

- Add transaction editing and deletion.
- Add monthly and yearly spending reports.
- Develop a Streamlit web dashboard.
- Export financial reports to CSV.

## Author

**Bolaji Olatunji**

GitHub: [beo-01](https://github.com/beo-01)
