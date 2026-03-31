import sqlite3

# Connect DB (creates file automatically)
conn = sqlite3.connect('finance.db', check_same_thread=False)
cursor = conn.cursor()

# -------------------------
# Create Users Table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

# -------------------------
# Create History Table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    username TEXT,
    income REAL,
    expense REAL,
    savings REAL,
    debt REAL,
    investment REAL,
    target_amount REAL,
    result TEXT
)
""")

conn.commit()


# -------------------------
# Functions
# -------------------------
def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False


def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchone()


def save_history(username, user_input, result):
    cursor.execute("""
        INSERT INTO history VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        user_input['income'],
        user_input['expense'],
        user_input['savings'],
        user_input['debt'],
        user_input['investment'],
        user_input['target_amount'],
        str(result)
    ))
    conn.commit()


def get_history(username):
    cursor.execute("SELECT * FROM history WHERE username=?", (username,))
    return cursor.fetchall()