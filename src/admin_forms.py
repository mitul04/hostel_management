import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import db

# --- SHARED BASE CLASS ---
class BasePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack_propagate(False)
        self.config(bg="#f0f0f0")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TRadiobutton", background="#f0f0f0", font=("Segoe UI", 11))

    def create_header(self, text):
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill="x", side="top")
        lbl = tk.Label(header, text=text, font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="white")
        lbl.pack(pady=15)

    def create_form_container(self):
        # Scrollable container for long forms
        canvas = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        return scrollable_frame

# --- STAFF MANAGEMENT PANELS ---

class AddStaffPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("ADD NEW STAFF MEMBER")
        container = self.create_form_container()

        # Fields List: (Label, Variable Name)
        self.entries = {}
        fields = [
            ("Full Name:", "name"),
            ("Aadhar No:", "aadhar"),
            ("Mobile:", "mobile"),
            ("Age:", "age"),
            ("DOB (YYYY-MM-DD):", "dob"),
            ("House Name:", "h_name"),
            ("House No:", "h_no"),
            ("Street:", "street"),
            ("District:", "district"),
            ("State:", "state"),
            ("Pincode:", "pin"),
            ("Username:", "username"),
            ("Password:", "password")
        ]

        for i, (lbl_text, key) in enumerate(fields):
            ttk.Label(container, text=lbl_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            ent = ttk.Entry(container, width=35)
            ent.grid(row=i, column=1, padx=10, pady=5)
            self.entries[key] = ent

        # Role Selection
        ttk.Label(container, text="Role:").grid(row=len(fields), column=0, sticky="e", padx=10)
        self.role_var = tk.StringVar(value="Security")
        role_frame = tk.Frame(container, bg="#f0f0f0")
        role_frame.grid(row=len(fields), column=1, sticky="w", pady=5)
        
        roles = ["Warden", "Chef", "Security", "Cleaning", "Electrician", "Plumber"]
        for r in roles:
            ttk.Radiobutton(role_frame, text=r, variable=self.role_var, value=r).pack(side="left", padx=5)

        # Buttons
        btn_frame = tk.Frame(container, bg="#f0f0f0")
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Add Staff", command=self.submit).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side="left", padx=10)

    def submit(self):
        # Gather Data
        data = {k: v.get().strip() for k, v in self.entries.items()}
        role = self.role_var.get()
        
        # Basic Validation
        if not data['aadhar'] or not data['username'] or not data['password']:
            messagebox.showwarning("Error", "Aadhar, Username and Password are required.")
            return

        # Combine Address
        address = f"{data['h_name']}, {data['h_no']}, {data['street']}, {data['district']}, {data['state']} - {data['pin']}"

        conn = db.get_db_connection()
        if not conn: return
        
        try:
            cursor = conn.cursor()
            
            # 1. Insert into Person
            cursor.execute("""
                INSERT INTO Person (aadhar, name, age, dob, mobile, address) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data['aadhar'], data['name'], data['age'], data['dob'], data['mobile'], address))

            # 2. Insert into Staff
            cursor.execute("INSERT INTO Staff (aadhar, role) VALUES (%s, %s)", (data['aadhar'], role))

            # 3. Insert into Login
            cursor.execute("""
                INSERT INTO Login (username, person_type, password, last_login) 
                VALUES (%s, 'staff', %s, %s)
            """, (data['username'], data['password'], datetime.now()))

            # 4. Insert into Access (Link Aadhar to Username)
            cursor.execute("INSERT INTO Access (aadhar, username) VALUES (%s, %s)", (data['aadhar'], data['username']))

            conn.commit()
            messagebox.showinfo("Success", "Staff Member Added Successfully!")
            self.clear_form()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def clear_form(self):
        for ent in self.entries.values():
            ent.delete(0, 'end')


class UpdateStaffPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("UPDATE STAFF DETAILS")
        container = self.create_form_container()

        ttk.Label(container, text="Enter Aadhar ID to Update:").grid(row=0, column=0, padx=10, pady=20, sticky="e")
        self.ent_search = ttk.Entry(container, width=30)
        self.ent_search.grid(row=0, column=1, padx=10, pady=20)
        
        # Only allowing mobile update for now as per previous logic, but can be expanded
        ttk.Label(container, text="New Mobile Number:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.ent_mobile = ttk.Entry(container, width=30)
        self.ent_mobile.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(container, text="Update Mobile", command=self.update_staff).grid(row=2, column=0, columnspan=2, pady=20)

    def update_staff(self):
        aadhar = self.ent_search.get()
        mob = self.ent_mobile.get()

        if aadhar and mob:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Person SET mobile = %s WHERE aadhar = %s", (mob, aadhar))
                if cursor.rowcount == 0:
                    messagebox.showwarning("Error", "Aadhar number not found.")
                else:
                    conn.commit()
                    messagebox.showinfo("Success", "Contact Updated")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()


# --- HOSTELLER (STUDENT) PANELS ---

class AddHostellerPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("ADD NEW HOSTELLER")
        container = self.create_form_container()

        self.entries = {}
        fields = [
            ("Full Name:", "name"),
            ("Aadhar No:", "aadhar"),
            ("Mobile:", "mobile"),
            ("Age:", "age"),
            ("DOB (YYYY-MM-DD):", "dob"),
            ("House Name:", "h_name"),
            ("House No:", "h_no"),
            ("Street:", "street"),
            ("District:", "district"),
            ("State:", "state"),
            ("Pincode:", "pin"),
            ("Guardian Name:", "g_name"),
            ("Guardian Phone:", "g_mob"),
            ("Join Date (YYYY-MM-DD):", "join_date"),
            ("Username:", "username"),
            ("Password:", "password")
        ]

        for i, (lbl_text, key) in enumerate(fields):
            ttk.Label(container, text=lbl_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            ent = ttk.Entry(container, width=35)
            ent.grid(row=i, column=1, padx=10, pady=5)
            self.entries[key] = ent

        btn_frame = tk.Frame(container, bg="#f0f0f0")
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Add Hosteller", command=self.submit).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side="left", padx=10)

    def submit(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        
        if not data['aadhar'] or not data['username']:
            messagebox.showwarning("Error", "Aadhar and Username are required.")
            return

        address = f"{data['h_name']}, {data['h_no']}, {data['street']}, {data['district']}, {data['state']} - {data['pin']}"

        conn = db.get_db_connection()
        if not conn: return
        
        try:
            cursor = conn.cursor()
            
            # 1. Insert Person
            cursor.execute("""
                INSERT INTO Person (aadhar, name, age, dob, mobile, address) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data['aadhar'], data['name'], data['age'], data['dob'], data['mobile'], address))

            # 2. Insert Guardian (Ignore if exists)
            try:
                cursor.execute("INSERT INTO Guardian (guardian_mob, guardian_name) VALUES (%s, %s)", 
                               (data['g_mob'], data['g_name']))
            except psycopg2.Error:
                conn.rollback() # Guardian might already exist for a sibling

            # 3. Insert Hosteller
            cursor.execute("""
                INSERT INTO Hosteller (aadhar, guardian_mob, join_date) 
                VALUES (%s, %s, %s)
            """, (data['aadhar'], data['g_mob'], data['join_date']))

            # 4. Insert Login
            cursor.execute("""
                INSERT INTO Login (username, person_type, password, last_login) 
                VALUES (%s, 'hosteller', %s, %s)
            """, (data['username'], data['password'], datetime.now()))

            # 5. Insert Access
            cursor.execute("INSERT INTO Access (aadhar, username) VALUES (%s, %s)", (data['aadhar'], data['username']))

            conn.commit()
            messagebox.showinfo("Success", "Hosteller Added Successfully!")
            self.clear_form()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def clear_form(self):
        for ent in self.entries.values():
            ent.delete(0, 'end')

class ProfileStaffPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("STAFF PROFILES")
        # Placeholder for viewing staff
        lbl = tk.Label(self, text="Use 'View Profile' in Options to see details.", bg="#f0f0f0")
        lbl.pack(pady=50)

# --- TEST WRAPPER ---
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Panels Jithin Test")
        self.geometry("1100x800")
        
        # Test the complex form
        self.panel = AddHostellerPanel(self)
        self.panel.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()