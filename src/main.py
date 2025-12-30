import tkinter as tk
from tkinter import ttk
from navigation import OptionsPanelGuest

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hostel Management System")
        self.geometry("1300x900")
        self.minsize(1300, 900)
        self.config(bg="#f0f0f0") # Light gray background for the main window container

        # --- GLOBAL STYLES ---
        self.setup_styles()

        # --- STATE MANAGEMENT ---
        self.right_panel = None
        self.navigation = None

        # --- INITIALIZATION ---
        # Load the Guest Sidebar (Left) which allows Login
        guest_panel = OptionsPanelGuest(self)
        self.addLeftPanel(guest_panel)
        
        # Trigger the initial view (usually the Login Screen)
        guest_panel.init()

    def setup_styles(self):
        """Defines the modern look and feel for the whole app"""
        style = ttk.Style()
        style.theme_use('clam') # 'clam' allows us to change colors easily

        # General Font
        default_font = ("Segoe UI", 11)
        bold_font = ("Segoe UI", 11, "bold")

        # Configure TButton (Standard Buttons)
        style.configure("TButton", font=bold_font, padding=6, borderwidth=0)
        style.map("TButton", background=[('active', '#bdc3c7')]) # Gray hover effect

        # Configure TLabel (Standard Text)
        style.configure("TLabel", font=default_font, background="#f0f0f0")

        # Configure Entry (Input boxes)
        style.configure("TEntry", padding=5)

        # Configure Sidebar Buttons (Dark Blue)
        style.configure("Sidebar.TButton", 
                        font=("Segoe UI", 11), 
                        background="#34495e", 
                        foreground="white", 
                        borderwidth=0,
                        anchor="center")
        style.map("Sidebar.TButton", 
                  background=[('active', '#1abc9c')], # Teal hover
                  foreground=[('active', 'white')])

    def addLeftPanel(self, panel_widget):
        """Switches the Sidebar (Left)"""
        if self.navigation is not None:
            self.navigation.destroy()
        
        self.navigation = panel_widget
        # Sidebar fills vertically (Y) but doesn't expand horizontally
        self.navigation.pack(side='left', fill='y')

    def addRightPanel(self, panel_widget):
        """Switches the Content Area (Right)"""
        if self.right_panel is not None:
            self.right_panel.destroy()
        
        self.right_panel = panel_widget
        # Content fills both directions and expands to take available space
        self.right_panel.pack(side='right', fill='both', expand=True, padx=20, pady=20)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()