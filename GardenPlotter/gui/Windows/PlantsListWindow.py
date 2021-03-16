from tkinter import *
class PlantListWindow:
    def __init__(self, master,size):
        self.master = master
        self.master.title("All my Plants")
        self.master.geometry(size)
        self.frame = Frame(self.master)

        self.quit  = Button(self.frame, text=f"Quit this window" ,command=self.close_window)
        self.quit.pack()
        self.label = Label(self.frame, text="PlantListWindow")
        self.label.pack()
        self.frame.pack()

    def close_window(self):
        self.master.destroy()