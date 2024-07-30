from tkinter import *
from constants import *
from subprocess import call
import pandas as pd

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   
   def checkboxState(self):
      return map((lambda var: var.get()), self.vars)
      
if __name__ == '__main__':
   app = Tk()
   app.title('Select desired button layout')
   btnToggle = Checkbar(app, ['Vertical Navigation', 'Markers', 'Start/End Marker', 'Survey','Undo/Redo'])
   btnToggle.pack(side='top')
   btnToggle.config(relief=GROOVE, bd=2)
   def allcheckboxStates(): 
      buttons = list(btnToggle.checkboxState())
      print(buttons)
      df = pd.DataFrame({'Buttons' : buttons})
      df.to_csv('buttons.csv') 
      call(["python3", 'wayfind.py'])
   Button(app, text='Launch', command=allcheckboxStates).pack()
   app.eval('tk::PlaceWindow . center')
   app.mainloop()