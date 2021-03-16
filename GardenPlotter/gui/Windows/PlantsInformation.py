from tkinter import *

class PlantInformationWindow:
    def __init__(self, master, size, plant_to_display):
        self.master = master
        self.master.title("Plant Information")
        self.master.geometry(size)
        self.show_widgets()

    def show_widgets(self):
        self.frame = Frame(self.master)
        self.quit  = Button(self.frame, text=f"Quit this window" ,command=self.close_window)
        self.quit.pack()
        self.label = Label(self.frame, text="THIS IS ONLY IN THE INFORMATION WINDOW")
        self.label.pack()
        self.frame.pack()
        
    def close_window(self):
        self.master.destroy()