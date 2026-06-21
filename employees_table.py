import sqlite3

conn = sqlite3.connect("payroll.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (

    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL,
    cnic TEXT NOT NULL,

    email TEXT NOT NULL,

    phone TEXT,

    department TEXT,

    designation TEXT,

    joining_date TEXT,

    basic_salary REAL,

    bank_account TEXT
)
""")

conn.commit()
conn.close()

print("Employees Table Created Successfully")