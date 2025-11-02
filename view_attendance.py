import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

attendance_path = "attendance"

def open_attendance_file():
    """Open and display selected attendance CSV file."""
    try:
        file_path = filedialog.askopenfilename(
            initialdir=attendance_path,
            title="Select Attendance File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        df = pd.read_csv(file_path)
        for i in tree.get_children():
            tree.delete(i)

        for index, row in df.iterrows():
            tree.insert("", "end", values=(row["Name"], row["Time"]))

        messagebox.showinfo("Success", f"Loaded {os.path.basename(file_path)}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file:\n{e}")

def refresh_list():
    """Auto-load the latest attendance file."""
    try:
        files = [f for f in os.listdir(attendance_path) if f.endswith(".csv")]
        if not files:
            messagebox.showwarning("No Files", "No attendance records found.")
            return
        latest = max(files, key=lambda x: os.path.getctime(os.path.join(attendance_path, x)))
        file_path = os.path.join(attendance_path, latest)
        df = pd.read_csv(file_path)
        for i in tree.get_children():
            tree.delete(i)
        for index, row in df.iterrows():
            tree.insert("", "end", values=(row["Name"], row["Time"]))
        messagebox.showinfo("Loaded", f"Showing latest file: {latest}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file:\n{e}")

# ---------------- Tkinter GUI ----------------

root = tk.Tk()
root.title("View Attendance Records")
root.geometry("500x400")

tk.Label(root, text="Attendance Records", font=("Helvetica", 16, "bold")).pack(pady=10)

# Treeview (table)
frame = tk.Frame(root)
frame.pack(pady=10)

columns = ("Name", "Time")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
tree.heading("Name", text="Name")
tree.heading("Time", text="Time")
tree.pack(fill="both", expand=True)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Open Attendance File", width=20, command=open_attendance_file).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Load Latest", width=15, command=refresh_list).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Close", width=10, command=root.destroy).grid(row=0, column=2, padx=10)

root.mainloop()
