import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import re
import random
import os

# Tumhara database name
DB_NAME = "university_lms.db"

# Purani DB delete mat karo (tumhara data safe rahega)
# Comment kar diya yeh part

def get_conn():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
        FullName TEXT NOT NULL,
        UniversityID TEXT NOT NULL UNIQUE,
        Email TEXT NOT NULL UNIQUE,
        Gender TEXT NOT NULL,
        Age INTEGER,
        Phone TEXT,
        CNIC TEXT UNIQUE,
        Address TEXT,
        EnrollmentDate TEXT
    )
    ''')
    conn.commit()
    conn.close()

# ====================== STYLISH LOGIN WITH MATH CAPTCHA + SKIP BUTTON ======================
def show_login():
    login_window = tk.Tk()
    login_window.title("Admin Login - University LMS")
    login_window.geometry("450x680")
    login_window.configure(bg="#1e272e")
    login_window.resizable(False, False)

    # Center the window
    login_window.eval('tk::PlaceWindow . center')

    main_frame = tk.Frame(login_window, bg="#1e272e")
    main_frame.pack(expand=True, pady=30)

    # Title & Logo
    tk.Label(main_frame, text="🎓", font=("Arial", 60), bg="#1e272e", fg="#00d2d3").pack(pady=(0,10))
    tk.Label(main_frame, text="University LMS", font=("Arial", 28, "bold"), fg="#00d2d3", bg="#1e272e").pack()
    tk.Label(main_frame, text="Admin Portal", font=("Arial", 16), fg="#dcdde1", bg="#1e272e").pack(pady=(0,30))

    # Username
    tk.Label(main_frame, text="👤 Username", font=("Arial", 12, "bold"), fg="#f5f6fa", bg="#1e272e").pack(anchor="w", padx=60)
    username_entry = tk.Entry(main_frame, font=("Arial", 12), width=35, justify="center", relief="solid", bd=1)
    username_entry.pack(pady=8, padx=60)

    # Password
    tk.Label(main_frame, text="🔒 Password", font=("Arial", 12, "bold"), fg="#f5f6fa", bg="#1e272e").pack(anchor="w", padx=60, pady=(20,0))
    password_entry = tk.Entry(main_frame, font=("Arial", 12), width=35, justify="center", show="●", relief="solid", bd=1)
    password_entry.pack(pady=8, padx=60)

    # Advanced reCAPTCHA - Math Question
    captcha_frame = tk.Frame(main_frame, bg="#2f3640", relief="raised", bd=3)
    captcha_frame.pack(pady=30, padx=50, fill="x")

    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    answer = num1 + num2

    tk.Label(captcha_frame, text="🤖 I'm not a robot", font=("Arial", 12, "bold"), fg="#00d2d3", bg="#2f3640").pack(pady=10)
    tk.Label(captcha_frame, text=f"Solve: {num1} + {num2} = ?", font=("Arial", 14), fg="white", bg="#2f3640").pack(pady=5)
    captcha_entry = tk.Entry(captcha_frame, font=("Arial", 12), width=10, justify="center")
    captcha_entry.pack(pady=10)

    # Login Function
    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        user_answer = captcha_entry.get().strip()

        if not username or not password:
            messagebox.showerror("⚠️ Error", "Username aur Password daalo!")
            return

        if not user_answer.isdigit() or int(user_answer) != answer:
            messagebox.showerror("❌ reCAPTCHA Failed", "Math question galat hai! Dobara try karo.")
            login_window.destroy()
            show_login()  # New question ke saath restart
            return

        if username == "Farooq" and password == "farooq123":
            login_window.destroy()
            start_main_app(username)
        else:
            messagebox.showerror("🚫 Access Denied", "Galat credentials!")

    # Skip Login Function
    def skip_to_main():
        login_window.destroy()
        start_main_app("Guest")

    # Buttons
    tk.Button(main_frame, text="LOGIN SECURELY", font=("Arial", 14, "bold"), bg="#00d2d3", fg="#1e272e",
              cursor="hand2", relief="flat", padx=20, pady=10, command=attempt_login).pack(pady=20)

    tk.Button(main_frame, text="⏭️ Skip Login (Guest Mode)", font=("Arial", 12), bg="#576574", fg="white",
              cursor="hand2", relief="flat", padx=20, pady=8, command=skip_to_main).pack(pady=10)

    # Footer
    tk.Label(login_window, text="© 2026 University Management System | Secured Login", 
             font=("Arial", 9), fg="#576574", bg="#1e272e").pack(side="bottom", pady=15)

    login_window.mainloop()

# ====================== MAIN APP ======================
def start_main_app(admin_name):
    root = tk.Tk()
    app = UniversityApp(root, admin_name)
    root.mainloop()

class UniversityApp:
    def __init__(self, root, admin_name):
        self.root = root
        self.root.title("University Student Management System")
        self.root.geometry("1500x850")
        self.root.configure(bg="#f0f2f5")

        create_table()  # Agar table nahi hai toh banayega
        self.admin_name = admin_name
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Modern Header
        header = tk.Frame(self.root, bg="#341f97", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🎓 University LMS", font=("Arial", 28, "bold"), fg="white", bg="#341f97").pack(side="left", padx=30, pady=15)
        tk.Label(header, text=f"Welcome, {self.admin_name} 👋", font=("Arial", 16), fg="#dfe4ea", bg="#341f97").pack(side="right", padx=40, pady=20)

        # Main container
        container = tk.Frame(self.root, bg="#f0f2f5")
        container.pack(fill="both", expand=True, padx=25, pady=25)

        # Left - Form
        form_frame = tk.LabelFrame(container, text=" 📝 Student Registration / Edit ", 
                                   font=("Arial", 16, "bold"), padx=25, pady=25, bg="white", fg="#341f97", relief="solid", bd=2)
        form_frame.grid(row=0, column=0, sticky="ns", padx=(0, 25))

        self.entries = {}
        fields = [
            ("Full Name*", "FullName"),
            ("University ID*", "UniversityID"),
            ("Email*", "Email"),
            ("Age", "Age"),
            ("Phone (11 digits)", "Phone"),
            ("CNIC (13 digits)", "CNIC")
        ]

        for i, (label_text, key) in enumerate(fields):
            tk.Label(form_frame, text=label_text + ":", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").grid(
                row=i, column=0, sticky="e", pady=12, padx=10)
            entry = tk.Entry(form_frame, width=42, font=("Arial", 12), relief="solid", bd=1)
            entry.grid(row=i, column=1, pady=12, padx=15)
            self.entries[key] = entry

        # Gender
        tk.Label(form_frame, text="Gender*:", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").grid(
            row=len(fields), column=0, sticky="e", pady=12, padx=10)
        self.gender_var = tk.StringVar(value="Male")
        gender_combo = ttk.Combobox(form_frame, textvariable=self.gender_var, values=["Male", "Female", "Other"], 
                                    state="readonly", width=39, font=("Arial", 12))
        gender_combo.grid(row=len(fields), column=1, pady=12, padx=15)

        # Address
        tk.Label(form_frame, text="Address:", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").grid(
            row=len(fields)+1, column=0, sticky="ne", pady=12, padx=10)
        self.address_text = tk.Text(form_frame, width=42, height=6, font=("Arial", 11), relief="solid", bd=1)
        self.address_text.grid(row=len(fields)+1, column=1, pady=12, padx=15)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=30)

        tk.Button(btn_frame, text="➕ Add Student", bg="#10ac84", fg="white", font=("Arial", 12, "bold"),
                  width=20, relief="flat", pady=8, command=self.add_student).grid(row=0, column=0, padx=15)
        tk.Button(btn_frame, text="✏️ Update Student", bg="#ff9f43", fg="white", font=("Arial", 12, "bold"),
                  width=20, relief="flat", pady=8, command=self.update_student).grid(row=0, column=1, padx=15)
        tk.Button(btn_frame, text="🗑️ Clear Form", bg="#576574", fg="white", font=("Arial", 12, "bold"),
                  width=20, relief="flat", pady=8, command=self.clear_form).grid(row=0, column=2, padx=15)

        # Right Panel
        right_frame = tk.Frame(container, bg="#f0f2f5")
        right_frame.grid(row=0, column=1, sticky="nsew")
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Search Bar
        search_frame = tk.Frame(right_frame, bg="#ffffff", relief="solid", bd=1)
        search_frame.pack(fill="x", pady=15, padx=15)
        tk.Label(search_frame, text="🔍 Search Student:", font=("Arial", 14, "bold"), bg="white", fg="#341f97").pack(side="left", padx=20, pady=12)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 13), width=50, relief="solid").pack(side="left", padx=10, pady=12)
        self.search_var.trace("w", lambda *args: self.search_students())
        tk.Button(search_frame, text="🔄 Refresh", bg="#341f97", fg="white", font=("Arial", 11, "bold"), command=self.load_data).pack(side="left", padx=15, pady=12)
        self.count_label = tk.Label(search_frame, text="Total Students: 0", font=("Arial", 16, "bold"), bg="white", fg="#10ac84")
        self.count_label.pack(side="right", padx=30, pady=12)

        # Table
        table_frame = tk.Frame(right_frame, bg="white", relief="solid", bd=2)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("ID", "Name", "Univ ID", "Email", "Gender", "Age", "Phone", "CNIC", "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#341f97")
        style.configure("Treeview", font=("Arial", 11), rowheight=30)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # Buttons below table
        button_frame = tk.Frame(right_frame)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="🗑️ Delete Selected Student", bg="#ee5a52", fg="white",
                  font=("Arial", 14, "bold"), command=self.delete_student, width=30, relief="flat", pady=10).grid(row=0, column=0, padx=20)

        tk.Button(button_frame, text="🖨️ Print Selected Student Slip", bg="#2ecc71", fg="white",
                  font=("Arial", 14, "bold"), command=self.print_slip, width=30, relief="flat", pady=10).grid(row=0, column=1, padx=20)

    def print_slip(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Print karne ke liye student select karo!")
            return

        sid = self.tree.item(sel[0])["values"][0]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Students WHERE StudentID=?", (sid,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return

        # Print Slip Window
        slip_window = tk.Toplevel(self.root)
        slip_window.title("Student Registration Slip")
        slip_window.geometry("700x800")
        slip_window.configure(bg="#f8f9fa")

        # Header
        header_frame = tk.Frame(slip_window, bg="#341f97", height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="🎓 UNIVERSITY OF EXCELLENCE", font=("Arial", 26, "bold"), fg="white", bg="#341f97").pack(pady=20)
        tk.Label(header_frame, text="Official Student Registration Slip", font=("Arial", 18), fg="#dfe4ea", bg="#341f97").pack()

        # Body
        body_frame = tk.Frame(slip_window, bg="#f8f9fa")
        body_frame.pack(pady=40, padx=60)

        tk.Label(body_frame, text="Student Details", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#f8f9fa").grid(row=0, column=0, columnspan=2, pady=20)

        info = [
            ("Student ID", row[0]),
            ("Full Name", row[1]),
            ("University ID", row[2]),
            ("Email", row[3]),
            ("Gender", row[4]),
            ("Age", row[5] or "N/A"),
            ("Phone", row[6] or "N/A"),
            ("CNIC", row[7] or "N/A"),
            ("Address", row[8] or "N/A"),
            ("Enrollment Date", row[9])
        ]

        for i, (label, value) in enumerate(info):
            tk.Label(body_frame, text=f"{label}:", font=("Arial", 14, "bold"), fg="#2c3e50", bg="#f8f9fa", anchor="w").grid(row=i+1, column=0, sticky="w", pady=10)
            tk.Label(body_frame, text=str(value), font=("Arial", 14), fg="#34495e", bg="#f8f9fa", anchor="w").grid(row=i+1, column=1, sticky="w", pady=10, padx=(30,0))

        # Footer
        footer_frame = tk.Frame(slip_window, bg="#f8f9fa")
        footer_frame.pack(side="bottom", pady=40)

        tk.Label(footer_frame, text="This is an official document issued by the University.", font=("Arial", 11, "italic"), fg="#7f8c8d", bg="#f8f9fa").pack()
        tk.Label(footer_frame, text="Authorized Signature _________________________", font=("Arial", 12), fg="#2c3e50", bg="#f8f9fa").pack(pady=20)

        # Print Instruction
        tk.Label(footer_frame, text="Tip: Press Ctrl+P to print this slip", font=("Arial", 12, "bold"), fg="#341f97", bg="#f8f9fa").pack(pady=10)

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.address_text.delete("1.0", tk.END)
        self.gender_var.set("Male")

    def validate_data(self):
        data = {k: e.get().strip() for k, e in self.entries.items()}
        data["Gender"] = self.gender_var.get()
        data["Address"] = self.address_text.get("1.0", tk.END).strip()

        if not (data["FullName"] and data["UniversityID"] and data["Email"]):
            messagebox.showerror("Required", "Full Name, University ID aur Email zaruri hain!")
            return None
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data["Email"]):
            messagebox.showerror("Invalid", "Email format galat hai!")
            return None
        if data["Phone"] and (len(data["Phone"]) != 11 or not data["Phone"].isdigit()):
            messagebox.showerror("Invalid", "Phone 11 digits ka hona chahiye!")
            return None
        if data["CNIC"] and (len(data["CNIC"]) != 13 or not data["CNIC"].isdigit()):
            messagebox.showerror("Invalid", "CNIC 13 digits ka hona chahiye!")
            return None
        try:
            data["Age"] = int(data["Age"]) if data["Age"] else None
        except:
            messagebox.showerror("Invalid", "Age number hona chahiye!")
            return None
        return data

    def add_student(self):
        data = self.validate_data()
        if not data: return
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute('''INSERT INTO Students (FullName, UniversityID, Email, Gender, Age, Phone, CNIC, Address, EnrollmentDate)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (data["FullName"], data["UniversityID"], data["Email"], data["Gender"], data["Age"],
                         data["Phone"] or None, data["CNIC"] or None, data["Address"] or None, date.today().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Naya student add ho gaya!")
            self.clear_form()
            self.load_data()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate", "University ID, Email ya CNIC already exist karta hai!")

    def update_student(self):
        sel = self.tree.selection()
        if not sel: 
            messagebox.showwarning("Select", "Pehle student select karo!")
            return
        data = self.validate_data()
        if not data: return
        sid = self.tree.item(sel[0])["values"][0]
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute('''UPDATE Students SET FullName=?, UniversityID=?, Email=?, Gender=?, Age=?, Phone=?, CNIC=?, Address=?
                           WHERE StudentID=?''',
                        (data["FullName"], data["UniversityID"], data["Email"], data["Gender"], data["Age"],
                         data["Phone"] or None, data["CNIC"] or None, data["Address"] or None, sid))
            conn.commit()
            conn.close()
            messagebox.showinfo("Updated", "Student record update ho gaya!")
            self.clear_form()
            self.load_data()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Duplicate value daala gaya!")

    def delete_student(self):
        sel = self.tree.selection()
        if not sel: 
            messagebox.showwarning("Select", "Delete karne ke liye student select karo!")
            return
        if messagebox.askyesno("Confirm Delete", "Yeh student permanently delete ho jayega!"):
            sid = self.tree.item(sel[0])["values"][0]
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM Students WHERE StudentID=?", (sid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Student record delete ho gaya!")
            self.load_data()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT StudentID, FullName, UniversityID, Email, Gender, Age, Phone, CNIC, EnrollmentDate FROM Students ORDER BY StudentID DESC")
        rows = cur.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.count_label.config(text=f"📊 Total Students: {len(rows)}")

    def search_students(self):
        term = self.search_var.get().lower()
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT StudentID, FullName, UniversityID, Email, Gender, Age, Phone, CNIC, EnrollmentDate FROM Students")
        rows = cur.fetchall()
        conn.close()
        filtered = [r for r in rows if term in " ".join(map(str, r)).lower()]
        for row in filtered:
            self.tree.insert("", "end", values=row)
        self.count_label.config(text=f"🔍 Found: {len(filtered)} students")

    def on_item_double_click(self, event):
        sel = self.tree.selection()
        if not sel: return
        sid = self.tree.item(sel[0])["values"][0]
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Students WHERE StudentID=?", (sid,))
        row = cur.fetchone()
        conn.close()
        if row:
            self.clear_form()
            self.entries["FullName"].insert(0, row[1])
            self.entries["UniversityID"].insert(0, row[2])
            self.entries["Email"].insert(0, row[3])
            self.gender_var.set(row[4])
            if row[5]: self.entries["Age"].insert(0, row[5])
            if row[6]: self.entries["Phone"].insert(0, row[6])
            if row[7]: self.entries["CNIC"].insert(0, row[7])
            if row[8]: self.address_text.insert("1.0", row[8])

if __name__ == "__main__":
    show_login()