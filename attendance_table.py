import sqlite3

conn = sqlite3.connect("payroll.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Attendance(
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    date TEXT,
    check_in_time TEXT,
    check_out_time TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Attendance Table Created Successfully")