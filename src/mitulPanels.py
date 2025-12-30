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
            'raise_complaint': RaiseComplaintPanel(self),
            'update_complaint': UpdateComplaintPanel(self),
            'view_bills': ViewBillsPanel(self),
            'pay_bill': PayBillPanel(self),
            'view_notices': ViewNoticesPanel___(self),
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
            "Raise Complaint": lambda: parent.show_panel('raise_complaint'),
            "Update Complaint": lambda: parent.show_panel('update_complaint'),
            "View Bills": lambda: parent.show_panel('view_bills'),
            "Pay Bill": lambda: parent.show_panel('pay_bill'),
            "View Notices": lambda: parent.show_panel('view_notices'),
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

class RaiseComplaintPanel(tk.Frame):
    def __init__(self, parent):
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightyellow")

        LabelField(self, text="Raise Complaint").place(x=20, y=20)
        LabelField(self, text="Complaint No:").place(x=30, y=80)
        self.entry_id = EntryField(self)
        self.entry_id.place(x=160, y=80)

        LabelField(self, text="Message:").place(x=30, y=120)
        self.entry_complaint = EntryField(self)
        self.entry_complaint.place(x=160, y=120)

        LabelField(self, text="Type:").place(x=30, y=160)
        self.entry_type = EntryField(self)
        self.entry_type.place(x=160, y=160)

        ButtonField(self, text="Submit", command=self.submit_complaint).place(x=100, y=200)

        cursor.close()
        connection.close()

    def submit_complaint(self):

        complaint_num = self.entry_id.get()
        complaint_text = self.entry_complaint.get().title()
        complaint_type = self.entry_type.get().title()

        if complaint_num and complaint_text and complaint_type:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            query = "INSERT INTO MessageType VALUES (%s, %s);"
            data = (complaint_text, complaint_type)
            cursor.execute(query, data)

            query = "INSERT INTO Complaint VALUES (%s, %s, %s, %s);"
            data = (complaint_num, datetime.today(), 'pending', complaint_text)
            cursor.execute(query, data)

            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Complaint Submission", "Complaint submitted successfully!")
            self.entry_complaint.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter valid information")

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

class ViewBillsPanel(tk.Frame):
    def __init__(self, parent):
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightcoral")

        LabelField(self, text="View Bills").place(x=20, y=20)

        cursor.execute("SELECT * FROM Bill LEFT JOIN Bill_Issue ON Bill.issue_date = Bill_Issue.issue_date ORDER BY Bill.Bill_no;")

        records = cursor.fetchall()
        y_position = 20

        complaint_text = f"Bill No\tAmount\t\tIssue Date\tDue Date\t\tPaid Date"

        LabelField(self, text=complaint_text).place(x=20, y=y_position)
        y_position = 60

        for rec in records:
            complaint_text = f"{rec[0]}\t{rec[1]}\t\t{rec[2]}\t{rec[5]}\t{rec[3]}"
            LabelField(self, text=complaint_text, bg="lightcoral").place(x=20, y=y_position)
            y_position += 30

        cursor.close()
        connection.close()

class PayBillPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="beige")

        LabelField(self, text="Pay Bill").place(x=20, y=20)
        LabelField(self, text="Bill ID:").place(x=30, y=80)
        self.entry_id = EntryField(self)
        self.entry_id.place(x=160, y=80)

        LabelField(self, text="Amount:").place(x=30, y=120)
        self.entry_amount = EntryField(self)
        self.entry_amount.place(x=160, y=120)

        ButtonField(self, text="Pay", command=self.pay_bill).place(x=100, y=180)

    def pay_bill(self):
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        bill_id = self.entry_id.get()
        amount = self.entry_amount.get()

        if bill_id and amount > 0:

            query = "UPDATE Bill SET paid_date = %s WHERE Bill_no = %s;"
            data = (datetime.today(), bill_id)
            cursor.execute(query,data)

            messagebox.showinfo("Bill Payment", f"Bill ID {bill_id} paid successfully!")
            self.entry_id.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter proper values.")

        connection.commit()
        cursor.close()
        connection.close()

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
