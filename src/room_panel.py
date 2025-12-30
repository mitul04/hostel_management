import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import date
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

# --- ACTION PANELS ---

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

        ttk.Button(btn_frame, text="Allocate Room", command=self.allocate).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Deallocate Room", command=self.deallocate).pack(side="left", padx=10)

    def allocate(self):
        self._manage_room("allocate")

    def deallocate(self):
        self._manage_room("deallocate")

    def _manage_room(self, action):
        room = self.ent_room.get().strip()
        user = self.ent_user.get().strip()

        if not room or not user:
            messagebox.showerror("Error", "Please enter Room and Username.")
            return

        conn = db.get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            
            # 1. Get Aadhar from Username
            cursor.execute("SELECT aadhar FROM Access WHERE username = %s;", (user,))
            res = cursor.fetchone()
            if not res:
                messagebox.showerror("Error", f"User '{user}' does not exist.")
                return
            aadhar = res[0]

            if action == "allocate":
                # Check if room is already taken
                cursor.execute("SELECT * FROM Gets WHERE room_no = %s AND building_no = '1';", (room,))
                if cursor.fetchone():
                    messagebox.showerror("Error", f"Room {room} is occupied.")
                    return
                
                cursor.execute("INSERT INTO Gets (aadhar, room_no, building_no) VALUES (%s, %s, '1');", (aadhar, room))
                msg = "allocated to"
            else:
                # Check if user actually owns this room
                cursor.execute("SELECT * FROM Gets WHERE aadhar = %s AND room_no = %s AND building_no = '1';", (aadhar, room))
                if not cursor.fetchone():
                    messagebox.showerror("Error", f"Room {room} is not allocated to {user}.")
                    return
                
                cursor.execute("DELETE FROM Gets WHERE aadhar = %s AND room_no = %s AND building_no = '1';", (aadhar, room))
                msg = "deallocated from"

            conn.commit()
            messagebox.showinfo("Success", f"Room {room} {msg} {user}.")
            self.ent_room.delete(0, 'end')
            self.ent_user.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
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
        name = self.ent_name.get().strip()
        rooms = self.ent_rooms.get().strip()

        if name and rooms.isdigit() and int(rooms) > 0:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Building (building_name, total_rooms) VALUES (%s, %s);", (name, int(rooms)))
                conn.commit()
                messagebox.showinfo("Success", f"Building '{name}' added.")
                self.ent_name.delete(0, 'end')
                self.ent_rooms.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        else:
            messagebox.showwarning("Error", "Invalid Input")

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

        ttk.Button(container, text="Update Bill", command=self.submit).grid(row=2, column=0, columnspan=2, pady=20)

    def submit(self):
        bid = self.ent_id.get().strip()
        amt = self.ent_amt.get().strip()

        # Simple validation for float
        is_float = False
        try:
            float(amt)
            is_float = True
        except ValueError:
            pass

        if bid and is_float and float(amt) >= 0:
            conn = db.get_db_connection()
            if not conn: return
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Bill SET amount = %s, paid_date = %s WHERE Bill_no = %s;", 
                               (float(amt), date.today(), bid))
                conn.commit()
                messagebox.showinfo("Success", "Bill Updated Successfully!")
                self.ent_id.delete(0, 'end')
                self.ent_amt.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()
        else:
            messagebox.showwarning("Error", "Invalid Bill ID or Amount.")

class ViewBillsPanel(BasePanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header("VIEW BILLS")
        
        # Upgraded to Treeview Table instead of text label
        cols = ("Bill No", "Amount", "Paid Date", "Issue Date")
        self.tree = self.create_treeview(cols)
        
        # Refresh button below table
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Refresh Data", command=self.load_data).pack()
        
        self.load_data()

    def load_data(self):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = db.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Bill;")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

# --- TEST WRAPPER ---
if __name__ == "__main__":
    app = tk.Tk()
    app.geometry("1000x800")
    app.title("Room Panel Test")
    
    # Just testing one panel
    panel = AllocateRoomPanel(app)
    panel.pack(fill="both", expand=True)
    
    app.mainloop()