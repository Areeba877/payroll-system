import sqlite3
import bcrypt

def register_user(username, password, role):

    conn = sqlite3.connect("payroll.db")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute("""
    INSERT INTO Users(username,password,role)
    VALUES(?,?,?)
    """, (
        username,
        hashed_password,
        role
    ))

    conn.commit()
    conn.close()

def login_user(username, password):

    conn = sqlite3.connect("payroll.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT password, role
    FROM Users
    WHERE username=?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    if user:

        if bcrypt.checkpw(
            password.encode(),
            user[0].encode()
        ):
            return user[1]

    return None