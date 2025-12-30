import tkinter as tk
import tk_modified as tk2
class AddStaffPanel(tk.Frame):
    def __init__(self, parent,options_panel):
        super().__init__(parent,width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="cyan")

        self.options_panel = options_panel
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
