import tkinter as tk

from src.login_panel import LoginPanel
from src.options_panel import OptionsPanelGuest
from src.panels_jithin import *

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizing Panels with Classes")
        self.geometry("1300x900")
        self.minsize(1300,900)
        self.right_panel = None
        self.options_panel = OptionsPanelGuest(self)
        self.options_panel.init()
        self.options_panel.pack(side='left')
    def addRightPanel(self,panel_right):
        try:
            self.right_panel.destroy()
        except Exception as error:
            pass
        self.right_panel=panel_right
        self.right_panel.pack(padx=10, pady=10,side='right')

    def addLeftPanel(self,panel_option):
        try:
            self.options_panel.destroy()
        except Exception as error:
            None
        self.options_panel=panel_option
        self.options_panel.pack(padx=10, pady=10,side='left')





class Panel1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent,width=1000, height=750)
        self.pack_propagate(False)
        self.config(bg="lightgreen")
        # add your designs in this function


# create panels for each of the pages as classes and write the design inside __init__() function
# Main execution
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
