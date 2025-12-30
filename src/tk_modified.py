import tkinter as tk
class ButtonField(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, width=20, font=('Arial', 12), *args, **kwargs)
        self.parent = parent


class EntryField(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, width=20, font=('Arial', 12), *args, **kwargs)
        self.parent = parent


class LabelField(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, font=('Arial', 12), *args, **kwargs)
        self.parent = parent
