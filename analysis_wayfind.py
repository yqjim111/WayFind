import xxlimited
from constants import *
import tkinter as tk
import tkinter.font as TkFont
from tkinter import Toplevel
from tkinter import messagebox
import pandas as pd
import time
import datetime
import logging
from PIL import ImageTk, Image
from functools import partial
import webbrowser

class runApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		print(BUTTONS)
		self.fileNum = 0
		self.floorIndex = 0
		self.pointIndex = 0
		self.actionCount = 0
		self.markerIndex = 0
		self.plotList = []
		self.imgList = []
		self.timeList = []
		self.unixList = []
		self.floorList = []
		self.xList = []
		self.yList = []
		self.signList = []
		self.markerList = []
		self.plotListMistake = []
		self.timeListMistake = []
		self.unixListMistake = []
		self.floorListMistake = []
		self.xListMistake = []
		self.yListMistake = []
		self.signListMistake = []
		self.markerListMistake = []
		self.xAbs = -1 # saves most recent absolute x position for the sign feature. Default is -1.
		self.yAbs = -1 # saves most recent absolute y position for the sign feature. Default is -1.
		for img in IMG_FILES:
		    self.imgList.append(ImageTk.PhotoImage(
		    	Image.open(r'images/'+img).resize((X,Y),Image.ANTIALIAS)))
		# Frames
		self.canvasFrame = tk.Frame(self)
		self.canvasFrame.grid(column = 0, row = 0)
		self.btnFrame = tk.Frame(self)
		self.btnFrame.grid(column = 2, row = 0)
		# Canvases
		self.canvas = tk.Canvas(self.canvasFrame, width=X, height=Y, 
			bd = 2, bg = 'white', cursor = CURSOR_TYPE)
		self.canvas.create_image(X/2,Y/2, anchor = tk.CENTER, image = self.imgList[0])
		self.canvas.bind('<Button-1>', self.plot)
		self.canvas.after(MS_AUTOSAVE, self.autoSave)
		self.canvas.pack()
		self.mytext = tk.Text(self,height=51, width = 26, state="disabled")
		self.mytext.grid(column=1, row=0)
		# Pop-up Message
		self.fnt = TkFont.Font(size = 70)
		self.msgList = []
		self.msgList.append(self.canvas.create_text(X/2,Y/2, text='', font = self.fnt))
		# Top Buttons
		self.ascendBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Ascend", command=self.ascend)
		self.descendBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Descend", command=self.descend)
		# Mid Buttons
		self.markerBtn = tk.Button(self.btnFrame, height = 4*BTN_HEIGHT, width = BTN_WIDTH, 
			text=MARKERS[self.markerIndex].replace(' ','\n'), command=self.rotateMarkerBtn)
		self.prevMarkerBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Prev. Marker", command=self.prevMarker)
		self.nextMarkerBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Next Marker", command=self.nextMarker)
		self.unixBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Show Unix", command=self.showUnix)
		self.signStartBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Sign Start", command=partial(self.addMarker,'Sign Start'))
		self.endBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="END", command=partial(self.addMarker,'END'))
		self.surveyBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Survey", command=partial(self.popup, 'general'))
		# Bottom Buttons
		self.undoBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Undo", command=partial(self.plotMistake,True))
		self.redoBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Redo", command=partial(self.plotMistake,False))
		self.saveBtn = tk.Button(self.btnFrame, height = BTN_HEIGHT, width = BTN_WIDTH, 
			text="Save", command=self.saveData)
		# Packing 
		if BUTTONS[0] == '1':
			self.ascendBtn.pack(side = 'top')
			self.descendBtn.pack(side = 'top', pady = (0,BTN_SPACING))
		if BUTTONS[1] == '1':
			self.markerBtn.pack(side = 'top')
			self.prevMarkerBtn.pack(side = 'top')
			self.nextMarkerBtn.pack(side = 'top', pady = (0,BTN_SPACING))
		if BUTTONS[2] == '1':
			self.signStartBtn.pack(side = 'top')
			self.endBtn.pack(side = 'top')
		if BUTTONS[3] == '1':
			self.surveyBtn.pack(side = 'top', pady = (0,BTN_SPACING))
			self.undoBtn.pack(side = 'top')
		if BUTTONS[4] == '1':
			self.redoBtn.pack(side = 'top')
			self.saveBtn.pack(side = 'top')
		self.after(MSG_TIME,self.deleteBtnMsg)
	
	# displays button press as message on-screen
	def btnMsg(self, button):
		self.msgList.append(self.canvas.create_text(X/2,Y/2,
                        text=button, font = self.fnt))
		module_logger.info(button)
		self.mytext.see('end')

	# deletes any on-screen button messages
	def deleteBtnMsg(self):
		if(len(self.msgList) > 0):
			for i in self.msgList:
				self.canvas.delete(i)
		self.after(MSG_TIME,self.deleteBtnMsg)

	# opens data entry popup
	def popup(self, survey_num):
		self.w = popupWindow(self, survey_num)
		self.w.b["state"] = "normal"
		self.wait_window(self.w.top)
		inVal = ''
		try:
			inVal = str(self.w.value)
		except:
			inVal = 'none'
		self.btnMsg(str(inVal))
		return inVal

	# ascend/go up a floor
	def ascend(self):
		self.floorIndex += 1
		if self.floorIndex == len(self.imgList):
			self.floorIndex -= 1
			print("We can't go up higher!")
		self.clearCanvas()
		self.actionCount = 0
		self.btnMsg('Ascend')

	# descend/go down a floor
	def descend(self):
		self.floorIndex -= 1
		if self.floorIndex < 0:
			self.floorIndex = 0
			print("We can't go down further!")
		self.clearCanvas()
		self.actionCount = 0
		self.btnMsg('Descend')

	# display unix time
	def showUnix(self):
		self.btnMsg(str(int(time.time())))

	# go to the preivous marker button
	def prevMarker(self):
		if (self.markerIndex > 0):
			self.markerIndex += -1
			self.markerBtn.config(text=str(MARKERS[self.markerIndex]).replace(' ','\n'))
		else:
			print("Cannot go back. We're at the first button")

	# go to the next marker button
	def nextMarker(self):
		markerBtnText = str(MARKERS[self.markerIndex]).replace(' ','\n')
		if markerBtnText.find('Survey') != -1:
			survey_num = markerBtnText[markerBtnText.find('Survey')+6]
			self.popup(survey_num)
		if (self.markerIndex < len(MARKERS)):
			self.markerIndex += 1
		else:
			self.markerIndex = 0
		markerBtnText = str(MARKERS[self.markerIndex]).replace(' ','\n')
		self.markerBtn.config(text=markerBtnText)

	# add marker and go to next marker
	def rotateMarkerBtn(self):
		self.addMarker(str(MARKERS[self.markerIndex]))
		self.nextMarker()

	# plot a point on the canvas
	def plot(self,event):
		self.actionCounter(True)
		x, y = (event.x), (event.y)
		x += CURSOR_OFFSET
		y += CURSOR_OFFSET
		self.xAbs = x
		self.yAbs = y
		self.plotList.append(self.canvas.create_oval(
			x-PLOT_SIZE, y-PLOT_SIZE, x+PLOT_SIZE, y+PLOT_SIZE, fill=RED))
		self.clearRedo()
		self.plotStore(x, y, 'Point')

	# plots given list of landmarks (const)
	def plotLmark(self):
		lmark = LANDMARK
		for i in range(len(lmark)):
			x1,y1 = lmark.loc[i,'X']*X, lmark.loc[i,'Y']*Y
			if lmark.loc[i,'Floor'] == FLOOR_DICT[self.floorIndex]:
				self.canvas.create_oval(
					x1-PLOT_SIZE, y1-PLOT_SIZE, x1+PLOT_SIZE, y1+PLOT_SIZE, fill=BROWN)

	# Maintains a Trailing Plot count of length PLOT_COUNT_MAX
	def actionCounter(self, isPoint, isUndo = False):
		if isPoint:
			self.pointIndex +=1
			self.actionCount += 1
			if self.actionCount >= PLOT_COUNT_MAX:
				self.actionCount -=1
				self.canvas.delete(self.plotList[self.pointIndex-PLOT_COUNT_MAX])
		else:
			if isUndo:
				self.pointIndex -=1
				self.actionCount -= 1
			else:
				self.actionCount += 1
		if self.actionCount < 0:
			self.actionCount = 0
			print('Error: actionCount below 0.')

	# Takes in absolute plot values and stores them through addData
	def plotStore(self, x, y, marker):
		xRel = round(x/X,5)
		yRel = round(y/Y,5)
		print(marker+' plotted at: ('+str(xRel)+', '+str(yRel)+')')
		self.addData(xRel,yRel,marker)

	# Add Sign 
	def plotSign(self):
		if (self.xAbs != -1 and self.yAbs != -1):
			self.actionCounter(False)
			x, y = self.xAbs, self.yAbs
			self.canvas.delete(self.plotList.pop())
			self.plotList.append(self.canvas.create_oval(
				x-PLOT_SIZE, y-PLOT_SIZE, x+PLOT_SIZE, y+PLOT_SIZE, fill=CYAN))
			self.plotStore(x, y, 'Sign')
			self.clearRedo()
		else:
			print("No points intialized, cannot mark sign.")

	# adjust the plot of the most recent point
	def plotAdjust(self, direction):
		if (self.xAbs != -1 and self.yAbs != -1 and self.actionCount != 0):
			x, y = self.xAbs, self.yAbs
			self.canvas.delete(self.plotList.pop())
			if direction == 0: # up
				y -= ADJ_SIZE
				self.yAbs = y
				self.plotList.append(self.canvas.create_oval(
					x-PLOT_SIZE, y-PLOT_SIZE, x+PLOT_SIZE, y+PLOT_SIZE, fill=RED))
			elif direction == 1: # right
				x += ADJ_SIZE
				self.xAbs = x
				self.plotList.append(self.canvas.create_oval(
					x-PLOT_SIZE, y-PLOT_SIZE, x+PLOT_SIZE, y+PLOT_SIZE, fill=RED))
			elif direction == 2: # down
				y += ADJ_SIZE
				self.yAbs = y
				self.plotList.append(self.canvas.create_oval(
					x-PLOT_SIZE, y-PLOT_SIZE, x+PLOT_SIZE, y+PLOT_SIZE, fill=RED))
			else: # left
				x -= ADJ_SIZE
				self.xAbs = x
				self.plotList.append(self.canvas.create_oval(
					x-PLOT_SIZE, y-PLOT_SIZE, x+PLOT_SIZE, y+PLOT_SIZE, fill=RED))
			self.popData(False)
			self.plotStore(x, y, 'Adjusted Point')
		else:
			print("No points intialized, cannot mark sign.")

	# Undo or Redo the most recent plot
	def plotMistake(self, isUndo):
		#DEBUG: print('actionCount pre ',self.actionCount)#
		if isUndo: # Undo
			if self.actionCount > 0:
				self.actionCounter(False,True)
				xRel = round(self.xList[-1]/X,5)
				yRel = round(self.yList[-1]/Y,5)
				if xRel == 0 and yRel == 0:
					print('Marker {} undone'.format(self.markerList[-1]))
					self.btnMsg('Undo {}'.format(self.markerList[-1]))
				else:
					print('Point unplotted at: ('+str(xRel)+', '+str (yRel)+')')
					self.plotListMistake.append(self.canvas.coords(self.plotList[-1]))
					self.canvas.delete(self.plotList.pop())
					self.btnMsg('Undo Plot')
				if len(self.xList) > 0:	
					self.xAbs = self.xList[-1]*X
					self.yAbs = self.yList[-1]*Y
				self.popData(True)
			else:
				print('Cannot undo. Nothing to undo.')
		else: # Redo
			if len(self.plotListMistake) != 0 or len(self.markerListMistake) != 0:
				self.timeList.append(self.timeListMistake.pop())
				self.unixList.append(self.unixListMistake.pop())
				self.floorList.append(self.floorListMistake.pop())
				self.xList.append(self.xListMistake.pop())
				self.yList.append(self.yListMistake.pop())
				self.markerList.append(self.markerListMistake.pop())
				xRel = round(self.xList[-1]/X,5)
				yRel = round(self.yList[-1]/Y,5)
				if len(self.xList) > 0:	
					self.xAbs = self.xList[-1]*X
					self.yAbs = self.yList[-1]*Y
				if xRel != 0 and yRel != 0: # is point
					x1,y1,x2,y2 = self.plotListMistake.pop()
					self.plotList.append(self.canvas.create_oval(x1, y1, x2, y2, fill=RED))
					self.actionCounter(True)
					print('Point replotted at: ('+str(xRel)+', '+str(yRel)+')')
					self.btnMsg('Redo Plot')
				else: # is marker
					self.actionCounter(False)
					self.btnMsg('Redo {}'.format(self.markerList[-1]))
			else:
				print('Cannot redo. Redo cache is empty.')
		#DEBUG: print('actionCount post ',self.actionCount)

	# Clear the Redo Cache
	def clearRedo(self):
		self.plotListMistake = []
		self.timeListMistake = []
		self.unixListMistake = []
		self.floorListMistake = []
		self.xListMistake = []
		self.yListMistake = []
		self.markerListMistake = []

	# clear the canvas of all points
	def clearCanvas(self):
		self.canvas.delete('all')
		self.canvas.create_image(X/2,Y/2, image = self.imgList[self.floorIndex])
		self.actionCount = 0
		self.clearRedo()
		self.plotLmark()

	# Add Unique Row Markers to Data
	def addMarker(self, marker):
		self.plotList.append(self.canvas.create_oval(0,0,0,0, fill=CYAN))
		self.actionCounter(True)
		self.addData(0,0, marker)
		print('Marker {} added.'.format(marker))
		self.btnMsg(marker)

	# Append Data to Python Lists for Later Concatenation in a pd.DataFrame
	def addData(self, xRel, yRel, marker):
		currentImg = IMG_FILES[self.floorIndex]
		self.timeList.append(datetime.datetime.now())
		self.unixList.append(time.time())
		self.floorList.append(currentImg[:currentImg.find('.')])
		self.xList.append(xRel)
		self.yList.append(yRel)
		self.markerList.append(marker)	 	

	# Pop last element of data lists
	def popData(self, isMistake):
		if isMistake == False:
			self.timeList.pop()
			self.unixList.pop()
			self.floorList.pop()
			self.xList.pop()
			self.yList.pop()
			self.markerList.pop()
		else:
			self.timeListMistake.append(self.timeList.pop())
			self.unixListMistake.append(self.unixList.pop())
			self.floorListMistake.append(self.floorList.pop())
			self.xListMistake.append(self.xList.pop())
			self.yListMistake.append(self.yList.pop())
			self.markerListMistake.append(self.markerList.pop())

	# Concatenate data and save to .csv
	def saveData(self):	
		# DEBUG
		# print(len(self.timeList))
		# print(len(self.unixList))
		# print(len(self.floorList))
		# print(len(self.markerList))
		# print(len(self.xList))
		# print(len(self.yList))
		df = pd.DataFrame( {'Time': self.timeList, 'Unix': self.unixList, 'Floor': self.floorList,
		 'Marker': self.markerList,'X': self.xList, 'Y': self.yList}) 
		filename = ''
		if len(self.timeList) == 0:
			filename = 'empty.csv'
		else:
			filename = str(self.timeList[-1])
			filename = filename[:filename.find(' ')]+'-filenum-'+str(self.fileNum)+'.csv'
		df.to_csv(filename)	
		print('Data Saved as '+filename)

	# Autosave data after MINS_AUTOSAVE minutes/MS_AUTOSAVE milliseconds
	def autoSave(self):
		self.saveData()
		print('Data Saved. AutoSave checkpoint at '+str(S_AUTOSAVE)+' seconds reached.')
		self.canvas.after(MS_AUTOSAVE,self.autoSave)

	# Save Data and create new, empty csv
	def saveNew(self):
		self.saveData()
		self.fileNum += 1
		self.clearCanvas()
		print('Saved data and initialized new data file.')
	
	# Save Data and Quit
	def saveQuit(self):
		self.saveData()
		print('Saved data and app quitting.')
		self.quit()

class MyHandlerText(logging.StreamHandler):
    def __init__(self, textctrl):
        logging.StreamHandler.__init__(self) # initialize parent
        self.textctrl = textctrl

    def emit(self, record):
        msg = self.format(record)
        self.textctrl.config(state="normal")
        self.textctrl.insert("end", msg + "\n")
        self.flush()
        self.textctrl.config(state="disabled")

class Checkbar(tk.Frame):
   def __init__(self, parent=None, picks=[], side='left'):
      tk.Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = tk.IntVar()
         chk = tk.Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, expand='yes')
         self.vars.append(var)
   
   def checkboxState(self):
      return map((lambda var: var.get()), self.vars)

class popupWindow(object):
	def __init__(self, master, survey_num):
		top = self.top = Toplevel(master)
		x = app.winfo_x()
		y = app.winfo_y()
		top.geometry("+%d+%d" % (x + 550, y))
		self.surveyResp = []
		for i, qtype in enumerate(SURVEY.iloc[:,0]):
			qtext = SURVEY.iloc[i,1]
			qrange = list(map(int,SURVEY.iloc[i,2].split(",")))
			if qtype == "slider":
				# slider
				self.surveyResp.append(tk.DoubleVar())
				slider_label = tk.Label(
					top,
					text=qtext
				)
				slider_label.pack(side = 'top')
				slider = tk.Scale(
					top,
					from_=qrange[0],
					to=qrange[1],
					orient='horizontal',  # vertical
					variable=self.surveyResp[i],
					length = 300
				)
				slider.pack(side = 'top', pady = (0,BTN_SPACING), padx = (BTN_SPACING,BTN_SPACING))
			elif qtype == "textbox":
        		# text box
				self.l = tk.Label(top, text=qtext)
				self.l.pack(side = 'top', pady = (BTN_SPACING*5,0))
				self.e = tk.Entry(top)
				self.e.pack(side = 'top', padx = (BTN_SPACING,BTN_SPACING))
				self.surveyResp.append(self.e)
			else:
				raise NameError('Invalid Survey Question Type for index {}'.format(i)) 
		self.b = tk.Button(top, text='Ok', command=partial(self.cleanup, survey_num))
		self.b.pack(side = 'top')

	def cleanup(self, survey_num):
		# self.value = self.e.get()
		self.top.destroy()
		resp = []
		for i in self.surveyResp:
			resp.append(i.get())
		df = SURVEY
		df['response'] = resp
		filename = "survey_resp_{}.csv".format(survey_num)
		df.to_csv(filename)	
		print("Saved file as {}".format(filename))

# defines action when window close is pressed
def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit? Make sure to save!"):
        app.destroy()

# opens URL (const)
def openUrl():
    webbrowser.open_new(URL)

if __name__ == "__main__":
	app = runApp()
	app.title('Wayfind: Real-World Wayfinding Tool')
	app.iconbitmap(r'images/dail.ico')
	app.protocol("WM_DELETE_WINDOW", on_closing)
	stderrHandler = logging.StreamHandler()
	module_logger = logging.getLogger(__name__)
	module_logger.addHandler(stderrHandler)
	guiHandler = MyHandlerText(app.mytext)
	module_logger.addHandler(guiHandler)
	module_logger.setLevel(logging.INFO)
	module_logger.info("Button Event Log:")    
	app.eval('tk::PlaceWindow . center')
	app.mainloop()