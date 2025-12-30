import  tkinter as tk
import tk_modified as tk2
import db
import constants
class LoginPanel(tk.Frame):
    def __init__(self, parent,options_panel):
        super().__init__(parent,width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightgreen")

        self.options_panel = options_panel

        self.title = tk.Label(self, text="LOGIN", font=('Arial', 16))
        self.title.place(x=80, y=40)

        # Create labels and entries for username and password
        self.label_username = tk2.LabelField(self, text="Username:")
        self.label_username.place(x=30, y=80)

        self.entry_username = tk2.EntryField(self)
        self.entry_username.place(x=130, y=80)

        self.label_password = tk2.LabelField(self,text="Password")
        self.label_password.place(x=30, y=130)

        self.entry_password = tk2.EntryField(self, show='*')
        self.entry_password.place(x=130, y=130)

        # Create login button
        self.login_button = tk.Button(self, text="Login", command=self.login, width=10, font=('Arial', 12))
        self.login_button.place(x=180, y=160)

        self.clear_button = tk.Button(self, text="Clear", command=self.clear, width=10, font=('Arial', 12))
        self.clear_button.place(x=50, y=160)

        self.title_1 = tk.Label(self, text="Contact admin for password resetting", font=('Arial', 12))
        self.title_1.place(x=30,y=200)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        role = db.login(username,password)
        if (role)in (constants.HOSTELLER,constants.STAFF):
            self.options_panel.userLogin(username,role)
    def clear(self):
        self.entry_password.delete(0, tk.END)
        self.entry_username.delete(0, tk.END)



