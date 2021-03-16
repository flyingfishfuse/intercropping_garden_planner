from tkinter import *
class ConfigurationWindow:

    def __init__(self, master):
        self.master = master
        self.master.title("Configuration Window")
        self.master.geometry("400x100+200+200")
        self.show_widgets()

    def show_widgets(self):
        "A frame with a button to quit the window"
        self.frame = Frame(self.master)
        self.quit_button = Button(self.frame, text=f"Quit this window",command=self.close_window)
        self.quit_button.pack()
        #self.create_button("Open Plant list database", PlantListWindow)
        self.frame.pack()

    def close_window(self):
        self.master.destroy()