from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ==========================
# Database Connection
# ==========================

def get_connection():
    return sqlite3.connect("payroll.db")


# ==========================
# Home Page
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Login Page
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        return f"Welcome {username}"

    return render_template("login.html")


# ==========================
# Add Employee
# ==========================

@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO Employees (
            full_name,
            cnic,
            email,
            phone,
            department,
            designation,
            joining_date,
            basic_salary,
            bank_account
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["full_name"],
            request.form["cnic"],
            request.form["email"],
            request.form["phone"],
            request.form["department"],
            request.form["designation"],
            request.form["joining_date"],
            request.form["basic_salary"],
            request.form["bank_account"]
        ))

        conn.commit()
        conn.close()

        return "Employee Added Successfully"

    return render_template("add_employee.html")


# ==========================
# Employee List
# ==========================

@app.route("/employees")
def employee_list():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()

    conn.close()

    return render_template(
        "employee_list.html",
        employees=employees
    )


# ==========================
# Add Department
# ==========================

@app.route("/add_department", methods=["GET", "POST"])
def add_department():

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Departments(department_name) VALUES (?)",
            (request.form["department_name"],)
        )

        conn.commit()
        conn.close()

        return "Department Added Successfully"

    return render_template("add_department.html")


# ==========================
# Department List
# ==========================

@app.route("/departments")
def department_list():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Departments")
    departments = cursor.fetchall()

    conn.close()

    return render_template(
        "department_list.html",
        departments=departments
    )


# ==========================
# Add Attendance
# ==========================

@app.route("/add_attendance", methods=["GET", "POST"])
def add_attendance():

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO Attendance (
            employee_id,
            date,
            check_in_time,
            check_out_time,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            request.form["employee_id"],
            request.form["date"],
            request.form["check_in_time"],
            request.form["check_out_time"],
            request.form["status"]
        ))

        conn.commit()
        conn.close()

        return "Attendance Added Successfully"

    return render_template("add_attendance.html")


# ==========================
# Attendance List
# ==========================

@app.route("/attendance")
def attendance_list():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Attendance")
    attendance_records = cursor.fetchall()

    conn.close()

    return render_template(
        "attendance_list.html",
        attendance_records=attendance_records
    )


# ==========================
# Add Salary Structure
# ==========================

@app.route("/add_salary_structure", methods=["GET", "POST"])
def add_salary_structure():

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO SalaryStructure (
            employee_id,
            basic_salary,
            house_allowance,
            medical_allowance,
            transport_allowance,
            tax,
            loan_deduction,
            other_deduction
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["employee_id"],
            request.form["basic_salary"],
            request.form["house_allowance"],
            request.form["medical_allowance"],
            request.form["transport_allowance"],
            request.form["tax"],
            request.form["loan_deduction"],
            request.form["other_deduction"]
        ))

        conn.commit()
        conn.close()

        return "Salary Structure Added Successfully"

    return render_template("add_salary_structure.html")


# ==========================
# Salary Structure List
# ==========================

@app.route("/salary_structures")
def salary_structures():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM SalaryStructure")
    records = cursor.fetchall()

    conn.close()

    return render_template(
        "salary_structure_list.html",
        records=records
    )


# ==========================
# Generate Payroll
# ==========================

@app.route("/generate_payroll")
def generate_payroll():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        employee_id,
        basic_salary,
        house_allowance,
        medical_allowance,
        transport_allowance,
        tax,
        loan_deduction,
        other_deduction
    FROM SalaryStructure
    """)

    records = cursor.fetchall()

    payroll_data = []

    for row in records:

        gross_salary = (
            float(row[1]) +
            float(row[2]) +
            float(row[3]) +
            float(row[4])
        )

        total_deductions = (
            float(row[5]) +
            float(row[6]) +
            float(row[7])
        )

        net_salary = gross_salary - total_deductions

        payroll_data.append(
            (
                row[0],
                gross_salary,
                total_deductions,
                net_salary
            )
        )

    conn.close()

    return render_template(
        "payroll_list.html",
        payroll_data=payroll_data
    )

@app.route("/payslip/<employee_id>")
def payslip(employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        employee_id,
        basic_salary,
        house_allowance,
        medical_allowance,
        transport_allowance,
        tax,
        loan_deduction,
        other_deduction
    FROM SalaryStructure
    WHERE employee_id = ?
    """, (employee_id,))

    record = cursor.fetchone()

    conn.close()

    if not record:
        return "Payslip Not Found"

    gross_salary = (
        float(record[1]) +
        float(record[2]) +
        float(record[3]) +
        float(record[4])
    )

    deductions = (
        float(record[5]) +
        float(record[6]) +
        float(record[7])
    )

    net_salary = gross_salary - deductions

    return render_template(
        "payslip.html",
        record=record,
        gross_salary=gross_salary,
        deductions=deductions,
        net_salary=net_salary
    )

@app.route("/payroll_report")
def payroll_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT employee_id,
           basic_salary,
           house_allowance,
           medical_allowance,
           transport_allowance
    FROM SalaryStructure
    """)

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "payroll_report.html",
        records=records
    )

@app.route("/profile")
def profile():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Employees LIMIT 1")
    employee = cursor.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        employee=employee
    )


if __name__ == "__main__":
    app.run(debug=True)