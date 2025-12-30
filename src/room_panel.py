import psycopg2
import tkinter as tk
from tkinter import messagebox
from datetime import date

db_params = {
    'dbname': 'hostel_mgmt',
    'user': 'postgres',
    'password': 'Alan123',
    'host': 'localhost',
    'port': '5432'
}

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hostel Management System")
        self.geometry("1300x900")
        self.minsize(1300, 900)

        self.options_panel = OptionsPanelHosteller(self)
        self.options_panel.pack(side='left')

        # Placeholder right panel
        self.right_panel = ViewComplaintsPanel(self)
        self.right_panel.pack(padx=10, pady=10, side='right')

        # Panel dictionary to switch views
        self.panel_dict = {
            'allocate_room': AllocateRoomPanel(self),
            'add_building': AddBuildingPanel(self),
            'view_bills': ViewBillsPanel(self),
            'update_bill': UpdateBillPanel(self)
        }

    def show_panel(self, panel_name):
        self.right_panel.pack_forget()
        self.right_panel = self.panel_dict[panel_name]
        self.right_panel.pack(padx=10, pady=10, side='right')

class OptionsPanelHosteller(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=300, height=750)
        self.pack_propagate(False)
        self.config(bg="lightgreen")

        buttons = {
            "Add Building": lambda: parent.show_panel('add_building'),
            "Allocate Room": lambda: parent.show_panel('allocate_room'),
            "View Bills": lambda: parent.show_panel('view_bills'),
            "Update Bill": lambda: parent.show_panel('update_bill')
        }

        for text, command in buttons.items():
            ButtonField(self, text=text, command=command).pack(pady=10)

class ButtonField(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, width=20, font=('Arial', 12), *args, **kwargs)

class EntryField(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, width=20, font=('Arial', 12), *args, **kwargs)

class LabelField(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, font=('Arial', 12), *args, **kwargs)

# Placeholder for ViewComplaintsPanel
class ViewComplaintsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightyellow")
        LabelField(self, text="ROOMS AND BILL MANAGER").place(x=30, y=30)

class AllocateRoomPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightpink")

        LabelField(self, text="ALLOCATE ROOM").place(x=80, y=40)

        self.label_room_number = LabelField(self, text="Room Number:")
        self.label_room_number.place(x=30, y=80)
        self.entry_room_number = EntryField(self)
        self.entry_room_number.place(x=150, y=80)

        self.label_user_name = LabelField(self, text="User Name:")
        self.label_user_name.place(x=30, y=130)
        self.entry_user_name = EntryField(self)
        self.entry_user_name.place(x=150, y=130)

        self.allocate_button = tk.Button(self, text="Allocate Room", width=15, font=('Arial', 12),
                                         command=self.allocate_room)
        self.allocate_button.place(x=150, y=180)

        self.deallocate_button = tk.Button(self, text="Deallocate Room", width=15, font=('Arial', 12),
                                           command=self.deallocate_room)
        self.deallocate_button.place(x=300, y=180)

    def allocate_room(self):
        room_number = self.entry_room_number.get().strip()
        user_name = self.entry_user_name.get().strip()

        if not room_number or not user_name:
            messagebox.showerror("Input Error", "Please enter a valid room number and user name.")
            return

        try:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            cursor.execute("SELECT aadhar FROM Access WHERE username = %s;", (user_name,))
            aadhar_result = cursor.fetchone()

            if not aadhar_result:
                messagebox.showerror("Allocation Error", f"User '{user_name}' does not exist.")
                return

            aadhar = aadhar_result[0]

            cursor.execute("SELECT * FROM Gets WHERE room_no = %s AND building_no = '1';", (room_number,))
            if cursor.fetchone():
                messagebox.showerror("Allocation Error", f"Room {room_number} is already allocated.")
                return

            cursor.execute("INSERT INTO Gets (aadhar, room_no, building_no) VALUES (%s, %s, '1');",
                           (aadhar, room_number))
            connection.commit()

            messagebox.showinfo("Success", f"Room {room_number} allocated to {user_name}.")
            self.entry_room_number.delete(0, tk.END)
            self.entry_user_name.delete(0, tk.END)

        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")
        finally:
            cursor.close()
            connection.close()

    def deallocate_room(self):
        room_number = self.entry_room_number.get().strip()
        user_name = self.entry_user_name.get().strip()

        if not room_number or not user_name:
            messagebox.showerror("Input Error", "Please enter a valid room number and user name.")
            return

        try:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            cursor.execute("SELECT aadhar FROM Access WHERE username = %s;", (user_name,))
            aadhar_result = cursor.fetchone()

            if not aadhar_result:
                messagebox.showerror("Deallocation Error", f"User '{user_name}' does not exist.")
                return

            aadhar = aadhar_result[0]

            cursor.execute("SELECT * FROM Gets WHERE aadhar = %s AND room_no = %s AND building_no = '1';",
                           (aadhar, room_number))
            if not cursor.fetchone():
                messagebox.showerror("Deallocation Error", f"Room {room_number} is not allocated to {user_name}.")
                return

            cursor.execute("DELETE FROM Gets WHERE aadhar = %s AND room_no = %s AND building_no = '1';",
                           (aadhar, room_number))
            connection.commit()

            messagebox.showinfo("Success", f"Room {room_number} deallocated from {user_name}.")
            self.entry_room_number.delete(0, tk.END)
            self.entry_user_name.delete(0, tk.END)

        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")
        finally:
            cursor.close()
            connection.close()

class AddBuildingPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightpink")

        LabelField(self, text="ADD BUILDING").place(x=20, y=20)
        LabelField(self, text="Building Name").place(x=30, y=80)
        self.entry_building_name = EntryField(self)
        self.entry_building_name.place(x=160, y=80)

        LabelField(self, text="Total Rooms").place(x=30, y=120)
        self.entry_total_rooms = EntryField(self)
        self.entry_total_rooms.place(x=160, y=120)

        ButtonField(self, text="Add Building", command=self.add_building).place(x=100, y=180)

    def add_building(self):
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        building_name = self.entry_building_name.get().strip()
        total_rooms = self.entry_total_rooms.get().strip()

        if building_name and total_rooms.isdigit() and int(total_rooms) > 0:
            try:
                query = "INSERT INTO Building (building_name, total_rooms) VALUES (%s, %s);"
                data = (building_name, int(total_rooms))

                cursor.execute(query, data)
                connection.commit()

                messagebox.showinfo("Success", f"Building '{building_name}' added successfully.")
                self.entry_building_name.delete(0, tk.END)
                self.entry_total_rooms.delete(0, tk.END)

            except Exception as e:
                messagebox.showerror("Error adding building", f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showwarning("Input Error", "Please enter valid building name and total rooms.")

class ViewBillsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightblue")

        LabelField(self, text="VIEW BILLS").place(x=30, y=30)
        self.label_bills = LabelField(self, text="")
        self.label_bills.place(x=30, y=70)

        ButtonField(self, text="Refresh Bills", command=self.view_bills).place(x=30, y=400)

    def view_bills(self):
        try:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Bill;")
            bills = cursor.fetchall()

            bill_info = "\n".join([f"Bill ID: {row[0]}, Amount: {row[1]}, User: {row[2]}" for row in bills])
            self.label_bills.config(text=bill_info if bill_info else "No bills found.")

        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")
        finally:
            cursor.close()
            connection.close()

class UpdateBillPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightsteelblue")

        LabelField(self, text="UPDATE BILL").place(x=20, y=20)

        LabelField(self, text="Bill ID:").place(x=30, y=80)
        self.bill_id_entry = EntryField(self)
        self.bill_id_entry.place(x=220, y=80)

        LabelField(self, text="Amount:").place(x=30, y=120)
        self.amount_entry = EntryField(self)
        self.amount_entry.place(x=220, y=120)

        ButtonField(self, text="Update Bill", command=self.update_bill).place(x=100, y=160)

    def update_bill(self):
        bill_id = self.bill_id_entry.get().strip()
        new_amount = self.amount_entry.get().strip()

        # Validate input: Bill ID should not be empty and amount should be a valid positive number
        if bill_id and new_amount.replace('.', '', 1).isdigit() and float(new_amount) >= 0:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            # Update the amount and set paid_date to today's date
            query = "UPDATE Bill SET amount = %s, paid_date = %s WHERE Bill_no = %s;"
            data = (float(new_amount), date.today(), bill_id)
            cursor.execute(query, data)

            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Bill Update", "Bill updated successfully!")
            # Clear input fields
            self.bill_id_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid Bill ID and a positive amount.")
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
