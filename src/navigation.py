import tkinter as tk
from tkinter import ttk
import constants
from login import LoginPanel

# --- IMPORTS FROM YOUR NEW RENAMED FILES ---
from student_views import * # Formerly mitulPanels.py
from staff_views import * # Formerly staff.py
from admin_forms import AddStaffPanel, AddHostellerPanel, UpdateStaffPanel # Formerly panels_jithin.py

class OptionsPanelStaff(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent, width=280, height=850)
        self.pack_propagate(False)
        self.config(bg="#2c3e50") # Dark Blue Sidebar
        self.parent = parent

        # Welcome Label
        lbl_welcome = tk.Label(self, text=f"Welcome,\n{username}", 
                               font=("Segoe UI", 14, "bold"), 
                               bg="#2c3e50", fg="white", justify="center")
        lbl_welcome.pack(pady=(40, 30), padx=10, fill="x")

        # Menu Buttons
        # We use a list to keep them in order
        self.buttons = {
            "Allocate Room": lambda: self.load_panel(AllocateRoomPanel),
            "Add Building": lambda: self.load_panel(AddBuildingPanel),
            "Add Staff": lambda: self.load_panel(AddStaffPanel),
            "Add Hosteller": lambda: self.load_panel(AddHostellerPanel),
            "View Bills": lambda: self.load_panel(ViewBillsPanel),
            "Update Bills": lambda: self.load_panel(UpdateBillPanel),
            "View Complaints": lambda: self.load_panel(ViewComplaintsPanel),
            "Update Complaint": lambda: self.load_panel(UpdateComplaintPanel),
            "Food Menu": lambda: self.load_panel(ViewMenuPanel),
            "Update Menu": lambda: self.load_panel(UpdateMenuPanel),
            "Mess Log": lambda: self.load_panel(MessAttendanceLogPanel),
            "Mark Attendance": lambda: self.load_panel(MarkAttendancePanel),
            "Issue Notice": lambda: self.load_panel(IssueNoticePanel),
            "View Notices": lambda: self.load_panel(ViewNoticesPanel),
            "View Profiles": lambda: self.load_panel(ViewProfilePanel),
            "Log Out": lambda: self.userLogout()
        }

        # Create Buttons using Modern ttk
        for text, command in self.buttons.items():
            btn = ttk.Button(self, text=text, command=command, style="Sidebar.TButton")
            btn.pack(fill="x", pady=2, padx=10)

    def load_panel(self, panel_class):
        # Creates the panel only when clicked (prevents lag)
        new_panel = panel_class(self.parent)
        self.parent.addRightPanel(new_panel)

    def init(self):
        self.load_panel(ViewNoticesPanel)

    def userLogout(self):
        guest = OptionsPanelGuest(self.parent)
        self.parent.addLeftPanel(guest)
        guest.init()


class OptionsPanelHosteller(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent, width=280, height=850)
        self.pack_propagate(False)
        self.config(bg="#2c3e50") # Dark Blue Sidebar
        self.parent = parent

        # Welcome Label
        lbl_welcome = tk.Label(self, text=f"Hello,\n{username}", 
                               font=("Segoe UI", 14, "bold"), 
                               bg="#2c3e50", fg="white", justify="center")
        lbl_welcome.pack(pady=(40, 30), padx=10, fill="x")

        self.buttons = {
            "View Complaints": lambda: self.load_panel(ViewComplaintsPanel),
            "Raise Complaint": lambda: self.load_panel(RaiseComplaintPanel),
            "Update Complaint": lambda: self.load_panel(UpdateComplaintPanel),
            "View Bills": lambda: self.load_panel(ViewBillsPanel),
            "Pay Bill": lambda: self.load_panel(PayBillPanel),
            "View Notices": lambda: self.load_panel(ViewNoticesPanel),
            "View Profile": lambda: self.load_panel(ViewProfilePanel),
            "Update Profile": lambda: self.load_panel(UpdateProfilePanel),
            "Log Out": lambda: self.userLogout()
        }

        # Create Buttons using Modern ttk
        for text, command in self.buttons.items():
            btn = ttk.Button(self, text=text, command=command, style="Sidebar.TButton")
            btn.pack(fill="x", pady=2, padx=10)

    def load_panel(self, panel_class):
        new_panel = panel_class(self.parent)
        self.parent.addRightPanel(new_panel)

    def init(self):
        self.load_panel(ViewNoticesPanel)

    def userLogout(self):
        guest = OptionsPanelGuest(self.parent)
        self.parent.addLeftPanel(guest)
        guest.init()


class OptionsPanelGuest(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=280, height=850)
        self.parent = parent
        self.pack_propagate(False)
        self.config(bg="#2c3e50") # Dark Blue Sidebar

        self.loginView = None
        
        # Center the title
        lbl_title = tk.Label(self, text="HOSTEL\nMANAGEMENT\nSYSTEM", 
                             font=("Segoe UI", 18, "bold"), 
                             bg="#2c3e50", fg="white", justify="center")
        lbl_title.place(relx=0.5, rely=0.4, anchor="center")

        lbl_sub = tk.Label(self, text="Please Login", 
                           font=("Segoe UI", 12), 
                           bg="#2c3e50", fg="#bdc3c7")
        lbl_sub.place(relx=0.5, rely=0.5, anchor="center")

    def init(self):
        self.loginView = LoginPanel(self.parent, self)
        self.parent.addRightPanel(self.loginView)

    def userLogin(self, username, role):
        if role == constants.STAFF:
            staff = OptionsPanelStaff(self.parent, username)
            self.parent.addLeftPanel(staff)
            staff.init()
        elif role == constants.HOSTELLER:
            hosteller = OptionsPanelHosteller(self.parent, username)
            self.parent.addLeftPanel(hosteller)
            hosteller.init()