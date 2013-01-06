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
		
		### Layout summary
		ConnectMachine = Tkinter.Frame(self)
		ConnectMachine.grid(row=0,column=0)
		
		LoadCentroid = Tkinter.Frame(self)
		LoadCentroid.grid(row=1,column=0)		
		
		LoadFeeder = Tkinter.Frame(self)
		LoadFeeder.grid(row=2,column=0)	
		
		ManualControl = Tkinter.Frame(self)
		ManualControl.grid(row=3,column=0)	
		
		AutomaticControl = Tkinter.Frame(self)
		AutomaticControl.grid(row=4,column=0)			
		
		Status = Tkinter.Frame(self)
		Status.grid(row=5,column=0)			
		
		### Layout details
		## Connect machine
		ConnectMachineTitle = Tkinter.Label(ConnectMachine,text=u"Connect machine:",anchor="w")
		ConnectMachineTitle.grid(row=0,column=0,sticky='W')
		
		# Drop down with serial ports
		SerialPorts = Tkinter.Button(ConnectMachine,text=u"COM 8")
		SerialPorts.grid(row=0,column=1)		
				
		# Refresh
		Refresh = Tkinter.Button(ConnectMachine,text=u"Refresh")
		Refresh.grid(row=0,column=2)	
		
		# Connect
		Connect = Tkinter.Button(ConnectMachine,text=u"Connect")
		Connect.grid(row=0,column=3)	
		
		# Disconnect
		Disconnect = Tkinter.Button(ConnectMachine,text=u"Disconnect")
		Disconnect.grid(row=0,column=4)

		
		## Load centroid file
		LoadCentroidTitle = Tkinter.Label(LoadCentroid,text=u"Load centroid file:",anchor="w")
		LoadCentroidTitle.grid(row=0,column=0,sticky='W')

		# File loaded
		CentroidLoaded = Tkinter.Label(LoadCentroid,text=u"DRV8818centroid.txt",anchor="w")
		CentroidLoaded.grid(row=0,column=1,sticky='W')
		
		# Browse for file
		CentroidBrowse = Tkinter.Button(LoadCentroid,text=u"Browse...")
		CentroidBrowse.grid(row=0,column=2)
		
		
		## Load feeder file
		LoadFeederTitle = Tkinter.Label(LoadFeeder,text=u"Load feeder file:",anchor="w")
		LoadFeederTitle.grid(row=0,column=0,sticky='W')

		# File loaded
		FeederLoaded = Tkinter.Label(LoadFeeder,text=u"DRV8818feeder.txt",anchor="w")
		FeederLoaded.grid(row=0,column=1,sticky='W')
		
		# Browse for file
		FeederBrowse = Tkinter.Button(LoadFeeder,text=u"Browse...")
		FeederBrowse.grid(row=0,column=2)
		
		
		## Manual control
		ManualControlTitle = Tkinter.Label(ManualControl,text=u"Manual Control:",anchor="w")
		ManualControlTitle.grid(row=0,column=0,sticky='W')
		
		# MinusX
		MinusX = Tkinter.Button(ManualControl,text=u"-X")
		MinusX.grid(row=0,column=1)
		
		# PlusX
		PlusX = Tkinter.Button(ManualControl,text=u"+X")
		PlusX.grid(row=0,column=2)
		
		# MinusY
		MinusY = Tkinter.Button(ManualControl,text=u"-Y")
		MinusY.grid(row=0,column=3)
		
		# PlusY
		PlusY = Tkinter.Button(ManualControl,text=u"+Y")
		PlusY.grid(row=0,column=4)		
		
		# MinusZ
		MinusX = Tkinter.Button(ManualControl,text=u"-Z")
		MinusX.grid(row=0,column=5)
		
		# PlusZ
		PlusX = Tkinter.Button(ManualControl,text=u"+Z")
		PlusX.grid(row=0,column=6)

		# VacuumOn
		VacuumOn = Tkinter.Button(ManualControl,text=u"Vacuum On")
		VacuumOn.grid(row=0,column=7)

		# VacuumOff
		VacuumOff = Tkinter.Button(ManualControl,text=u"Vacuum Off")
		VacuumOff.grid(row=0,column=8)		

		
		## Automatic control
		AutomaticControlTitle = Tkinter.Label(AutomaticControl,text=u"Automatic Control:",anchor="w")
		AutomaticControlTitle.grid(row=0,column=0,sticky='W')
		
		# Play
		Play = Tkinter.Button(AutomaticControl,text=u"Play")
		Play.grid(row=0,column=1)		

		# Pause
		Pause = Tkinter.Button(AutomaticControl,text=u"Pause")
		Pause.grid(row=0,column=2)	

		# Stop
		Stop = Tkinter.Button(AutomaticControl,text=u"Stop")
		Stop.grid(row=0,column=3)
		
		# Previous line
		PreviousLine = Tkinter.Button(AutomaticControl,text=u"Previous Line")
		PreviousLine.grid(row=0,column=4)

		# Next line
		NextLine = Tkinter.Button(AutomaticControl,text=u"Next Line")
		NextLine.grid(row=0,column=5)

		# Step
		Step = Tkinter.Button(AutomaticControl,text=u"Step")
		Step.grid(row=0,column=6)		
		
		
		## Status
		StatusTitle = Tkinter.Label(Status,text=u"Status:",anchor="w")
		StatusTitle.grid(row=0,column=0,sticky='W')
		
		# X Location
		XLocation = Tkinter.Label(Status,text=u"X:  5.0 in",anchor="w")
		XLocation.grid(row=0,column=1,sticky='W')
		
		# Y Location
		YLocation = Tkinter.Label(Status,text=u"Y:  6.0 in",anchor="w")
		YLocation.grid(row=0,column=2,sticky='W')		
		
		# Z Location
		ZLocation = Tkinter.Label(Status,text=u"Z:  1.0 in",anchor="w")
		ZLocation.grid(row=0,column=3,sticky='W')		
		
		# Vacuum status
		VacuumStatus = Tkinter.Label(Status,text=u"Vacuum:  ON",anchor="w")
		VacuumStatus.grid(row=0,column=4,sticky='W')				
		
		# G Code viewer
		GCodeListBox = Tkinter.Listbox(Status)
		GCodeListBox.grid(row=1,column=0,columnspan=5,sticky='SEW')
		
		GCodeScrollBar = Tkinter.Scrollbar(Status)
		GCodeScrollBar.grid(row=1,column=0,columnspan=5,sticky='NSE')
		
		for i in range(100):
			GCodeListBox.insert(i,"g0 x"+str(i)+" f1600")
		
		GCodeListBox.config(yscrollcommand=GCodeScrollBar.set)
		GCodeScrollBar.config(command=GCodeListBox.yview)
		
		'''
		# Focus on text box
		self.entry.focus_set()
		self.entry.selection_range(0,Tkinter.END)
		'''
		
		
		# Manage resizing
		self.grid_columnconfigure(0,weight=1) # enable resizing
		self.resizable(True,True) # enable x resizing and enable y resizing
		self.update() # disable automatic resizing
		self.geometry(self.geometry()) # disable automatic resizing
		
if __name__ == "__main__":
	app = boardforge_tk(None)
	app.title('Board Forge - www.boardforge.com')
	app.mainloop()