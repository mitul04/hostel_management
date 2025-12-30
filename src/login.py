import tkinter as tk
from tkinter import ttk
import db
import constants

class LoginPanel(tk.Frame):
    def __init__(self, parent, options_panel):
        super().__init__(parent, width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="#f0f0f0")  # Clean light gray background
        self.options_panel = options_panel

        # --- STYLE CONFIGURATION ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="white", font=("Segoe UI", 11))
        style.configure("Header.TLabel", background="#2c3e50", foreground="white", font=("Segoe UI", 24, "bold"))
        style.configure("Card.TFrame", background="white")
        style.configure("TButton", font=("Segoe UI", 11), padding=5)

        # --- CENTERED LOGIN CARD ---
        # We use a 'place' strategy here just once to perfectly center the card in the middle of the screen
        self.card_frame = ttk.Frame(self, style="Card.TFrame", padding=40)
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center")

        # --- TITLE ---
        lbl_title = tk.Label(self.card_frame, text="LOGIN", font=("Segoe UI", 22, "bold"), bg="white", fg="#2c3e50")
        lbl_title.pack(pady=(0, 20))

        # --- USERNAME FIELD ---
        lbl_user = ttk.Label(self.card_frame, text="Username:")
        lbl_user.pack(fill="x", pady=(10, 5))
        
        self.entry_username = ttk.Entry(self.card_frame, width=30, font=("Segoe UI", 12))
        self.entry_username.pack(fill="x", pady=(0, 10))

        # --- PASSWORD FIELD ---
        lbl_pass = ttk.Label(self.card_frame, text="Password:")
        lbl_pass.pack(fill="x", pady=(10, 5))
        
        self.entry_password = ttk.Entry(self.card_frame, width=30, font=("Segoe UI", 12), show="*")
        self.entry_password.pack(fill="x", pady=(0, 20))

        # --- BUTTONS ---
        btn_frame = tk.Frame(self.card_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)

        # clear button (secondary)
        self.clear_button = ttk.Button(btn_frame, text="Clear", command=self.clear)
        self.clear_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

        # login button (primary)
        self.login_button = ttk.Button(btn_frame, text="Login", command=self.login)
        self.login_button.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # --- FOOTER ---
        footer_text = "Contact admin for password resetting"
        self.title_1 = tk.Label(self.card_frame, text=footer_text, font=("Segoe UI", 9), bg="white", fg="gray")
        self.title_1.pack(pady=(20, 0))

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        # Ensure db.login is robust; if it fails, the app might crash
        try:
            role = db.login(username, password)
            if role in (constants.HOSTELLER, constants.STAFF):
                self.options_panel.userLogin(username, role)
            else:
                # Optional: Show visual feedback if login fails (e.g., shake or red text)
                print("Invalid login credentials") 
        except Exception as e:
            print(f"Login Error: {e}")

    def clear(self):
        self.entry_password.delete(0, tk.END)
        self.entry_username.delete(0, tk.END)