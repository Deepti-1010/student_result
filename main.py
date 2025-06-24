import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# DB Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="student_app",
        password="password123",
        database="student_db"
    )

# --- Core Functions ---

def add_student():
    roll = roll_var.get()
    name = name_var.get()
    dob = dob_var.get_date()
    dept = dept_var.get()
    if not (roll and name and dept):
        messagebox.showwarning("Input Error", "Missing fields!")
        return
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO students (roll_no, name, dob, department) VALUES (%s, %s, %s, %s)",
                    (roll, name, dob, dept))
        conn.commit()
        messagebox.showinfo("Success", f"Student {name} added.")
        load_students()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists.")
    finally:
        conn.close()

def add_result():
    sel = students_tree.selection()
    if not sel:
        messagebox.showwarning("Select", "Select student first.")
        return
    subject = subject_var.get()
    marks = marks_var.get()
    if not (subject and marks.isdigit()):
        messagebox.showwarning("Input Error", "Invalid subject or marks.")
        return
    sid = students_tree.item(sel[0], 'values')[0]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO results (student_id, subject, marks) VALUES (%s, %s, %s)",
                (sid, subject, int(marks)))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Result added.")
    load_results(sid)

def load_students():
    for row in students_tree.get_children():
        students_tree.delete(row)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT student_id, roll_no, name, DATE_FORMAT(dob, '%Y-%m-%d'), department FROM students")
    for row in cur.fetchall():
        students_tree.insert('', tk.END, values=row)
    conn.close()

def load_results(student_id):
    for row in results_tree.get_children():
        results_tree.delete(row)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT subject, marks FROM results WHERE student_id = %s", (student_id,))
    for row in cur.fetchall():
        results_tree.insert('', tk.END, values=row)
    conn.close()

def on_student_select(event):
    sel = students_tree.selection()
    if sel:
        sid = students_tree.item(sel[0], 'values')[0]
        load_results(sid)

# --- GUI Setup ---

root = tk.Tk()
root.title("Student Result Management System")
root.geometry("800x600")

# Student frame
frame1 = ttk.LabelFrame(root, text="Student Info")
frame1.pack(fill="x", padx=10, pady=5)

roll_var = tk.StringVar()
name_var = tk.StringVar()
dob_var = DateEntry(frame1, width=12)
dept_var = tk.StringVar()
subject_var = tk.StringVar()
marks_var = tk.StringVar()

ttk.Label(frame1, text="Roll No:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(frame1, textvariable=roll_var).grid(row=0, column=1, padx=5)
ttk.Label(frame1, text="Name:").grid(row=0, column=2)
ttk.Entry(frame1, textvariable=name_var).grid(row=0, column=3)
ttk.Label(frame1, text="DOB:").grid(row=0, column=4)
dob_var.grid(row=0, column=5)
ttk.Label(frame1, text="Dept:").grid(row=1, column=0)
ttk.Entry(frame1, textvariable=dept_var).grid(row=1, column=1)
ttk.Button(frame1, text="Add Student", command=add_student).grid(row=1, column=3, pady=5)

# Students list
frame2 = ttk.Frame(root)
frame2.pack(fill="both", expand=True, padx=10, pady=5)

students_tree = ttk.Treeview(frame2, columns=("ID","Roll","Name","DOB","Dept"), show="headings")
for col in students_tree["columns"]:
    students_tree.heading(col, text=col)
students_tree.pack(side="left", fill="both", expand=True)
students_tree.bind("<<TreeviewSelect>>", on_student_select)

# Results section
frame3 = ttk.LabelFrame(root, text="Add/Show Results")
frame3.pack(fill="x", padx=10, pady=5)

ttk.Label(frame3, text="Subject:").grid(row=0, column=0, padx=5)
ttk.Entry(frame3, textvariable=subject_var).grid(row=0, column=1)
ttk.Label(frame3, text="Marks:").grid(row=0, column=2)
ttk.Entry(frame3, textvariable=marks_var).grid(row=0, column=3)
ttk.Button(frame3, text="Add Result", command=add_result).grid(row=0, column=4)

results_tree = ttk.Treeview(frame3, columns=("Subject","Marks"), show="headings")
results_tree.heading("Subject", text="Subject")
results_tree.heading("Marks", text="Marks")
results_tree.grid(row=1, column=0, columnspan=5, pady=5)

load_students()
root.mainloop()
