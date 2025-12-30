import tkinter as tk
from cProfile import label

import constants
from mitulPanels import *
import tk_modified as tk2
from login_panel import LoginPanel
#from add_staff_panel import AddStaffPanel
from src.staff import *


class OptionsPanelStaff(tk.Frame):
    def __init__(self, parent,username):
        super().__init__(parent, width=300, height=850)
        self.pack_propagate(False)
        self.config(bg="lightgreen")
        self.parent = parent
        self.panel_dict = {
            'allocate_room': AllocateRoomPanel(parent),
            'add_building':AddBuildingPanel (parent),
            'view_bills':ViewBillsPanel (parent),
            'update_bill':UpdateBillPanel(parent),
            'view_complaints':ViewComplaintsPanel_(parent),
          #  'raise_complaint': RaiseComplaintPanel(parent),
            'ISSUE_NOTICE': ISSUENOTICEPANEL(parent),
            'update_complaint': UpdateComplaintPanel(parent),
            'view_bills': ViewBillsPanel(parent),
          #  'pay_bill': PayBillPanel(parent),
            'view_notices': ViewNoticesPanel___(parent),
            'VIEW_MENU': VIEWMENUPANEL(parent),
            'UPDATE_MENU': UPDATEMENUPANEL(parent),
            'MESSATTENDANCE': MESSATTENDANCEPANEL(parent),
            'MESSATTENDANCEMARK': MESSATTENDANCEPANEL(parent)
        }

        # self.buttons = {
        #     "View Complaints": lambda: parent.addRightPanel(self.panel_dict['view_complaints']),
        #     "Raise Complaint": lambda: parent.addRightPanel(self.panel_dict['raise_complaint']),
        #     "Update Complaint": lambda: parent.addRightPanel(self.panel_dict['update_complaint']),
        #     "View Bills": lambda: parent.addRightPanel(self.panel_dict['view_bills']),
        #     "Pay Bill": lambda: parent.addRightPanel(self.panel_dict['pay_bill']),
        #     "View Notices": lambda: parent.addRightPanel(self.panel_dict['view_notices'])
        # }
        #
        self.user_label = tk.Label(self,text="Howdy "+username+"!",font=('Arial', 10))
        self.user_label.pack(padx=5,pady=30)
        self.buttons = {
            "allocate room": lambda: parent.addRightPanel( AllocateRoomPanel(parent)),
            "add building":lambda: parent.addRightPanel( AddBuildingPanel(parent)),
            "View Bills": lambda: parent.addRightPanel(ViewBillsPanel(parent)),
            "update bills": lambda: parent.addRightPanel(UpdateBillPanel(parent)),
            "view complaint": lambda: parent.addRightPanel(ViewComplaintsPanel_(parent)),
          #  "Raise Complaint": lambda: parent.addRightPanel(RaiseComplaintPanel(parent)),
            "Update Complaint": lambda: parent.addRightPanel(UpdateComplaintPanel(parent)),
            "VIEW MENU": lambda: parent.addRightPanel(VIEWMENUPANEL(parent)),
            "ADD_TO_MENU": lambda: parent.addRightPanel(UPDATEMENUPANEL(parent)),
            "VIEW MESS ATTENDANCE": lambda: parent.addRightPanel(MESSATTENDANCEPANEL(parent)),
            "MARK_MESS_ATTENDANCE": lambda: parent.addRightPanel(MESSATTENDANCEMARKPANEL(parent)),
            "ISSUE NOTICE":lambda: parent.addRightPanel(ISSUENOTICEPANEL(parent)),
        #    "Pay Bill": lambda: parent.addRightPanel(PayBillPanel(parent)),
            "View Notices": lambda: parent.addRightPanel(ViewNoticesPanel___(parent)),
            "View Profile": lambda: parent.addRightPanel(ViewProfilePanel(parent)),
            "Update Profile": lambda: parent.addRightPanel(UpdateProfilePanel(parent)),
            "Log out": lambda: self.userLogout()
        }

        for text, command in self.buttons.items():
            tk2.ButtonField(self, text=text, command=command).pack(pady=10)
    def init(self):
        self.parent.addRightPanel(self.panel_dict['view_notices'])

    def userLogout(self,):
            guest = OptionsPanelGuest(self.parent)
            print("here")
            self.parent.addLeftPanel(guest)
            guest.init()


#---------------------------------------------------------------------------#


class OptionsPanelHosteller(tk.Frame):
    def __init__(self, parent,username):
        super().__init__(parent, width=300, height=750)
        self.pack_propagate(False)
        self.config(bg="lightgreen")
        self.parent = parent
        self.panel_dict = {
            'view_complaints': ViewComplaintsPanel_(parent),
            'raise_complaint': RaiseComplaintPanel(parent),
            'update_complaint': UpdateComplaintPanel(parent),
            'view_bills': ViewBillsPanel(parent),
            'pay_bill': PayBillPanel(parent),
            'view_notices': ViewNoticesPanel___(parent),
        }

        # self.buttons = {
        #     "View Complaints": lambda: parent.addRightPanel(self.panel_dict['view_complaints']),
        #     "Raise Complaint": lambda: parent.addRightPanel(self.panel_dict['raise_complaint']),
        #     "Update Complaint": lambda: parent.addRightPanel(self.panel_dict['update_complaint']),
        #     "View Bills": lambda: parent.addRightPanel(self.panel_dict['view_bills']),
        #     "Pay Bill": lambda: parent.addRightPanel(self.panel_dict['pay_bill']),
        #     "View Notices": lambda: parent.addRightPanel(self.panel_dict['view_notices'])
        # }
        #
        self.user_label = tk.Label(self,text="Howdy "+username+"!",font=('Arial', 20))
        self.user_label.pack(padx=5,pady=30)
        self.buttons = {
            "View Complaints": lambda: parent.addRightPanel(ViewComplaintsPanel_(parent)),
            "Raise Complaint": lambda: parent.addRightPanel(RaiseComplaintPanel(parent)),
            "Update Complaint": lambda: parent.addRightPanel(UpdateComplaintPanel(parent)),
            "View Bills": lambda: parent.addRightPanel(ViewBillsPanel(parent)),
            "Pay Bill": lambda: parent.addRightPanel(PayBillPanel(parent)),
            "View Notices": lambda: parent.addRightPanel(ViewNoticesPanel___(parent)),
            "View Profile": lambda: parent.addRightPanel(ViewProfilePanel(parent)),
            "Update Profile": lambda: parent.addRightPanel(UpdateProfilePanel(parent)),
            "Log out": lambda: self.userLogout()
        }

        for text, command in self.buttons.items():
            tk2.ButtonField(self, text=text, command=command).pack(pady=10)
    def init(self):
        self.parent.addRightPanel(self.panel_dict['view_notices'])

    def userLogout(self,):
            guest = OptionsPanelGuest(self.parent)
            print("here")
            self.parent.addLeftPanel(guest)
            guest.init()




class OptionsPanelGuest(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent,width=300, height=750)
        self.parent = parent
        self.pack_propagate(False)
        self.config(bg="lightgreen")

        self.loginView = None
        # tab for warden/admin
        self.label = tk.Label(self,text="Welcome to \nHostel \nManagement \nSystem",font=('Arial', 20))
        self.label.pack(padx=30,pady=30)

    def init(self,):
        self.parent = self.parent
        self.loginView = LoginPanel(self.parent,self)
        self.parent.addRightPanel(self.loginView)


#class OptionsPanelGuest(tk.Frame):
    def userLogin(self, username, role):
        if role == constants.STAFF:
            staff = OptionsPanelStaff(self.parent, username)  # Pass 'role' here
            self.parent.addLeftPanel(staff)
            staff.init()
        elif role == constants.HOSTELLER:
            hosteller = OptionsPanelHosteller(self.parent, username)
            self.parent.addLeftPanel(hosteller)
            hosteller.init()


