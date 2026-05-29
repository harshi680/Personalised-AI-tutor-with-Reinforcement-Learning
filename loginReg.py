import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from sessionCSV import save_session,load_session
# ---------------- Database Config ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'student_exam_ml',
    'charset': 'utf8',
    'port': '3308'
}

# ---------------- Database Connection ----------------
def create_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# ---------------- Registration ----------------
def register_student():
    name = reg_name_entry.get().strip()
    class_name = reg_class_entry.get().strip()
    regno = reg_regno_entry.get().strip()
    email = reg_email_entry.get().strip()
    password = reg_password_entry.get().strip()

    if not (name and class_name and regno and email and password):
        messagebox.showwarning("⚠️ Input Error", "All fields are required!")
        return

    conn = create_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO students (name, class, regno, email, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, class_name, regno, email, password))
            conn.commit()
            messagebox.showinfo("✅ Success", "Student registered successfully!")
            reg_name_entry.delete(0, tk.END)
            reg_class_entry.delete(0, tk.END)
            reg_regno_entry.delete(0, tk.END)
            reg_email_entry.delete(0, tk.END)
            reg_password_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            if err.errno == 1062:
                messagebox.showerror("❌ Error", "Email or RegNo already exists!")
            else:
                messagebox.showerror("❌ Error", f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()

# ---------------- Login ----------------
def login_student():
    email = login_email_entry.get().strip()
    password = login_password_entry.get().strip()

    if not (email and password):
        messagebox.showwarning("⚠️ Input Error", "Email & Password are required!")
        return

    conn = create_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT name, class FROM students WHERE email = %s AND password = %s", (email, password))
            student = cursor.fetchone()
            if student:
                messagebox.showinfo("🎉 Welcome", f"Hello {student['name']}! 🚀")
                login_email_entry.delete(0, tk.END)
                login_password_entry.delete(0, tk.END)
                root.withdraw()
                python_path = sys.executable
                #-session -------
                session = load_session()
                key = "email"
                value = email
                session[key] = value
                save_session(session)
                for key, value in session.items():
                    print(f"  {key}: {value}")
                #session ends----------
                subprocess.Popen([python_path, "main2.py"])
                subprocess.Popen([python_path, "facetrackingNew.py"])
            else:
                messagebox.showerror("❌ Login Failed", "Invalid email or password.")
        finally:
            cursor.close()
            conn.close()

# ---------------- Tkinter Window ----------------
root = tk.Tk()
root.title("🎓 Student Exam Portal")
root.geometry("800x720")
root.resizable(False, False)

# Gradient Background
canvas = tk.Canvas(root, width=800, height=720)
canvas.pack(fill="both", expand=True)

# Custom gradient creation
def create_gradient(canvas, color1, color2):
    for i in range(0, 720):
        r = i / 720
        color = f"#{int((1-r)*int(color1[1:3],16) + r*int(color2[1:3],16)):02x}" \
                f"{int((1-r)*int(color1[3:5],16) + r*int(color2[3:5],16)):02x}" \
                f"{int((1-r)*int(color1[5:],16) + r*int(color2[5:],16)):02x}"
        canvas.create_line(0, i, 800, i, fill=color)

create_gradient(canvas, "#89CFF0", "#FFDEE9")  # Light blue to pink

# ---------------- Styling ----------------
style = ttk.Style()
style.theme_use('clam')

style.configure("TLabel", font=("Arial", 12), background="#FFFFFF", padding=5)
style.configure("Header.TLabel", font=("Arial", 24, "bold"), background="#FFFFFF", foreground="#ff4081")
style.configure("TButton",
                font=("Arial", 12, "bold"),
                padding=8,
                background="#4CAF50",
                foreground="white",
                borderwidth=0)
style.map("TButton", background=[("active", "#3e8e41")])

# ---------------- Main Frame (With Shadow) ----------------
main_frame = tk.Frame(canvas, bg="darkblue", bd=2, relief="ridge")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=650, height=650)

ttk.Label(main_frame, text="🎓 Student Exam Portal", style="Header.TLabel").pack(pady=20)

# ---------------- Registration Box ----------------
reg_frame = ttk.LabelFrame(main_frame, text="📋 Register", padding=20)
reg_frame.pack(pady=15, fill="x", padx=20)

ttk.Label(reg_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
reg_name_entry = ttk.Entry(reg_frame, width=30)
reg_name_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(reg_frame, text="Class:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
reg_class_entry = ttk.Entry(reg_frame, width=30)
reg_class_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(reg_frame, text="Reg No:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
reg_regno_entry = ttk.Entry(reg_frame, width=30)
reg_regno_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(reg_frame, text="Email:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
reg_email_entry = ttk.Entry(reg_frame, width=30)
reg_email_entry.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(reg_frame, text="Password:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
reg_password_entry = ttk.Entry(reg_frame, width=30, show="*")
reg_password_entry.grid(row=4, column=1, padx=10, pady=5)

ttk.Button(reg_frame, text="✅ Register", command=register_student).grid(row=5, columnspan=2, pady=10)

# ---------------- Login Box ----------------
login_frame = ttk.LabelFrame(main_frame, text="🔑 Login", padding=20)
login_frame.pack(pady=15, fill="x", padx=20)

ttk.Label(login_frame, text="Email:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
login_email_entry = ttk.Entry(login_frame, width=30)
login_email_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
login_password_entry = ttk.Entry(login_frame, width=30, show="*")
login_password_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Button(login_frame, text="🚀 Login", command=login_student).grid(row=2, columnspan=2, pady=10)

root.mainloop()
