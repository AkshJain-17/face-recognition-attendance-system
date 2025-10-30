import tkinter as tk
from tkinter import messagebox
import pandas as pd
import subprocess
import os

USERS_FILE = "users.csv"

# Create users file if missing
if not os.path.exists(USERS_FILE):
    df = pd.DataFrame(columns=["username", "password", "security_question", "security_answer"])
    df.to_csv(USERS_FILE, index=False)

# ---------------------- Utility Functions ----------------------
def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame(columns=["username", "password", "security_question", "security_answer"])

def save_users(df):
    df.to_csv(USERS_FILE, index=False)

def open_main_gui(username):
    root = tk.Tk()
    root.title("Face Recognition Attendance System")

    # Example welcome label
    tk.Label(root, text=f"Welcome, {username}!", font=("Arial", 16, "bold")).pack(pady=20)

    # Buttons for main functions
    tk.Button(root, text="📷 Take Attendance", width=20, command=lambda: messagebox.showinfo("Feature", "Attendance feature here")).pack(pady=10)
    tk.Button(root, text="🧠 Train Model", width=20, command=lambda: messagebox.showinfo("Feature", "Model training feature here")).pack(pady=10)
    tk.Button(root, text="🗂️ Manage Students", width=20, command=lambda: messagebox.showinfo("Feature", "Manage students here")).pack(pady=10)
    tk.Button(root, text="🚪 Logout", width=20, command=root.destroy).pack(pady=10)

    root.mainloop()

# ---------------------- Main Application ----------------------
class FaceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition Attendance System")
        self.geometry("420x380")
        self.config(bg="#222")

        self.active_frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.active_frame is not None:
            self.active_frame.destroy()
        self.active_frame = new_frame
        self.active_frame.pack(fill="both", expand=True)

# ---------------------- Login Frame ----------------------
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#222")

        tk.Label(self, text="Login", font=("Arial", 18, "bold"), fg="#fff", bg="#222").pack(pady=20)

        self.username = tk.Entry(self, font=("Arial", 12))
        self.username.pack(pady=8)
        self.username.insert(0, "Username")

        self.password = tk.Entry(self, show="*", font=("Arial", 12))
        self.password.pack(pady=8)
        self.password.insert(0, "Password")

        tk.Button(self, text="Login", font=("Arial", 12, "bold"), bg="#28a745", fg="#fff",
                  command=self.login_user).pack(pady=10)
        tk.Button(self, text="Create New User", font=("Arial", 10), bg="#007bff", fg="#fff",
                  command=lambda: master.switch_frame(RegisterFrame)).pack(pady=5)
        tk.Button(self, text="Forgot Password?", font=("Arial", 10), bg="#ffc107", fg="#000",
                  command=lambda: master.switch_frame(ForgotFrame)).pack(pady=5)

    def login_user(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        df = load_users()

        if username in df["username"].values:
            stored_pass = df.loc[df["username"] == username, "password"].values[0]
            if stored_pass == password:
                messagebox.showinfo("Success", f"Welcome {username}!")
                subprocess.Popen(["python", "app.py", username])
            else:
                messagebox.showerror("Error", "Incorrect password!")
        else:
            messagebox.showerror("Error", "User not found!")

# ---------------------- Register Frame ----------------------
class RegisterFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#222")

        tk.Label(self, text="Register New User", font=("Arial", 18, "bold"), fg="#fff", bg="#222").pack(pady=20)

        self.username = tk.Entry(self, font=("Arial", 12))
        self.username.pack(pady=8)
        self.username.insert(0, "New Username")

        self.password = tk.Entry(self, show="*", font=("Arial", 12))
        self.password.pack(pady=8)
        self.password.insert(0, "New Password")

        self.question = tk.Entry(self, font=("Arial", 12))
        self.question.pack(pady=8)
        self.question.insert(0, "Security Question")

        self.answer = tk.Entry(self, font=("Arial", 12))
        self.answer.pack(pady=8)
        self.answer.insert(0, "Answer")

        tk.Button(self, text="Register", font=("Arial", 12, "bold"), bg="#28a745", fg="#fff",
                  command=self.register_user).pack(pady=10)
        tk.Button(self, text="Back to Login", font=("Arial", 10), bg="#007bff", fg="#fff",
                  command=lambda: master.switch_frame(LoginFrame)).pack(pady=5)

    def register_user(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        question = self.question.get().strip()
        answer = self.answer.get().strip()

        if not (username and password and question and answer):
            messagebox.showerror("Error", "All fields are required!")
            return

        df = load_users()
        if username in df["username"].values:
            messagebox.showerror("Error", "Username already exists!")
            return

        new_user = pd.DataFrame([[username, password, question, answer]],
                                columns=["username", "password", "security_question", "security_answer"])
        df = pd.concat([df, new_user], ignore_index=True)
        save_users(df)
        messagebox.showinfo("Success", "User registered successfully!")
        self.master.switch_frame(LoginFrame)

# ---------------------- Forgot Password Frame ----------------------
class ForgotFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#222")

        tk.Label(self, text="Forgot Password", font=("Arial", 18, "bold"), fg="#fff", bg="#222").pack(pady=20)

        self.username = tk.Entry(self, font=("Arial", 12))
        self.username.pack(pady=8)
        self.username.insert(0, "Enter Username")

        self.answer = tk.Entry(self, font=("Arial", 12))
        self.answer.pack(pady=8)
        self.answer.insert(0, "Security Answer")

        self.new_password = tk.Entry(self, show="*", font=("Arial", 12))
        self.new_password.pack(pady=8)
        self.new_password.insert(0, "New Password")

        tk.Button(self, text="Reset Password", font=("Arial", 12, "bold"), bg="#28a745", fg="#fff",
                  command=self.reset_password).pack(pady=10)
        tk.Button(self, text="Back to Login", font=("Arial", 10), bg="#007bff", fg="#fff",
                  command=lambda: master.switch_frame(LoginFrame)).pack(pady=5)

    def reset_password(self):
        username = self.username.get().strip()
        answer = self.answer.get().strip()
        new_pass = self.new_password.get().strip()

        df = load_users()

        if username not in df["username"].values:
            messagebox.showerror("Error", "User not found!")
            return

        stored_answer = df.loc[df["username"] == username, "security_answer"].values[0]
        if stored_answer != answer:
            messagebox.showerror("Error", "Incorrect security answer!")
            return

        df.loc[df["username"] == username, "password"] = new_pass
        save_users(df)
        messagebox.showinfo("Success", "Password reset successfully!")
        self.master.switch_frame(LoginFrame)

# ---------------------- Run App ----------------------
if __name__ == "__main__":
    app = FaceApp()
    app.mainloop()
