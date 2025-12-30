import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime
import db

# --- SHARED BASE CLASS ---
class BasePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack_propagate(False)
        self.config(bg="#f0f0f0")
        
        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#bdc3c7")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))

    def create_header(self, text):
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill="x", side="top")
        lbl = tk.Label(header, text=text, font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="white")
        lbl.pack(pady=15)

    def create_treeview(self, columns):
        frame = tk.Frame(self, bg="#f0f0f0")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        scroll = ttk.Scrollbar(frame)
        scroll.pack(side="right", fill="y")
        
        tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scroll.set)
        tree.pack(fill="both", expand=True)
        scroll.config(command=tree.yview)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
            
        return tree

    def create_form_container(self):
        frame = tk.Frame(self, bg="#f0f0f0")
        frame.pack(pady=40)
        return frame

# --- VIEW PANELS (TABLES) ---

class ViewComplaintsPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("MY COMPLAINTS")
        
        cols = ("ID", "Date", "Status", "Type", "Message")
        self.tree = self.create_treeview(cols)
        self.tree.column("Message", width=300, anchor="w")
        self.load_data()

    def load_data(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Complaint.Complaint_no, Complaint.Date, Complaint.Status, MessageType.Type, Complaint.Message 
                FROM Complaint 
                LEFT JOIN MessageType ON Complaint.Message = MessageType.Message 
                ORDER BY Complaint.Complaint_no;
            """)
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

class ViewBillsPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("MY BILLS")

        cols = ("Bill No", "Amount", "Issue Date", "Due Date", "Paid Date")
        self.tree = self.create_treeview(cols)
        self.load_data()

    def load_data(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Bill.Bill_no, Bill.amount, Bill_Issue.issue_date, Bill_Issue.due_date, Bill.paid_date 
                FROM Bill 
                LEFT JOIN Bill_Issue ON Bill.issue_date = Bill_Issue.issue_date 
                ORDER BY Bill.Bill_no;
            """)
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

class ViewNoticesPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("NOTICES")

        cols = ("Notice No", "Date", "Message")
        self.tree = self.create_treeview(cols)
        self.tree.column("Message", width=400, anchor="w")
        self.load_data()

    def load_data(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Notice_no, Date, Message FROM Notice ORDER BY Notice_no DESC;")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

class ViewProfilePanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("HOSTELLER DIRECTORY")

        cols = ("Name", "Aadhar", "Mobile", "Join Date")
        self.tree = self.create_treeview(cols)
        self.load_data()

    def load_data(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, Person.aadhar, mobile, join_date 
                FROM Person 
                JOIN Hosteller ON Person.aadhar = Hosteller.aadhar 
                ORDER BY name;
            """)
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

# --- ACTION PANELS (FORMS) ---

class RaiseComplaintPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("RAISE NEW COMPLAINT")
        container = self.create_form_container()

        ttk.Label(container, text="Complaint ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_id = ttk.Entry(container, width=30)
        self.ent_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="Type (e.g. Electric):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_type = ttk.Entry(container, width=30)
        self.ent_type.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(container, text="Message:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_msg = ttk.Entry(container, width=30)
        self.ent_msg.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(container, text="Submit Complaint", command=self.submit).grid(row=3, column=0, columnspan=2, pady=20)

    def submit(self):
        cid = self.ent_id.get()
        ctype = self.ent_type.get().title()
        msg = self.ent_msg.get().title()

        if cid and ctype and msg:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                # Insert Type if not exists (Simplified logic)
                try:
                    cursor.execute("INSERT INTO MessageType VALUES (%s, %s);", (msg, ctype))
                except psycopg2.Error:
                    conn.rollback() # Type might exist, ignore
                
                cursor.execute("INSERT INTO Complaint VALUES (%s, %s, %s, %s);", 
                               (cid, datetime.today(), 'pending', msg))
                conn.commit()
                messagebox.showinfo("Success", "Complaint raised successfully!")
                self.ent_id.delete(0, 'end')
                self.ent_msg.delete(0, 'end')
                self.ent_type.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        else:
            messagebox.showwarning("Error", "All fields required.")

class UpdateComplaintPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("UPDATE COMPLAINT")
        container = self.create_form_container()

        ttk.Label(container, text="Complaint ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_id = ttk.Entry(container, width=30)
        self.ent_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="New Status (resolved/pending):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_status = ttk.Entry(container, width=30)
        self.ent_status.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(container, text="Update", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        cid = self.ent_id.get()
        status = self.ent_status.get().lower()

        if cid and status in ['resolved', 'pending']:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Complaint SET Status = %s WHERE Complaint_no = %s;", (status, cid))
                conn.commit()
                messagebox.showinfo("Success", "Status updated.")
                self.ent_id.delete(0, 'end')
                self.ent_status.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        else:
            messagebox.showwarning("Error", "Invalid Input.")

class PayBillPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("PAY BILL")
        container = self.create_form_container()

        ttk.Label(container, text="Bill ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_id = ttk.Entry(container, width=30)
        self.ent_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="Amount:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_amount = ttk.Entry(container, width=30)
        self.ent_amount.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(container, text="Pay Now", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        bid = self.ent_id.get()
        amt = self.ent_amount.get()

        if bid and amt:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Bill SET paid_date = %s WHERE Bill_no = %s;", (datetime.today(), bid))
                conn.commit()
                messagebox.showinfo("Success", "Bill Paid!")
                self.ent_id.delete(0, 'end')
                self.ent_amount.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        else:
            messagebox.showwarning("Error", "Enter Bill ID and Amount.")

class UpdateProfilePanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("UPDATE PROFILE")
        container = self.create_form_container()

        ttk.Label(container, text="Aadhar Number:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_aadhar = ttk.Entry(container, width=30)
        self.ent_aadhar.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="New Mobile:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_mobile = ttk.Entry(container, width=30)
        self.ent_mobile.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(container, text="Update Contact", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        aadhar = self.ent_aadhar.get()
        mobile = self.ent_mobile.get()

        if aadhar and mobile:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Person SET mobile = %s WHERE aadhar = %s;", (mobile, aadhar))
                conn.commit()
                messagebox.showinfo("Success", "Profile Updated.")
                self.ent_aadhar.delete(0, 'end')
                self.ent_mobile.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        else:
            messagebox.showwarning("Error", "All fields required.")

# --- ALIASES (Legacy Support) ---
# These map the old class names to the new modern ones
ViewComplaintsPanel_ = ViewComplaintsPanel
ViewNoticesPanel___ = ViewNoticesPanel

if __name__ == "__main__":
    # Simple test runner
    root = tk.Tk()
    root.geometry("1000x800")
    panel = ViewComplaintsPanel(root)
    panel.pack(fill="both", expand=True)
    root.mainloop()