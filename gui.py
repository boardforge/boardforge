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
		### Layout settings
		LabelCellPadding = 0
		SummaryCellPadding = 5
		DetailsCellPadding = 5
		Background = '#D4D0C8' # Default #D4D0C8
		
		
		### Layout summary		
		ConnectMachine = Tkinter.Frame(self,bg=Background)
		ConnectMachine.grid(row=0,column=0,sticky='W',padx=SummaryCellPadding,pady=SummaryCellPadding)
		
		Status = Tkinter.Frame(self,bg=Background)
		Status.grid(row=1,column=0,sticky='W',padx=SummaryCellPadding,pady=SummaryCellPadding)		
		
		# Manual control
		ManualLabel = Tkinter.Frame(self,bg=Background)
		ManualLabel.grid(row=2,column=0,sticky='W',padx=LabelCellPadding,pady=LabelCellPadding)			
		
		ManualControl = Tkinter.Frame(self,bg=Background)
		ManualControl.grid(row=3,column=0,sticky='W',padx=SummaryCellPadding,pady=SummaryCellPadding,rowspan=3)		
		
		# Automatic control
		AutomaticLabel = Tkinter.Frame(self,bg=Background)
		AutomaticLabel.grid(row=2,column=1,sticky='W',padx=LabelCellPadding,pady=LabelCellPadding)				
		
		LoadCentroid = Tkinter.Frame(self,bg=Background)
		LoadCentroid.grid(row=3,column=1,sticky='W',padx=SummaryCellPadding,pady=SummaryCellPadding)		
		
		LoadFeeder = Tkinter.Frame(self,bg=Background)
		LoadFeeder.grid(row=4,column=1,sticky='W',padx=SummaryCellPadding,pady=SummaryCellPadding)	
		
		AutomaticControl = Tkinter.Frame(self,bg=Background)
		AutomaticControl.grid(row=5,column=1,sticky='W',padx=SummaryCellPadding,pady=SummaryCellPadding)			
		
		# Gcode viewer
		Gcode = Tkinter.Frame(self,bg=Background)
		Gcode.grid(row=6,column=0,sticky='SEW',padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=2)	

		'''
		### Layout details
		## Connect label
		ConnectMachineTitle = Tkinter.Label(ConnectLabel,text=u"Connect Machine:",anchor="w")
		ConnectMachineTitle.grid(row=0,column=0,sticky='W',padx=LabelCellPadding,pady=LabelCellPadding)
		'''
		
		## Connect machine		
		# Drop down with serial ports
		SerialPorts = Tkinter.Button(ConnectMachine,text=u"COM 8")
		SerialPorts.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)		
				
		# Refresh
		Refresh = Tkinter.Button(ConnectMachine,text=u"Refresh")
		Refresh.grid(row=0,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)	
		
		# Connect
		Connect = Tkinter.Button(ConnectMachine,text=u"Connect")
		Connect.grid(row=0,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)	
		
		# Disconnect
		Disconnect = Tkinter.Button(ConnectMachine,text=u"Disconnect")
		Disconnect.grid(row=0,column=4,padx=DetailsCellPadding,pady=DetailsCellPadding)

		
		## Manual label
		ManualControlTitle = Tkinter.Label(ManualLabel,text=u"\n Manual Control:",anchor="w")
		ManualControlTitle.grid(row=0,column=0,sticky='W',padx=LabelCellPadding,pady=LabelCellPadding)		

		# MinusX
		MinusX = Tkinter.Button(ManualControl,text=u"-X")
		MinusX.grid(row=1,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# PlusX
		PlusX = Tkinter.Button(ManualControl,text=u"+X")
		PlusX.grid(row=1,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# MinusY
		MinusY = Tkinter.Button(ManualControl,text=u"-Y")
		MinusY.grid(row=2,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# PlusY
		PlusY = Tkinter.Button(ManualControl,text=u"+Y")
		PlusY.grid(row=0,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# MinusZ
		MinusX = Tkinter.Button(ManualControl,text=u"-Z")
		MinusX.grid(row=2,column=5,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# PlusZ
		PlusX = Tkinter.Button(ManualControl,text=u"+Z")
		PlusX.grid(row=0,column=5,padx=DetailsCellPadding,pady=DetailsCellPadding)

		# VacuumOn
		VacuumOn = Tkinter.Button(ManualControl,text=u"Vacuum On")
		VacuumOn.grid(row=0,column=7,padx=DetailsCellPadding,pady=DetailsCellPadding)

		# VacuumOff
		VacuumOff = Tkinter.Button(ManualControl,text=u"Vacuum Off")
		VacuumOff.grid(row=2,column=7,padx=DetailsCellPadding,pady=DetailsCellPadding)		

		
		## Automatic label
		AutomaticControlTitle = Tkinter.Label(AutomaticLabel,text=u"\n Automatic Control:",anchor="w")
		AutomaticControlTitle.grid(row=0,column=0,sticky='W',padx=LabelCellPadding,pady=LabelCellPadding)	
		
		
		## Load centroid file
		# Browse for file
		CentroidBrowse = Tkinter.Button(LoadCentroid,text=u"Browse for Centroid file...")
		CentroidBrowse.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# File loaded
		CentroidLoaded = Tkinter.Label(LoadCentroid,text=u"DRV8818centroid.txt",anchor="w")
		CentroidLoaded.grid(row=0,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		
		## Load feeder file
		# Browse for file
		FeederBrowse = Tkinter.Button(LoadFeeder,text=u"Browse for Feeder file...")
		FeederBrowse.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)

		# File loaded
		FeederLoaded = Tkinter.Label(LoadFeeder,text=u"DRV8818feeder.txt",anchor="w")
		FeederLoaded.grid(row=0,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Play
		Play = Tkinter.Button(AutomaticControl,text=u"Play")
		Play.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)		

		# Pause
		Pause = Tkinter.Button(AutomaticControl,text=u"Pause")
		Pause.grid(row=0,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)	

		# Stop
		Stop = Tkinter.Button(AutomaticControl,text=u"Stop")
		Stop.grid(row=0,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		
		## Machine status
		# X Location
		XLocation = Tkinter.Label(Status,text=u"X:  5.0 in",anchor="w")
		XLocation.grid(row=0,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Y Location
		YLocation = Tkinter.Label(Status,text=u"Y:  6.0 in",anchor="w")
		YLocation.grid(row=0,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Z Location
		ZLocation = Tkinter.Label(Status,text=u"Z:  1.0 in",anchor="w")
		ZLocation.grid(row=0,column=3,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Vacuum status
		VacuumStatus = Tkinter.Label(Status,text=u"Vacuum:  ON",anchor="w")
		VacuumStatus.grid(row=0,column=4,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)				
		
		
		## Step
		# Previous line
		LastLine = Tkinter.Button(Gcode,text=u"Previous Line")
		LastLine.grid(row=0,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Run line
		RunLine = Tkinter.Button(Gcode,text=u"Run Line")
		RunLine.grid(row=1,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Next line
		NextLine = Tkinter.Button(Gcode,text=u"Next Line")
		NextLine.grid(row=2,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		
		## G Code viewer		
		GCodeListBox = Tkinter.Listbox(Gcode)
		GCodeListBox.grid(row=0,column=1,sticky='NSEW',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=3)
		
		GCodeScrollBar = Tkinter.Scrollbar(Gcode)
		GCodeScrollBar.grid(row=0,column=1,sticky='NSE',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=3)
		
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