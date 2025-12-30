import psycopg2
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

db_params = {
    'dbname': 'hostel_mgmt',
    'user': 'postgres',
    'password': 'Jeswin',
    'host': 'localhost',
    'port': '5432'
}

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hostel Management System")
        self.geometry("1300x900")
        self.minsize(1300, 900)

        self.options_panel = OptionsPanelStaff(self)
        self.options_panel.pack(side='left')

        # Placeholder right panel
        self.right_panel = ViewComplaintsPanel(self)
        self.right_panel.pack(padx=10, pady=10, side='right')

        # Panel dictionary to switch views
        self.panel_dict = {
            'allocate_room': AllocateRoomPanel(self),
            'add_building': AddBuildingPanel(self),
            'view_bills': ViewBillsPanel(self),
            'update_bill': UpdateBillPanel(self),
            'view_complaints': ViewComplaintsPanel_(self),
            'ISSUE_NOTICE': ISSUENOTICEPANEL(self),
            'update_complaint': UpdateComplaintPanel(self),
            'VIEW_MENU': VIEWMENUPANEL(self),
            'UPDATE_MENU': UPDATEMENUPANEL(self),
            'view_notices': ViewNoticesPanel___(self),
            'MESSATTENDANCE': MESSATTENDANCEPANEL(self),
            'MESSATTENDANCEMARK': MESSATTENDANCEMARKPANEL(self),
            'view_profile': ViewProfilePanel(self),
            'update_profile': UpdateProfilePanel(self)
        }

    def show_panel(self, panel_name):
        self.right_panel.pack_forget()
        self.right_panel = self.panel_dict[panel_name]
        self.right_panel.pack(padx=10, pady=10, side='right')

class OptionsPanelStaff(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=300, height=750)
        self.pack_propagate(False)
        self.config(bg="lightgreen")

        buttons = {
            "Add Building": lambda: parent.show_panel('add_building'),
            "Allocate Room": lambda: parent.show_panel('allocate_room'),
            "View Bills": lambda: parent.show_panel('view_bills'),
            "Update Bill": lambda: parent.show_panel('update_bill'),
            "View Complaints": lambda: parent.show_panel('view_complaints'),
            "ISSUE NOTICE": lambda: parent.show_panel('ISSUE_NOTICE'),
            "Update Complaint": lambda: parent.show_panel('update_complaint'),
            "FOOD MENU": lambda: parent.show_panel('VIEW_MENU'),
            "UPDATE MENU": lambda: parent.show_panel('UPDATE_MENU'),
            "View Notices": lambda: parent.show_panel('view_notices'),
            "mess attendance": lambda: parent.show_panel('MESSATTENDANCE'),
            "mess attendance mark": lambda: parent.show_panel('MESSATTENDANCEMARK'),
            "View Profile": lambda: parent.show_panel('view_profile'),
            "Update Profile": lambda: parent.show_panel('update_profile')
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
            data = (float(new_amount), datetime.today(), bill_id)
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



class ViewComplaintsPanel_(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightblue")

        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Complaint LEFT JOIN MessageType ON Complaint.Message = MessageType.Message ORDER BY Complaint.Complaint_no;")

        records = cursor.fetchall()
        y_position = 20

        complaint_text = f"Complaint No\tDate\t\tStatus\t\tType\t\tMessage\t\t\t "

        LabelField(self, text=complaint_text).place(x=20, y=y_position)
        y_position = 60

        for rec in records:
            complaint_text = f"{rec[0]}\t{rec[1]}\t{rec[2]}\t\t{rec[5]}\t\t{rec[3]}"
            LabelField(self, text=complaint_text, bg="lightblue").place(x=20, y=y_position)
            y_position += 30

        cursor.close()
        connection.close()

class ISSUENOTICEPANEL(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightyellow")

        LabelField(self, text="ISSUE NOTICE").place(x=20, y=20)
        LabelField(self, text="NOTICE No:").place(x=30, y=80)
        self.entry_id = EntryField(self)
        self.entry_id.place(x=160, y=80)

        LabelField(self, text="Message:").place(x=30, y=120)
        self.entry_message = EntryField(self)
        self.entry_message.place(x=160, y=120)

        ButtonField(self, text="Submit", command=self.submit_notice).place(x=100, y=200)

    def submit_notice(self):
        notice_no = self.entry_id.get()
        message = self.entry_message.get()

        if notice_no and message:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            query = "INSERT INTO Notice (notice_no, message, date) VALUES (%s, %s, %s);"
            data = (notice_no, message, datetime.today())
            cursor.execute(query, data)

            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Notice Submission", "Notice submitted successfully!")
            self.entry_id.delete(0, tk.END)
            self.entry_message.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter valid information")
class MESSATTENDANCEPANEL(tk.Frame):
    def __init__(self, parent):
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightgrey")

        LabelField(self, text="MESS ATTENDANCE DETAILS").place(x=20, y=20)

        cursor.execute("SELECT P.AADHAR,P.NAME,A.DATE_and_time,A.FOOD_ID FROM ATTENDS A JOIN PERSON P ON A.AADHAR=P.AADHAR JOIN MESS M ON A.FOOD_ID=M.FOOD_ID;")

        records = cursor.fetchall()
        y_position = 20

        complaint_text = f"AADHAR\t\tNAME\t\tdate and time\t\t\tFOOD ID"

        LabelField(self, text=complaint_text).place(x=20, y=y_position)
        y_position = 60

        for rec in records:
            complaint_text = f"{rec[0]}\t{rec[1]}\t\t{rec[2]}\t\t{rec[3]}"
            LabelField(self, text=complaint_text, bg="lightgrey").place(x=20, y=y_position)
            y_position += 30

        cursor.close()
        connection.close()


class VIEWMENUPANEL(tk.Frame):
    def __init__(self, parent):
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightcoral")

        LabelField(self, text="View MENU").place(x=20, y=20)

        cursor.execute("SELECT * from mess;")

        records = cursor.fetchall()
        y_position = 20

        complaint_text = f"FOOD ID\tFOOD NAME\tFOOD TYPE"

        LabelField(self, text=complaint_text).place(x=20, y=y_position)
        y_position = 60

        for rec in records:
            complaint_text = f"{rec[0]}\t{rec[1]}\t\t{rec[2]}\t"
            LabelField(self, text=complaint_text, bg="lightcoral").place(x=20, y=y_position)
            y_position += 30

        cursor.close()
        connection.close()

class UPDATEMENUPANEL(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightyellow")

        LabelField(self, text="FOOD MENU UPDATE").place(x=20, y=20)
        LabelField(self, text="FOOD ID:").place(x=30, y=80)
        self.entry_id = EntryField(self)
        self.entry_id.place(x=160, y=80)

        LabelField(self, text="FOODNAME:").place(x=30, y=120)
        self.entry_message = EntryField(self)
        self.entry_message.place(x=160, y=120)

        LabelField(self, text="FOODTYPE:").place(x=30, y=160)
        self.entry_type = EntryField(self)
        self.entry_type.place(x=160, y=160)

        ButtonField(self, text="Submit", command=self.submit_notice).place(x=100, y=200)

    def submit_notice(self):
        notice_no = self.entry_id.get()
        message = self.entry_message.get()
        type = self.entry_type.get()

        if notice_no and message and type:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            query = "INSERT INTO MESS (food_id,food_name,food_type) VALUES (%s, %s,%s);"
            data = (notice_no, message,type)
            cursor.execute(query, data)

            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("MENU Submission", "MENU submitted successfully!")
            self.entry_id.delete(0, tk.END)
            self.entry_message.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter valid information")
class ViewNoticesPanel___(tk.Frame):
    def __init__(self, parent):
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightgrey")

        LabelField(self, text="View Notices").place(x=20, y=20)

        cursor.execute("SELECT * FROM Notice ORDER BY Notice_no;")

        records = cursor.fetchall()
        y_position = 20

        complaint_text = f"Notice No\t\tDate\t\tMessage\t\t"

        LabelField(self, text=complaint_text).place(x=20, y=y_position)
        y_position = 60

        for rec in records:
            complaint_text = f"{rec[0]}\t\t{rec[2]}\t{rec[1]}"
            LabelField(self, text=complaint_text, bg="lightgrey").place(x=20, y=y_position)
            y_position += 30

        cursor.close()
        connection.close()


class ViewProfilePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightcyan")

        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute("SELECT name, Person.aadhar, mobile, join_date FROM Person JOIN Hosteller ON Person.aadhar = Hosteller.aadhar ORDER BY name;")
        records = cursor.fetchall()

        y_position = 20

        profile_text = f"Name\t\taadhar\t\tmobile\t\tJoin Date"
        LabelField(self, text=profile_text).place(x=20, y=y_position)
        y_position = 60

        for rec in records:
            profile_text = f"{rec[0]}\t\t{rec[1]}\t\t{rec[2]}\t\t{rec[3]}"
            LabelField(self, text=profile_text, bg="lightcyan").place(x=20, y=y_position)
            y_position += 30

        cursor.close()
        connection.close()

class UpdateComplaintPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightpink")

        LabelField(self, text="Update Complaint").place(x=20, y=20)
        LabelField(self, text="Complaint ID:").place(x=30, y=80)
        self.entry_id = EntryField(self)
        self.entry_id.place(x=160, y=80)

        LabelField(self, text="New Status:").place(x=30, y=120)
        self.entry_status = EntryField(self)
        self.entry_status.place(x=160, y=120)

        ButtonField(self, text="Update", command=self.update_complaint).place(x=100, y=180)

    def update_complaint(self):

        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        complaint_id = self.entry_id.get()
        new_status = self.entry_status.get().lower()

        if complaint_id and new_status in {'resolved', 'pending'}:
            query = "UPDATE Complaint SET Status = %s WHERE Complaint_no = %s;"
            data = (new_status, complaint_id)

            cursor.execute(query,data)

            messagebox.showinfo("Update Complaint", f"Complaint ID {complaint_id} updated to '{new_status}' status.")
            self.entry_id.delete(0, tk.END)
            self.entry_status.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid Complaint ID and status ('resolved' or 'pending').")

        connection.commit()
        cursor.close()
        connection.close()
class MESSATTENDANCEMARKPANEL(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightyellow")

        LabelField(self, text="MESS ATTENDANCE MARK").place(x=20, y=20)
        LabelField(self, text="AADHAR:").place(x=30, y=80)
        self.entry_id = EntryField(self)
        self.entry_id.place(x=160, y=80)

        LabelField(self, text="FOODID:").place(x=30, y=120)
        self.entry_food_id = EntryField(self)
        self.entry_food_id.place(x=160, y=120)

        ButtonField(self, text="Submit", command=self.submit_notice).place(x=100, y=250)

    def submit_notice(self):
        aadhar = self.entry_id.get()
        food_id = self.entry_food_id.get()

        if aadhar and food_id:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            query = "INSERT INTO ATTENDS (AADHAR, food_ID, DATE_AND_TIME) VALUES (%s, %s, %s);"
            data = (aadhar, food_id, datetime.now())
            cursor.execute(query, data)

            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Attendance Submission", "Attendance submitted successfully!")
            self.entry_id.delete(0, tk.END)
            self.entry_food_id.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter valid information.")



class UpdateProfilePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightsteelblue")

        LabelField(self, text="Update Profile").place(x=20, y=20)

        LabelField(self, text="Enter Aadhar:").place(x=30, y=80)
        self.aadhar_entry = EntryField(self)
        self.aadhar_entry.place(x=220, y=80)

        LabelField(self, text="New Contact Number:").place(x=30, y=120)
        self.new_mobile_entry = EntryField(self)
        self.new_mobile_entry.place(x=220, y=120)

        ButtonField(self, text="Update", command=self.update_profile).place(x=100, y=160)

    def update_profile(self):
        aadhar = self.aadhar_entry.get()
        new_mobile = self.new_mobile_entry.get()

        if aadhar and new_mobile:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            query = "UPDATE Person SET mobile = %s WHERE aadhar = %s;"
            data = (new_mobile, aadhar)
            cursor.execute(query, data)

            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Profile Update", "Profile updated successfully!")
            self.aadhar_entry.delete(0, tk.END)
            self.new_mobile_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter proper values.")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
