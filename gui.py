#	This file is part of Board Forge (TM) www.boardforge.com
#
#	Board Forge (TM) is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	at your option) any later version.
#
#	Board Forge is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Board Forge (TM).  If not, see <http://www.gnu.org/licenses/>.
#
#	Adapted from: 
#	Simple example of python and tkinter - http://sebsauvage.net/python/gui/
#	File loading - http://tkinter.unpythonic.net/wiki/tkFileDialog
#	Gcode area listbox - http://www.tutorialspoint.com/python/tk_listbox.htm
#	Gcode area scrollbar - http://effbot.org/zone/tkinter-scrollbar-patterns.htm

import Tkinter

class boardforge_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		self.grid()
		
		## Connect machine
		ConnectMachine = Tkinter.Label(self,text=u"Connect machine:",anchor="w")
		ConnectMachine.grid(row=0,column=0,sticky='W')
		
		# Drop down with serial ports
		SerialPorts = Tkinter.Button(self,text=u"COM 8")
		SerialPorts.grid(row=0,column=1)		
				
		# Refresh
		Refresh = Tkinter.Button(self,text=u"Refresh")
		Refresh.grid(row=0,column=2)	
		
		# Connect
		Connect = Tkinter.Button(self,text=u"Connect")
		Connect.grid(row=0,column=3)	
		
		# Disconnect
		Disconnect = Tkinter.Button(self,text=u"Disconnect")
		Disconnect.grid(row=0,column=4)

		## Load centroid file
		LoadCentroid = Tkinter.Label(self,text=u"Load centroid file:",anchor="w")
		LoadCentroid.grid(row=1,column=0,sticky='W')

		# File loaded
		CentroidLoaded = Tkinter.Label(self,text=u"DRV8818centroid.txt",anchor="w")
		CentroidLoaded.grid(row=1,column=1,sticky='W')
		
		# Browse for file
		CentroidBrowse = Tkinter.Button(self,text=u"Browse...")
		CentroidBrowse.grid(row=1,column=2)
		
		## Load feeder file
		LoadFeeder = Tkinter.Label(self,text=u"Load feeder file:",anchor="w")
		LoadFeeder.grid(row=2,column=0,sticky='W')

		# File loaded
		FeederLoaded = Tkinter.Label(self,text=u"DRV8818feeder.txt",anchor="w")
		FeederLoaded.grid(row=2,column=1,sticky='W')
		
		# Browse for file
		FeederBrowse = Tkinter.Button(self,text=u"Browse...")
		FeederBrowse.grid(row=2,column=2)
		
		## Manual control
		ManualControl = Tkinter.Label(self,text=u"Manual Control:",anchor="w")
		ManualControl.grid(row=3,column=0,sticky='W')
		
		# MinusX
		MinusX = Tkinter.Button(self,text=u"-X")
		MinusX.grid(row=3,column=1)
		
		# PlusX
		PlusX = Tkinter.Button(self,text=u"+X")
		PlusX.grid(row=3,column=2)
		
		# MinusY
		MinusY = Tkinter.Button(self,text=u"-Y")
		MinusY.grid(row=3,column=3)
		
		# PlusY
		PlusY = Tkinter.Button(self,text=u"+Y")
		PlusY.grid(row=3,column=4)		
		
		# MinusZ
		MinusX = Tkinter.Button(self,text=u"-Z")
		MinusX.grid(row=3,column=5)
		
		# PlusZ
		PlusX = Tkinter.Button(self,text=u"+Z")
		PlusX.grid(row=3,column=6)

		# VacuumOn
		VacuumOn = Tkinter.Button(self,text=u"Vacuum On")
		VacuumOn.grid(row=3,column=7)

		# VacuumOff
		VacuumOff = Tkinter.Button(self,text=u"Vacuum Off")
		VacuumOff.grid(row=3,column=8)		

		## Automatic control
		AutomaticControl = Tkinter.Label(self,text=u"Automatic Control:",anchor="w")
		AutomaticControl.grid(row=4,column=0,sticky='W')
		
		# Play
		Play = Tkinter.Button(self,text=u"Play")
		Play.grid(row=4,column=1)		

		# Pause
		Pause = Tkinter.Button(self,text=u"Pause")
		Pause.grid(row=4,column=2)	

		# Stop
		Stop = Tkinter.Button(self,text=u"Stop")
		Stop.grid(row=4,column=3)
		
		# Previous line
		PreviousLine = Tkinter.Button(self,text=u"Previous Line")
		PreviousLine.grid(row=4,column=4)

		# Next line
		NextLine = Tkinter.Button(self,text=u"Next Line")
		NextLine.grid(row=4,column=5)

		# Step
		Step = Tkinter.Button(self,text=u"Step")
		Step.grid(row=4,column=6)		
		
		## Status
		Status = Tkinter.Label(self,text=u"Status:",anchor="w")
		Status.grid(row=5,column=0,sticky='W')
		
		# X Location
		XLocation = Tkinter.Label(self,text=u"X:  5.0 in",anchor="w")
		XLocation.grid(row=5,column=1,sticky='W')
		
		# Y Location
		YLocation = Tkinter.Label(self,text=u"Y:  6.0 in",anchor="w")
		YLocation.grid(row=5,column=2,sticky='W')		
		
		# Z Location
		ZLocation = Tkinter.Label(self,text=u"Z:  1.0 in",anchor="w")
		ZLocation.grid(row=5,column=3,sticky='W')		
		
		# Vacuum status
		VacuumStatus = Tkinter.Label(self,text=u"Vacuum:  ON",anchor="w")
		VacuumStatus.grid(row=5,column=4,sticky='W')				
		
		# G Code viewer
		GCodeListBox = Tkinter.Listbox(self)
		GCodeListBox.grid(row=6,column=0,columnspan=9,sticky='SEW')
		
		GCodeScrollBar = Tkinter.Scrollbar(self)
		GCodeScrollBar.grid(row=6,column=0,columnspan=9,sticky='NSE')
		
		for i in range(100):
			GCodeListBox.insert(i,"g0 x"+str(i)+" f1600")
		
		GCodeListBox.config(yscrollcommand=GCodeScrollBar.set)
		GCodeScrollBar.config(command=GCodeListBox.yview)
		

		
		'''
		# Text box
		self.entryVariable = Tkinter.StringVar()
		self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
		self.entry.grid(column=0,row=0,sticky='EW')
		self.entry.bind("<Return>", self.OnPressEnter)
		self.entryVariable.set(u"Enter text here.")
		
		# Button
		button = Tkinter.Button(self,text=u"Button",command=self.OnButtonClick)
		button.grid(column=1,row=0)
		
		# Label
		self.labelVariable = Tkinter.StringVar()
		label = Tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="blue")
		label.grid(column=0,row=1,columnspan=2,sticky='EW')
		self.labelVariable.set(u"Hello!")
				
		# Focus on text box
		self.entry.focus_set()
		self.entry.selection_range(0,Tkinter.END)
		'''
		
		# Manage resizing
		self.grid_columnconfigure(0,weight=1) # enable resizing
		self.resizable(True,True) # enable x resizing and enable y resizing
		self.update() # disable automatic resizing
		self.geometry(self.geometry()) # disable automatic resizing
	'''
	# Returns an opened file in read mode.
	def askopenfile(self):
		return tkFileDialog.askopenfile(mode='r', **self.file_opt)
		
	def OnButtonClick(self):
		self.labelVariable.set(self.entryVariable.get()+" You clicked the button!")
		
		# Focus on text box
		self.entry.focus_set()
		self.entry.selection_range(0,Tkinter.END)
		
	def OnPressEnter(self,event):
		self.labelVariable.set(self.entryVariable.get()+" You pressed enter!")
		
		# Focus on text box		
		self.entry.focus_set()
		self.entry.selection_range(0,Tkinter.END)
	'''
		
if __name__ == "__main__":
	app = boardforge_tk(None)
	app.title('Board Forge - www.boardforge.com')
	app.mainloop()