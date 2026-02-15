import hashlib
import sqlite3
import matplotlib.pyplot as plt

# ---------- Database Setup ----------
conn = sqlite3.connect("voting.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    voted INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS votes (
    candidate TEXT
)
""")

conn.commit()


# ---------- Helper Functions ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        cur.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (username, hash_password(password), 0)
        )
        conn.commit()
        print("Registration successful")
    except:
        print("User already exists")


def login_user():
    username = input("Username: ")
    password = input("Password: ")

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    user = cur.fetchone()
    if user:
        print("Login successful")
        return username
    else:
        print("Invalid credentials")
        return None


# ---------- Voting ----------
def vote(username):
    cur.execute("SELECT voted FROM users WHERE username=?", (username,))
    if cur.fetchone()[0] == 1:
        print("You have already voted")
        return

    print("\nCandidates:")
    print("1. Alice")
    print("2. Bob")
    print("3. Charlie")

    choice = input("Enter choice (1/2/3): ")
    candidates = {"1": "Alice", "2": "Bob", "3": "Charlie"}

    if choice in candidates:
        cur.execute("INSERT INTO votes VALUES (?)", (candidates[choice],))
        cur.execute("UPDATE users SET voted=1 WHERE username=?", (username,))
        conn.commit()
        print("Vote cast successfully")
    else:
        print("Invalid choice")


# ---------- Result Visualization ----------
def show_results():
    cur.execute("SELECT candidate FROM votes")
    data = cur.fetchall()

    if not data:
        print("No votes yet")
        return

    results = {}
    for vote in data:
        results[vote[0]] = results.get(vote[0], 0) + 1

    plt.bar(results.keys(), results.values())
    plt.xlabel("Candidates")
    plt.ylabel("Votes")
    plt.title("Voting Results")
    plt.show()


# ---------- Main Menu ----------
while True:
    print("\n--- Online Voting System ---")
    print("1. Register")
    print("2. Login")
    print("3. View Results")
    print("4. Exit")

    ch = input("Choose option: ")

    if ch == "1":
        register_user()

    elif ch == "2":
        user = login_user()
        if user:
            vote(user)

    elif ch == "3":
        show_results()

    elif ch == "4":
        break

    else:
        print("Invalid option")

conn.close()
