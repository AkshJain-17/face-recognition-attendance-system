import pandas as pd
import os

USERS_FILE = "users.csv"

# ------------------ Initialize Admin File ------------------
def init_users():
    """
    Create users.csv if missing or empty, and add a default admin account.
    """
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["username", "password", "security_question", "security_answer"])
        df.to_csv(USERS_FILE, index=False)

    users = pd.read_csv(USERS_FILE)
    if users.empty:
        print("⚙️ No admin found. Creating default admin account (admin/admin123)")
        df = pd.DataFrame([{
            "username": "admin",
            "password": "admin123",
            "security_question": "What is your favorite color?",
            "security_answer": "blue"
        }])
        df.to_csv(USERS_FILE, index=False)
    else:
        # Ensure all expected columns exist
        required_cols = ["username", "password", "security_question", "security_answer"]
        for col in required_cols:
            if col not in users.columns:
                users[col] = ""
        users.to_csv(USERS_FILE, index=False)

# ------------------ Verify Login ------------------
def verify_login(username, password):
    """
    Verify credentials from CSV. Automatically trims whitespace.
    """
    users = pd.read_csv(USERS_FILE)
    # Convert everything to string and trim spaces/newlines
    users = users.astype(str).apply(lambda x: x.str.strip())
    username = str(username).strip()
    password = str(password).strip()
    
    user = users[(users["username"] == username) & (users["password"] == password)]
    return not user.empty

# ------------------ Add New Admin ------------------
def add_user(username, password, security_question, security_answer):
    users = pd.read_csv(USERS_FILE)
    users = users.astype(str).apply(lambda x: x.str.strip())

    if username in users["username"].values:
        return False

    new_user = pd.DataFrame({
        "username": [username.strip()],
        "password": [password.strip()],
        "security_question": [security_question.strip()],
        "security_answer": [security_answer.strip()]
    })
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USERS_FILE, index=False)
    return True

# ------------------ Change Password ------------------
def change_password(username, old_password, new_password):
    users = pd.read_csv(USERS_FILE)
    users = users.astype(str).apply(lambda x: x.str.strip())
    username = username.strip()
    old_password = old_password.strip()

    match = (users["username"] == username) & (users["password"] == old_password)
    if match.any():
        users["password"] = users["password"].astype(str)
        users.loc[match, "password"] = str(new_password).strip()
        users.to_csv(USERS_FILE, index=False)
        return True
    return False

# ------------------ Forgot Password ------------------
def get_security_question(username):
    users = pd.read_csv(USERS_FILE)
    users = users.astype(str).apply(lambda x: x.str.strip())
    user = users[users["username"] == str(username).strip()]
    if not user.empty:
        return user.iloc[0]["security_question"]
    return None

def reset_password_if_correct(username, answer):
    users = pd.read_csv(USERS_FILE)
    users = users.astype(str).apply(lambda x: x.str.strip())
    user = users[users["username"] == str(username).strip()]
    if user.empty:
        return False

    if str(user.iloc[0]["security_answer"]).lower() == str(answer).strip().lower():
        new_pass = input("Enter new password: ")
        users["password"] = users["password"].astype(str)
        users.loc[users["username"] == username, "password"] = str(new_pass).strip()
        users.to_csv(USERS_FILE, index=False)
        return True
    else:
        return False

# ------------------ Initialize on Import ------------------
init_users()
