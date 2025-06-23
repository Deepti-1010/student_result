import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class StudentApp:
    def __init__(self, root):
        self.db = Database()
        self.db.setup()
        self.root = root
        root.title("Student Result Management")
        root.geometry("800x500")

        # Left: Student List
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(left_frame, text="Students").pack()
        self.student_list = tk.Listbox(left_frame, height=20, width=25)
        self.student_list.pack()
        self.student_list.bind("<<ListboxSelect>>", self.on_student_select)

        tk.Button(left_frame, text="Add Student", command=self.add_student).pack(pady=5)
        tk.Button(left_frame, text="Edit Student", command=self.edit_student).pack(pady=5)
        tk.Button(left_frame, text="Delete Student", command=self.delete_student).pack(pady=5)

        # Right: Results + Entry
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(right_frame, text="Results").grid(row=0, column=0, columnspan=3)
        self.tree = ttk.Treeview(right_frame, columns=("Subject", "Marks"), show="headings")
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Marks", text="Marks")
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew")

        tk.Label(right_frame, text="Subject").grid(row=2, column=0)
        self.subject_entry = tk.Entry(right_frame)
        self.subject_entry.grid(row=2, column=1)

        tk.Label(right_frame, text="Marks").grid(row=3, column=0)
        self.marks_entry = tk.Entry(right_frame)
        self.marks_entry.grid(row=3, column=1)

        tk.Button(right_frame, text="Add Result", command=self.add_result).grid(row=4, column=0, columnspan=2, pady=5)

        # Load initial data
        self.load_students()

    def load_students(self):
        self.student_list.delete(0, tk.END)
        for s in self.db.get_students():
            self.student_list.insert(tk.END, f"{s['id']}: {s['name']}")

    def on_student_select(self, _):
        selection = self.student_list.curselection()
        if not selection:
            return
        idx = selection[0]
        student_str = self.student_list.get(idx)
        student_id = int(student_str.split(":")[0])
        self.load_results(student_id)

    def load_results(self, student_id):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for res in self.db.get_results(student_id):
            self.tree.insert("", tk.END, values=(res["subject"], res["marks"]))

    def add_student(self):
        name = tk.simpledialog.askstring("Add Student", "Enter student name:")
        if name:
            self.db.add_student(name)
            self.load_students()

    def edit_student(self):
        sel = self.student_list.curselection()
        if not sel:
            messagebox.showwarning("Select", "Please select a student")
            return
        idx = sel[0]
        st_str = self.student_list.get(idx)
        sid, old = st_str.split(": ",1)
        new = tk.simpledialog.askstring("Edit Student", "New name:", initialvalue=old)
        if new:
            self.db.update_student(int(sid), new)
            self.load_students()

    def delete_student(self):
        sel = self.student_list.curselection()
        if not sel:
            messagebox.showwarning("Select", "Please select a student")
            return
        idx = sel[0]
        sid = int(self.student_list.get(idx).split(":")[0])
        if messagebox.askyesno("Confirm", "Delete this student and all results?"):
            self.db.delete_student(sid)
            self.load_students()
            for r in self.tree.get_children():
                self.tree.delete(r)

    def add_result(self):
        sel = self.student_list.curselection()
        if not sel:
            messagebox.showwarning("Select", "Please select a student")
            return
        sid = int(self.student_list.get(sel[0]).split(":")[0])
        subj = self.subject_entry.get().strip()
        marks = self.marks_entry.get().strip()
        if not subj or not marks.isdigit():
            messagebox.showwarning("Input Error", "Please enter valid subject and numeric marks.")
            return
        self.db.add_result(sid, subj, int(marks))
        self.subject_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)
        self.load_results(sid)
