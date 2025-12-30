import constants
import psycopg2
from tkinter import messagebox

import tkinter as tk
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

        self.options_panel = OptionsPanelHosteller(self)
        self.options_panel.pack(side='left')

        self.right_panel = ViewComplaintsPanel_(self)
        self.right_panel.pack(padx=10, pady=10, side='right')

        # Panel dictionary to switch views
        self.panel_dict = {
            'view_complaints': ViewComplaintsPanel_(self),
            'ISSUE_NOTICE': ISSUENOTICEPANEL(self),
            'update_complaint': UpdateComplaintPanel(self),
            'VIEW_MENU': VIEWMENUPANEL(self),
            'UPDATE_MENU': UPDATEMENUPANEL(self),
            'view_notices': ViewNoticesPanel___(self),
            'MESSATTENDANCE': MESSATTENDANCEPANEL(self),
            'view_profile': ViewProfilePanel(self),
            'update_profile': UpdateProfilePanel(self)
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
            "View Complaints": lambda: parent.show_panel('view_complaints'),
            "ISSUE NOTICE": lambda: parent.show_panel('ISSUE_NOTICE'),
            "Update Complaint": lambda: parent.show_panel('update_complaint'),
            "FOOD MENU": lambda: parent.show_panel('VIEW_MENU'),
            "UPDATE MENU": lambda: parent.show_panel('UPDATE_MENU'),
            "View Notices": lambda: parent.show_panel('view_notices'),
            "mess attendance": lambda: parent.show_panel('MESSATTENDANCE'),
            "View Profile": lambda: parent.show_panel('view_profile'),
            "Update Profile": lambda: parent.show_panel('update_profile')
        }

        for text, command in buttons.items():
            ButtonField(self, text=text, command=command).pack(pady=10)

class ButtonField(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, width=20, font=('Arial', 12), *args, **kwargs)
        self.parent = parent


class EntryField(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, width=20, font=('Arial', 12), *args, **kwargs)
        self.parent = parent


class LabelField(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, font=('Arial', 12), *args, **kwargs)
        self.parent = parent


# Panels for Each Functionality
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
