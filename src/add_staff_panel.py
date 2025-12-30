import tkinter as tk
from tkinter import ttk

class AddStaffPanel(tk.Frame):
    def __init__(self, parent, options_panel):
        super().__init__(parent)
        self.pack_propagate(False)
        self.config(bg="#f0f0f0")  # Clean light gray background
        self.options_panel = options_panel

        # --- STYLE CONFIGURATION ---
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
        style.configure("TRadiobutton", background="#f0f0f0", font=("Segoe UI", 11))

        # --- HEADER ---
        header_frame = tk.Frame(self, bg="#2c3e50", height=70)
        header_frame.pack(fill="x", side="top")
        
        lbl_title = tk.Label(header_frame, text="ADD STAFF MEMBER", 
                             font=("Segoe UI", 18, "bold"), 
                             bg="#2c3e50", fg="white")
        lbl_title.pack(pady=15)

        # --- SCROLLABLE CONTENT (Optional but good for small screens) ---
        # For now, we will use a central frame
        content_frame = tk.Frame(self, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=50, pady=20)

        # --- FORM FIELDS ---
        # (Label Text, Variable Name, Show Password?)
        form_fields = [
            ("Full Name:", "entry_name", False),
            ("Aadhar Number:", "entry_aadhar", False),
            ("Mobile Number:", "entry_mobile", False),
            ("House Name:", "entry_house_name", False),
            ("House No:", "entry_house_no", False),
            ("Street:", "entry_street", False),
            ("District:", "entry_district", False),
            ("State:", "entry_state", False),
            ("Pin Code:", "entry_pin", False),
            ("Username:", "entry_username", False),
            ("Password:", "entry_password", True)
        ]

        self.entries = {}  # Store entry widgets to access them later

        # Generate form using Grid
        for i, (text, key, is_password) in enumerate(form_fields):
            # Label
            lbl = ttk.Label(content_frame, text=text)
            lbl.grid(row=i, column=0, sticky="e", padx=15, pady=8)

            # Entry
            if is_password:
                ent = ttk.Entry(content_frame, width=35, show="*")
            else:
                ent = ttk.Entry(content_frame, width=35)
            
            ent.grid(row=i, column=1, sticky="w", padx=15, pady=8)
            self.entries[key] = ent
            
            # Map old variable names to new dictionary for compatibility if needed
            setattr(self, key, ent) 

        # --- ROLE SELECTION ---
        row_idx = len(form_fields)
        lbl_role = ttk.Label(content_frame, text="Role:")
        lbl_role.grid(row=row_idx, column=0, sticky="e", padx=15, pady=8)

        radio_frame = tk.Frame(content_frame, bg="#f0f0f0")
        radio_frame.grid(row=row_idx, column=1, sticky="w", padx=15, pady=8)

        self.role_var = tk.StringVar(value="User")
        
        # Fixed logic: Values are now distinct (Warden vs Chef vs Admin)
        roles = [("User", "User"), ("Warden", "Warden"), ("Chef", "Chef"), ("Admin", "Admin")]
        
        for text, value in roles:
            rbtn = ttk.Radiobutton(radio_frame, text=text, variable=self.role_var, value=value)
            rbtn.pack(side="left", padx=10)

        # --- BUTTONS ---
        btn_frame = tk.Frame(content_frame, bg="#f0f0f0")
        btn_frame.grid(row=row_idx + 1, column=0, columnspan=2, pady=30)

        self.add_button = ttk.Button(btn_frame, text="Add Staff", width=15)
        self.add_button.pack(side="left", padx=10)

        self.clear_button = ttk.Button(btn_frame, text="Clear Form", width=15)
        self.clear_button.pack(side="left", padx=10)