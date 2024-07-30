from constants import *
import pandas as pd
import tkinter as tk
from subprocess import call
from functools import partial

class runApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.btnFrame = tk.Frame(self)
        self.liveTrack = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Live Tracking", command=partial(self.openFile,'metawindow_wayfind.py'))
        self.validation = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Validation", command=partial(self.openFile,'validation_wayfind.py'))
        self.analysis = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Analysis", command=partial(self.openFile,'analysis_wayfind.py'))
        self.btnFrame.pack()
        self.liveTrack.pack(side = 'top', pady = (BTN_SPACING,BTN_SPACING), padx = (3*BTN_SPACING,3*BTN_SPACING))
        self.validation.pack(side = 'top', pady = (BTN_SPACING,BTN_SPACING), padx = (3*BTN_SPACING,3*BTN_SPACING))
    
    def openFile(self, filename):
        call(["python3", filename])

if __name__ == "__main__":
    app = runApp()
    app.title('Select mode')
    app.iconbitmap(r'images/dail.ico')
    app.eval('tk::PlaceWindow . center')
    app.mainloop()