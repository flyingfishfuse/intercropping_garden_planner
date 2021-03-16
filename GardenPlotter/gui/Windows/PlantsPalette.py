class PlantsPalette(MainWindow):
    def __init__(self, master, size):
        self.master = master
        self.master.title("Plant selection")
        self.master.geometry(size)
        self.show_widgets()

    def show_widgets(self):
        self.frame = Frame(self.master)
        self.quit  = Button(self.frame, text=f"Quit this window" ,command=self.close_window)
        self.quit.pack()
        self.label = Label(self.frame, text="THIS IS THE PALETTE")
        self.label.pack()
        self.frame.pack()
        
    def close_window(self):
        self.master.destroy()