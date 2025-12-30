import tkinter as tk
import tk_modified as tk2
from datetime import datetime


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizing Panels with Classes")
        self.geometry("1300x900")
        self.minsize(1300,900)

        self.options_panel = OptionsPanelStaff(self)
        self.options_panel.pack(side='left')

        self.right_panel = AddStaffPanel(self)
        self.right_panel.pack(padx=10, pady=10,side='right')

        self.dict = {'staffprofile': ProfileStaffPanel(self)}



class OptionsPanelStaff(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent,width=300, height=750)
        self.pack_propagate(False)
        self.config(bg="lightgreen")

        # tab for warden/admin
        self.hosteller = tk2.ButtonField(self,text="Hosteller")
        self.hosteller.pack(pady=10)
        self.rooms = tk2.ButtonField(self,text="Rooms")
        self.rooms.pack(pady=10)

        # tab for admin
        self.bill = tk2.ButtonField(self,text="Bills")
        self.bill.pack(pady=10)

        # tab for cheff/admin
        self.mess = tk2.ButtonField(self,text="Mess")
        self.mess.pack(pady=10)


        # common tabs
        self.complaints = tk2.ButtonField(self, text="Complaints")
        self.complaints.pack(pady=10)
        self.profile = tk2.ButtonField(self,text="Profile")
        self.profile.pack(pady=10)
        self.logout = tk2.ButtonField(self,text="Log out")
        self.logout.pack(pady=10)




class ProfileStaffPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent,width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="blue")

        self.label_name = tk2.LabelField(self, text="Name:")
        self.label_name.place(x=30, y=80)

        self.entry_name = tk2.LabelField(self,text="Mitul")
        self.entry_name.place(x=130, y=80)

class AddStaffPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent,width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="cyan")

        self.label_name = tk2.LabelField(self, text="Name:")
        self.label_name.place(x=30, y=80)

        self.entry_name = tk2.EntryField(self)
        self.entry_name.place(x=130, y=80)

        self.label_aadhar = tk2.LabelField(self, text="Aadhar:")
        self.label_aadhar.place(x=30, y=130)

        self.entry_aadhar = tk2.EntryField(self)
        self.entry_aadhar.place(x=130, y=130)

        self.label_mobile = tk2.LabelField(self, text="Mobile:")
        self.label_mobile.place(x=30, y=160)

        self.entry_mobile = tk2.EntryField(self)
        self.entry_mobile.place(x=130, y=160)

        self.label_role = tk2.LabelField(self, text="Role:")
        self.label_role.place(x=30, y=200)

        self.label_house_name = tk2.LabelField(self, text="House name:")
        self.label_house_name.place(x=30, y=240)

        self.entry_house_name = tk2.EntryField(self)
        self.entry_house_name.place(x=130, y=240)

        self.label_house_no = tk2.LabelField(self, text="House no:")
        self.label_house_no.place(x=30, y=280)

        self.entry_house_no = tk2.EntryField(self)
        self.entry_house_no.place(x=130, y=280)

        self.label_street = tk2.LabelField(self, text="Street:")
        self.label_street.place(x=30, y=320)

        self.entry_street = tk2.EntryField(self)
        self.entry_street.place(x=130, y=320)

        self.label_district = tk2.LabelField(self, text="District:")
        self.label_district.place(x=30, y=360)

        self.entry_district = tk2.EntryField(self)
        self.entry_district.place(x=130, y=360)

        self.label_state = tk2.LabelField(self, text="State:")
        self.label_state.place(x=30, y=400)

        self.entry_state = tk2.EntryField(self)
        self.entry_state.place(x=130, y=400)

        self.label_pin = tk2.LabelField(self, text="Pin code:")
        self.label_pin.place(x=30, y=440)

        self.entry_pin = tk2.EntryField(self)
        self.entry_pin.place(x=130, y=440)

        self.label_username = tk2.LabelField(self, text="Username:")
        self.label_username.place(x=30, y=480)

        self.entry_username = tk2.EntryField(self)
        self.entry_username.place(x=130, y=480)

        self.label_password = tk2.LabelField(self, text="Password:")
        self.label_password.place(x=30, y=480)

        self.entry_password = tk2.EntryField(self)
        self.entry_password.place(x=130, y=480)



        self.role_var = tk.StringVar(value="User")  # Default value

        self.radio_user = tk.Radiobutton(self, text="User", variable=self.role_var, value="User", font=('Arial', 12))
        self.radio_user.place(x=130, y=200)

        self.radio_warden = tk.Radiobutton(self, text="Warden", variable=self.role_var, value="Admin", font=('Arial', 12))
        self.radio_warden.place(x=200, y=200)

        self.radio_cheff = tk.Radiobutton(self, text="Cheff", variable=self.role_var, value="Admin", font=('Arial', 12))
        self.radio_cheff.place(x=292, y=200)

        self.radio_admin = tk.Radiobutton(self, text="Admin", variable=self.role_var, value="Admin", font=('Arial', 12))
        self.radio_admin.place(x=366, y=200)

        self.clear_button = tk.Button(self, text="Clear", width=10, font=('Arial', 12))
        self.clear_button.place(x=40, y=520)
        self.add_button = tk.Button(self, text="Add", width=10, font=('Arial', 12))
        self.add_button.place(x=180, y=520)

        self.title = tk.Label(self, text="ADD STAFF", font=('Arial', 16))
        self.title.place(x=80, y=40)


class UpdateStaffPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent,width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="magenta")

        self.label_name = tk2.LabelField(self, text="Name:")
        self.label_name.place(x=30, y=80)

        self.entry_name = tk2.EntryField(self)
        self.entry_name.place(x=130, y=80)

        self.label_aadhar = tk2.LabelField(self, text="Aadhar:")
        self.label_aadhar.place(x=30, y=130)

        self.entry_aadhar = tk2.EntryField(self)
        self.entry_aadhar.place(x=130, y=130)

        self.label_mobile = tk2.LabelField(self, text="Mobile:")
        self.label_mobile.place(x=30, y=160)

        self.entry_mobile = tk2.EntryField(self)
        self.entry_mobile.place(x=130, y=160)

        self.label_role = tk2.LabelField(self, text="Role:")
        self.label_role.place(x=30, y=200)

        self.label_house_name = tk2.LabelField(self, text="House name:")
        self.label_house_name.place(x=30, y=240)

        self.entry_house_name = tk2.EntryField(self)
        self.entry_house_name.place(x=130, y=240)

        self.label_house_no = tk2.LabelField(self, text="House no:")
        self.label_house_no.place(x=30, y=280)

        self.entry_house_no = tk2.EntryField(self)
        self.entry_house_no.place(x=130, y=280)

        self.label_street = tk2.LabelField(self, text="Street:")
        self.label_street.place(x=30, y=320)

        self.entry_street = tk2.EntryField(self)
        self.entry_street.place(x=130, y=320)

        self.label_district = tk2.LabelField(self, text="District:")
        self.label_district.place(x=30, y=360)

        self.entry_district = tk2.EntryField(self)
        self.entry_district.place(x=130, y=360)

        self.label_state = tk2.LabelField(self, text="State:")
        self.label_state.place(x=30, y=400)

        self.entry_state = tk2.EntryField(self)
        self.entry_state.place(x=130, y=400)

        self.label_pin = tk2.LabelField(self, text="Pin code:")
        self.label_pin.place(x=30, y=440)

        self.entry_pin = tk2.EntryField(self)
        self.entry_pin.place(x=130, y=440)

        self.label_username = tk2.LabelField(self, text="Username:")
        self.label_username.place(x=30, y=480)

        self.entry_username = tk2.EntryField(self)
        self.entry_username.place(x=130, y=480)

        self.label_password = tk2.LabelField(self, text="Password:")
        self.label_password.place(x=30, y=480)

        self.entry_password = tk2.EntryField(self)
        self.entry_password.place(x=130, y=480)



        self.role_var = tk.StringVar(value="User")  # Default value

        self.radio_user = tk.Radiobutton(self, text="User", variable=self.role_var, value="User", font=('Arial', 12))
        self.radio_user.place(x=130, y=200)

        self.radio_warden = tk.Radiobutton(self, text="Warden", variable=self.role_var, value="Admin", font=('Arial', 12))
        self.radio_warden.place(x=200, y=200)

        self.radio_cheff = tk.Radiobutton(self, text="Cheff", variable=self.role_var, value="Admin", font=('Arial', 12))
        self.radio_cheff.place(x=292, y=200)

        self.radio_admin = tk.Radiobutton(self, text="Admin", variable=self.role_var, value="Admin", font=('Arial', 12))
        self.radio_admin.place(x=366, y=200)

        self.clear_button = tk.Button(self, text="Clear", width=10, font=('Arial', 12))
        self.clear_button.place(x=40, y=520)
        self.add_button = tk.Button(self, text="Add", width=10, font=('Arial', 12))
        self.add_button.place(x=180, y=520)

        self.title = tk.Label(self, text="UPDATE STAFF", font=('Arial', 16))
        self.title.place(x=80, y=40)




class AddHostellerPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent,width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="yellow")

        self.label_name = tk2.LabelField(self, text="Name:")
        self.label_name.place(x=30, y=80)

        self.entry_name = tk2.EntryField(self)
        self.entry_name.place(x=130, y=80)

        self.label_aadhar = tk2.LabelField(self, text="Aadhar:")
        self.label_aadhar.place(x=30, y=130)

        self.entry_aadhar = tk2.EntryField(self)
        self.entry_aadhar.place(x=130, y=130)


        self.label_mobile = tk2.LabelField(self, text="Mobile:")
        self.label_mobile.place(x=30, y=160)

        self.entry_mobile = tk2.EntryField(self)
        self.entry_mobile.place(x=130, y=160)

        self.label_dob = tk2.LabelField(self, text="DOB:")
        self.label_dob.place(x=30, y=200)

        self.entry_dob = tk2.EntryField(self)
        self.entry_dob.place(x=130, y=200)

        self.label_house_name = tk2.LabelField(self, text="House name:")
        self.label_house_name.place(x=30, y=240)

        self.entry_house_name = tk2.EntryField(self)
        self.entry_house_name.place(x=130, y=240)

        self.label_house_no = tk2.LabelField(self, text="House no:")
        self.label_house_no.place(x=30, y=280)

        self.entry_house_no = tk2.EntryField(self)
        self.entry_house_no.place(x=130, y=280)

        self.label_street = tk2.LabelField(self, text="Street:")
        self.label_street.place(x=30, y=320)

        self.entry_street = tk2.EntryField(self)
        self.entry_street.place(x=130, y=320)

        self.label_district = tk2.LabelField(self, text="District:")
        self.label_district.place(x=30, y=360)

        self.entry_district = tk2.EntryField(self)
        self.entry_district.place(x=130, y=360)

        self.label_state = tk2.LabelField(self, text="State:")
        self.label_state.place(x=30, y=400)

        self.entry_state = tk2.EntryField(self)
        self.entry_state.place(x=130, y=400)

        self.label_pin = tk2.LabelField(self, text="Pin code:")
        self.label_pin.place(x=30, y=440)

        self.entry_pin = tk2.EntryField(self)
        self.entry_pin.place(x=130, y=440)

        self.label_username = tk2.LabelField(self, text="Username:")
        self.label_username.place(x=30, y=480)

        self.entry_username = tk2.EntryField(self)
        self.entry_username.place(x=130, y=480)

        self.label_password = tk2.LabelField(self, text="Password:")
        self.label_password.place(x=30, y=480)

        self.entry_password = tk2.EntryField(self)
        self.entry_password.place(x=130, y=480)


        self.label_guardian_name = tk2.LabelField(self, text="Guardian name:")
        self.label_guardian_name.place(x=350, y=80)

        self.entry_guardian_name = tk2.EntryField(self)
        self.entry_guardian_name.place(x=480, y=80)

        self.label_guardian_phone = tk2.LabelField(self, text="Guardian phone:")
        self.label_guardian_phone.place(x=350, y=120)

        self.entry_guardian_phone = tk2.EntryField(self)
        self.entry_guardian_phone.place(x=480, y=120)


        self.label_join_date = tk2.LabelField(self, text="Join date:")
        self.label_join_date.place(x=350, y=160)

        self.entry_join_date = tk2.EntryField(self)
        self.entry_join_date.place(x=480, y=160)


        self.clear_button = tk.Button(self, text="Clear", width=10, font=('Arial', 12))
        self.clear_button.place(x=40, y=520)
        self.add_button = tk.Button(self, text="Add", width=10, font=('Arial', 12))
        self.add_button.place(x=180, y=520)

        self.title = tk.Label(self, text="ADD HOSTELLER", font=('Arial', 16))
        self.title.place(x=80, y=40)

# create panels for each of the pages as classes and write the design inside __init__() function
# Main execution
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()