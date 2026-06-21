import sqlite3

conn = sqlite3.connect("payroll.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS SalaryStructure(
    structure_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    basic_salary REAL,
    house_allowance REAL,
    medical_allowance REAL,
    transport_allowance REAL,
    tax REAL,
    loan_deduction REAL,
    other_deduction REAL
)
""")

conn.commit()
conn.close()

print("SalaryStructure Table Created Successfully")