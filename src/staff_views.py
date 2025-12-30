import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime
import db  # Using your central database file

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
        style.configure("TRadiobutton", background="#f0f0f0", font=("Segoe UI", 11))

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

# --- ACTION PANELS (FORMS) ---

class AllocateRoomPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("ALLOCATE ROOM")
        container = self.create_form_container()

        ttk.Label(container, text="Room Number:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_room = ttk.Entry(container, width=30)
        self.ent_room.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="User Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_user = ttk.Entry(container, width=30)
        self.ent_user.grid(row=1, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(container, bg="#f0f0f0")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Allocate", command=self.allocate).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Deallocate", command=self.deallocate).pack(side="left", padx=10)

    def allocate(self):
        self._manage_room("allocate")

    def deallocate(self):
        self._manage_room("deallocate")

    def _manage_room(self, action):
        room = self.ent_room.get().strip()
        user = self.ent_user.get().strip()

        if not room or not user:
            messagebox.showerror("Error", "Enter Room and Username")
            return

        conn = db.get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # Get Aadhar
            cursor.execute("SELECT aadhar FROM Access WHERE username = %s;", (user,))
            res = cursor.fetchone()
            if not res:
                messagebox.showerror("Error", "User not found")
                return
            aadhar = res[0]

            if action == "allocate":
                # Check occupancy
                cursor.execute("SELECT * FROM Gets WHERE room_no = %s AND building_no = '1';", (room,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Room already occupied")
                    return
                cursor.execute("INSERT INTO Gets (aadhar, room_no, building_no) VALUES (%s, %s, '1');", (aadhar, room))
                msg = "Allocated"
            else:
                # Check ownership
                cursor.execute("SELECT * FROM Gets WHERE aadhar = %s AND room_no = %s AND building_no = '1';", (aadhar, room))
                if not cursor.fetchone():
                    messagebox.showerror("Error", "User is not in this room")
                    return
                cursor.execute("DELETE FROM Gets WHERE aadhar = %s AND room_no = %s AND building_no = '1';", (aadhar, room))
                msg = "Deallocated"

            conn.commit()
            messagebox.showinfo("Success", f"Room {msg} successfully!")
            self.ent_room.delete(0, 'end')
            self.ent_user.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

class AddBuildingPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("ADD BUILDING")
        container = self.create_form_container()

        ttk.Label(container, text="Building Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_name = ttk.Entry(container, width=30)
        self.ent_name.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="Total Rooms:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_rooms = ttk.Entry(container, width=30)
        self.ent_rooms.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(container, text="Add Building", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        name = self.ent_name.get()
        rooms = self.ent_rooms.get()

        if name and rooms.isdigit():
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Building (building_name, total_rooms) VALUES (%s, %s);", (name, int(rooms)))
                conn.commit()
                messagebox.showinfo("Success", "Building Added")
                self.ent_name.delete(0, 'end')
                self.ent_rooms.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Invalid Input")

class UpdateBillPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("UPDATE BILL")
        container = self.create_form_container()

        ttk.Label(container, text="Bill ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_id = ttk.Entry(container, width=30)
        self.ent_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="New Amount:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_amt = ttk.Entry(container, width=30)
        self.ent_amt.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(container, text="Update", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        bid = self.ent_id.get()
        amt = self.ent_amt.get()
        if bid and amt:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Bill SET amount = %s, paid_date = %s WHERE Bill_no = %s;", (amt, datetime.today(), bid))
                conn.commit()
                messagebox.showinfo("Success", "Bill Updated")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

class IssueNoticePanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("ISSUE NOTICE")
        container = self.create_form_container()

        ttk.Label(container, text="Notice ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_id = ttk.Entry(container, width=30)
        self.ent_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="Message:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_msg = ttk.Entry(container, width=30)
        self.ent_msg.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(container, text="Issue", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        nid = self.ent_id.get()
        msg = self.ent_msg.get()
        if nid and msg:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Notice (notice_no, message, date) VALUES (%s, %s, %s);", 
                               (nid, msg, datetime.today()))
                conn.commit()
                messagebox.showinfo("Success", "Notice Issued")
                self.ent_id.delete(0, 'end')
                self.ent_msg.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

class UpdateMenuPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("UPDATE MENU")
        container = self.create_form_container()

        ttk.Label(container, text="Food ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_id = ttk.Entry(container, width=30)
        self.ent_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_name = ttk.Entry(container, width=30)
        self.ent_name.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(container, text="Type:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_type = ttk.Entry(container, width=30)
        self.ent_type.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(container, text="Add Item", command=self.submit).grid(row=3, column=0, columnspan=2, pady=20)

    def submit(self):
        fid = self.ent_id.get()
        fname = self.ent_name.get()
        ftype = self.ent_type.get()
        if fid and fname:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO MESS (food_id, food_name, food_type) VALUES (%s, %s, %s);", 
                               (fid, fname, ftype))
                conn.commit()
                messagebox.showinfo("Success", "Item Added")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

class MarkAttendancePanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("MARK MESS ATTENDANCE")
        container = self.create_form_container()

        ttk.Label(container, text="Aadhar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_id = ttk.Entry(container, width=30)
        self.ent_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="Food ID:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_fid = ttk.Entry(container, width=30)
        self.ent_fid.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(container, text="Submit", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        uid = self.ent_id.get()
        fid = self.ent_fid.get()
        if uid and fid:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO ATTENDS (AADHAR, food_ID, DATE_AND_TIME) VALUES (%s, %s, %s);", 
                               (uid, fid, datetime.now()))
                conn.commit()
                messagebox.showinfo("Success", "Attendance Marked")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

class UpdateProfilePanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("UPDATE PROFILE")
        container = self.create_form_container()

        ttk.Label(container, text="Aadhar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_aadhar = ttk.Entry(container, width=30)
        self.ent_aadhar.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(container, text="New Mobile:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_mob = ttk.Entry(container, width=30)
        self.ent_mob.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(container, text="Update", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        uid = self.ent_aadhar.get()
        mob = self.ent_mob.get()
        if uid and mob:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Person SET mobile = %s WHERE aadhar = %s;", (mob, uid))
                conn.commit()
                messagebox.showinfo("Success", "Profile Updated")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

class UpdateComplaintPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("UPDATE COMPLAINT")
        container = self.create_form_container()
        
        ttk.Label(container, text="Complaint ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_id = ttk.Entry(container, width=30)
        self.ent_id.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(container, text="New Status:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_stat = ttk.Entry(container, width=30)
        self.ent_stat.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Button(container, text="Update", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        cid = self.ent_id.get()
        stat = self.ent_stat.get().lower()
        if cid and stat in ['resolved', 'pending']:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Complaint SET Status = %s WHERE Complaint_no = %s;", (stat, cid))
                conn.commit()
                messagebox.showinfo("Success", "Complaint Updated")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

# --- VIEW PANELS (TABLES) ---

class ViewBillsPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("ALL BILLS")
        cols = ("Bill No", "Amount", "Paid Date", "Issue Date")
        self.tree = self.create_treeview(cols)
        self.load()

    def load(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Bill")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        finally:
            conn.close()

class ViewComplaintsPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("ALL COMPLAINTS")
        cols = ("ID", "Date", "Status", "Type", "Message")
        self.tree = self.create_treeview(cols)
        self.tree.column("Message", width=300, anchor="w")
        self.load()

    def load(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Complaint.*, MessageType.Type FROM Complaint LEFT JOIN MessageType ON Complaint.Message = MessageType.Message")
            for row in cursor.fetchall():
                # Adjusting for tuple structure returned by fetchall
                self.tree.insert("", "end", values=(row[0], row[1], row[2], row[4], row[3])) 
        finally:
            conn.close()

class ViewMenuPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("FOOD MENU")
        cols = ("ID", "Name", "Type")
        self.tree = self.create_treeview(cols)
        self.load()

    def load(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mess")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        finally:
            conn.close()

class MessAttendanceLogPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("ATTENDANCE LOG")
        cols = ("Aadhar", "Name", "Time", "Food ID")
        self.tree = self.create_treeview(cols)
        self.tree.column("Time", width=150)
        self.load()

    def load(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT P.AADHAR, P.NAME, A.DATE_and_time, A.FOOD_ID FROM ATTENDS A JOIN PERSON P ON A.AADHAR=P.AADHAR")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        finally:
            conn.close()

class ViewNoticesPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("NOTICES")
        cols = ("ID", "Message", "Date")
        self.tree = self.create_treeview(cols)
        self.tree.column("Message", width=300)
        self.load()

    def load(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Notice ORDER BY Notice_no")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        finally:
            conn.close()

class ViewProfilePanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("PROFILES")
        cols = ("Name", "Aadhar", "Mobile", "Joined")
        self.tree = self.create_treeview(cols)
        self.load()

    def load(self):
        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name, Person.aadhar, mobile, join_date FROM Person JOIN Hosteller ON Person.aadhar = Hosteller.aadhar")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        finally:
            conn.close()

# --- LEGACY ALIASES (For Compatibility) ---
# These map the old names to the new modern classes
ViewComplaintsPanel_ = ViewComplaintsPanel
ISSUENOTICEPANEL = IssueNoticePanel
VIEWMENUPANEL = ViewMenuPanel
UPDATEMENUPANEL = UpdateMenuPanel
ViewNoticesPanel___ = ViewNoticesPanel
MESSATTENDANCEPANEL = MessAttendanceLogPanel
MESSATTENDANCEMARKPANEL = MarkAttendancePanel

# --- TEST WRAPPER ---
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Staff Panel Test")
        self.geometry("1300x900")
        
        # Testing Allocate Room Panel
        panel = AllocateRoomPanel(self)
        panel.pack(fill='both', expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()