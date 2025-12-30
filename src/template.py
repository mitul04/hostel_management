import tkinter as tk

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizing Panels with Classes")
        self.geometry("1200x900")
        self.bottom_panel = Panel1(self)
        self.bottom_panel.pack(padx=10, pady=10)


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
