import sqlite3

conn = sqlite3.connect("payroll.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Payroll(
    payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    gross_salary REAL,
    total_deductions REAL,
    net_salary REAL
)
""")

conn.commit()
conn.close()

print("Payroll Table Created Successfully")