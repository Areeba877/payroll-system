import sqlite3

def create_database():

    conn = sqlite3.connect("payroll.db")

    print("Database Created Successfully")

    conn.close()

create_database()