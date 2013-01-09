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
# 	Menu - http://www.tutorialspoint.com/python/tk_menubutton.htm

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
		ConnectMachine.grid(row=0,column=0,sticky='W',padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=4)
		
		Status = Tkinter.Frame(self,bg=Background)
		Status.grid(row=1,column=0,padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=4)		
		
		# Automatic control
		AutomaticLabel = Tkinter.Frame(self,bg=Background)
		AutomaticLabel.grid(row=2,column=0,sticky='W',padx=LabelCellPadding,pady=LabelCellPadding)				
		
		LoadCentroid = Tkinter.Frame(self,bg=Background)
		LoadCentroid.grid(row=3,column=0,sticky='W',padx=SummaryCellPadding,pady=SummaryCellPadding)		
		
		LoadFeeder = Tkinter.Frame(self,bg=Background)
		LoadFeeder.grid(row=4,column=0,sticky='W',padx=SummaryCellPadding,pady=SummaryCellPadding)			
		
		MachineSettings = Tkinter.Frame(self,bg=Background)
		MachineSettings.grid(row=3,column=1,sticky='NW',padx=SummaryCellPadding,pady=SummaryCellPadding,rowspan=2)			

		VisionFrame = Tkinter.Frame(self,bg=Background)
		VisionFrame.grid(row=3,column=2,sticky='SEW',padx=SummaryCellPadding,pady=SummaryCellPadding,rowspan=3)	
		
		# Manual control
		ManualLabel = Tkinter.Frame(self,bg=Background)
		ManualLabel.grid(row=2,column=3,sticky='W',padx=LabelCellPadding,pady=LabelCellPadding)			
		
		ManualControl = Tkinter.Frame(self,bg=Background)
		ManualControl.grid(row=3,column=3,sticky='NW',padx=SummaryCellPadding,pady=SummaryCellPadding,rowspan=3)		

		ManualGcodeSend = Tkinter.Frame(self,bg=Background)
		ManualGcodeSend.grid(row=5,column=3,sticky='NW',padx=SummaryCellPadding,pady=SummaryCellPadding)			
		
		# Component plan viewer
		ComponentPlan = Tkinter.Frame(self,bg=Background)
		ComponentPlan.grid(row=7,column=0,sticky='SEW',padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=3)	
		
		'''
		# Gcode viewer
		Gcode = Tkinter.Frame(self,bg=Background)
		Gcode.grid(row=7,column=3,sticky='SEW',padx=SummaryCellPadding,pady=SummaryCellPadding)			
		'''
		
		AutomaticControl = Tkinter.Frame(self,bg=Background)
		AutomaticControl.grid(row=8,column=0,padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=3)			
		
		# Debug
		Debugger = Tkinter.Frame(self,bg=Background)
		Debugger.grid(row=9,column=0,sticky='S',padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=3)
		
		### Layout details
		## Connect machine		
		# Find Machine
		FindMachine = Tkinter.Button(ConnectMachine,text=u"Find machine",command=self.OnFindMachineClick)
		FindMachine.grid(row=0,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		## Serial port selector		
		SerialPorts = Tkinter.Listbox(ConnectMachine,height=3,width=10)
		SerialPorts.grid(row=0,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=3)
		
		SerialPortsScrollBar = Tkinter.Scrollbar(ConnectMachine)
		SerialPortsScrollBar.grid(row=0,column=1,sticky='E',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=3)
		
		for i in range(15):
			SerialPorts.insert(i,"COM"+str(i+1)+"")
		
		SerialPorts.config(yscrollcommand=SerialPortsScrollBar.set)
		SerialPortsScrollBar.config(command=SerialPorts.yview)		
		
		
		# Connect
		Connect = Tkinter.Button(ConnectMachine,text=u"Connect",command=self.OnConnectClick)
		Connect.grid(row=0,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)	
		
		# Disconnect
		Disconnect = Tkinter.Button(ConnectMachine,text=u"Disconnect",command=self.OnDisconnectClick)
		Disconnect.grid(row=0,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# ConnectionStatus
		ConnectionStatus = Tkinter.Label(ConnectMachine,text=u"Connected on COM8",anchor="w")
		ConnectionStatus.grid(row=0,column=4,padx=DetailsCellPadding,pady=DetailsCellPadding)		

		## Machine status
		# X Location
		XLocation = Tkinter.Label(Status,text=u"\n X:  5.0 inches",anchor="w")
		XLocation.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Y Location
		YLocation = Tkinter.Label(Status,text=u"\n Y:  6.0 inches",anchor="w")
		YLocation.grid(row=0,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Z Location
		ZLocation = Tkinter.Label(Status,text=u"\n Z:  1.0 inches",anchor="w")
		ZLocation.grid(row=0,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)		

		# Rotation
		Rotation = Tkinter.Label(Status,text=u"\n Rotation: 90 degrees",anchor="w")
		Rotation.grid(row=0,column=4,padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		# Vacuum status
		VacuumStatus = Tkinter.Label(Status,text=u"\n Vacuum:  ON",anchor="w")
		VacuumStatus.grid(row=0,column=5,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		
		## Manual label
		ManualControlTitle = Tkinter.Label(ManualLabel,text=u"\n Manual Control:",anchor="w")
		ManualControlTitle.grid(row=0,column=0,sticky='W',padx=LabelCellPadding,pady=LabelCellPadding)		

		# MinusX
		MinusX = Tkinter.Button(ManualControl,text=u"-X",command=self.OnMinusXClick)
		MinusX.grid(row=1,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# PlusX
		PlusX = Tkinter.Button(ManualControl,text=u"+X",command=self.OnPlusXClick)
		PlusX.grid(row=1,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# MinusY
		MinusY = Tkinter.Button(ManualControl,text=u"-Y",command=self.OnMinusYClick)
		MinusY.grid(row=2,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# PlusY
		PlusY = Tkinter.Button(ManualControl,text=u"+Y",command=self.OnPlusYClick)
		PlusY.grid(row=0,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# MinusZ
		MinusX = Tkinter.Button(ManualControl,text=u"-Z",command=self.OnMinusZClick)
		MinusX.grid(row=2,column=5,padx=DetailsCellPadding,pady=DetailsCellPadding)	
		
		# PlusZ
		PlusX = Tkinter.Button(ManualControl,text=u"+Z",command=self.OnPlusZClick)
		PlusX.grid(row=0,column=5,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Counter clockwise
		CounterClockWise = Tkinter.Button(ManualControl,text=u"CCW",command=self.OnCounterClockWiseClick)
		CounterClockWise.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Clockwise
		ClockWise = Tkinter.Button(ManualControl,text=u"CW",command=self.OnClockWiseClick)
		ClockWise.grid(row=0,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)			

		# VacuumOn
		VacuumOn = Tkinter.Button(ManualControl,text=u"Vacuum On",command=self.OnVacuumOnClick)
		VacuumOn.grid(row=0,column=7,padx=DetailsCellPadding,pady=DetailsCellPadding)

		# VacuumOff
		VacuumOff = Tkinter.Button(ManualControl,text=u"Vacuum Off",command=self.OnVacuumOffClick)
		VacuumOff.grid(row=2,column=7,padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Manual Gcode
		ManualGcode = Tkinter.Entry(ManualGcodeSend,text=u"Enter gcode")
		ManualGcode.grid(row=0,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Send Manual Gcode
		SendManualGcode = Tkinter.Button(ManualGcodeSend,text=u"Send Gcode",command=self.OnSendManualGcode)
		SendManualGcode.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		
		## Automatic label
		AutomaticControlTitle = Tkinter.Label(AutomaticLabel,text=u"\n Automatic Control:",anchor="w")
		AutomaticControlTitle.grid(row=0,column=0,sticky='W',padx=LabelCellPadding,pady=LabelCellPadding)	
		
		
		## Load centroid file
		# Browse for file
		CentroidBrowse = Tkinter.Button(LoadCentroid,text=u"Browse for Centroid file...",command=self.OnCentroidBrowseClick)
		CentroidBrowse.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# File loaded
		CentroidLoaded = Tkinter.Label(LoadCentroid,text=u"DRV8818centroid.txt",anchor="w")
		CentroidLoaded.grid(row=0,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		
		## Load feeder file
		# Browse for file
		FeederBrowse = Tkinter.Button(LoadFeeder,text=u"Browse for Feeder file...",command=self.OnFeederBrowseClick)
		FeederBrowse.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)

		# File loaded
		FeederLoaded = Tkinter.Label(LoadFeeder,text=u"DRV8818feeder.txt",anchor="w")
		FeederLoaded.grid(row=0,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		## Automatic controls		
		# Play
		Play = Tkinter.Button(AutomaticControl,text=u"Play",command=self.OnPlayClick)
		Play.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)		

		# Pause
		Pause = Tkinter.Button(AutomaticControl,text=u"PAUSE",command=self.OnPauseClick,bg='red',fg='white')
		Pause.grid(row=0,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)	

		# Stop
		Stop = Tkinter.Button(AutomaticControl,text=u"Stop",command=self.OnStopClick)
		Stop.grid(row=0,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)				

		
		## Machine settings
		# Speed
		SpeedLabel = Tkinter.Label(MachineSettings,text=u"Speed",anchor="w")
		SpeedLabel.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		SpeedScale = Tkinter.Scale(MachineSettings,orient='horizontal',command=self.SpeedScaleSlide)
		SpeedScale.grid(row=0,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Vacuum
		VacuumRateLabel = Tkinter.Label(MachineSettings,text=u"Vacuum",anchor="w")
		VacuumRateLabel.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		VacuumScale = Tkinter.Scale(MachineSettings,orient='horizontal',command=self.VacuumScaleSlide)
		VacuumScale.grid(row=1,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		## Component plan step
		# Home
		Home = Tkinter.Button(ComponentPlan,text=u"Home",command=self.OnHomeClick)
		Home.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Previous Component
		PreviousComponent = Tkinter.Button(ComponentPlan,text=u"Previous Component",command=self.OnPreviousComponentClick)
		PreviousComponent.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Run Component
		RunComponent = Tkinter.Button(ComponentPlan,text=u"Run Component",command=self.OnRunComponentClick)
		RunComponent.grid(row=2,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Next Component
		NextComponent = Tkinter.Button(ComponentPlan,text=u"Next Component",command=self.OnNextComponentClick)
		NextComponent.grid(row=3,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		## Component plan viewer		
		ComponentPlanListBox = Tkinter.Listbox(ComponentPlan,width=90)
		ComponentPlanListBox.grid(row=0,column=1,sticky='NSEW',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=4)
		
		ComponentPlanScrollBar = Tkinter.Scrollbar(ComponentPlan)
		ComponentPlanScrollBar.grid(row=0,column=1,sticky='NSE',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=4)
			
		for i in range(5):
			ComponentPlanListBox.insert(i,"Pick 0805 1 uf capacitor (C"+str(i)+") from Feeder"+str(i+5)+" (1,"+str(i+5)+"), rotate 90 degrees, and place at "+str(i+5)+",2.")		
			
		for i in range(5):
			ComponentPlanListBox.insert(i,"Pick 0603 1k ohm resistor (R"+str(i)+") from Feeder"+str(i)+" (1,"+str(i)+"), rotate 0 degrees, and place at "+str(i)+",2.")		
		
		ComponentPlanListBox.config(yscrollcommand=ComponentPlanScrollBar.set)
		ComponentPlanScrollBar.config(command=ComponentPlanListBox.yview)				
		
		'''
		## Gcode Step
		# Previous gcode
		PreviousGcode = Tkinter.Button(Gcode,text=u"Previous Gcode",command=self.OnPreviousGcodeClick)
		PreviousGcode.grid(row=0,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Run line
		RunGcode = Tkinter.Button(Gcode,text=u"Run Gcode",command=self.OnRunGcodeClick)
		RunGcode.grid(row=1,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Next line
		NextGcode = Tkinter.Button(Gcode,text=u"Next Gcode",command=self.OnNextGcodeClick)
		NextGcode.grid(row=2,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
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
		
		## Vision
		Vision = Tkinter.Label(VisionFrame,text=u"Vision",fg='white',bg='black',width='35',height='10')
		Vision.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)				
		
		# Debugger
		self.DebuggerValue = Tkinter.StringVar()
		label = Tkinter.Label(Debugger,textvariable=self.DebuggerValue,anchor="w",bg="white")
		label.grid(column=0,row=0,columnspan=2,sticky='EW')
		self.DebuggerValue.set(u"Debugger")
		
		# Manage resizing
		self.grid_columnconfigure(0,weight=1) # enable resizing
		self.resizable(True,True) # enable x resizing and enable y resizing
		self.update() # disable automatic resizing
		self.geometry(self.geometry()) # disable automatic resizing

		
	#Button click events
	def OnPortClick(self):
		self.DebuggerValue.set(u"Port clicked")	

	def OnFindMachineClick(self):
		self.DebuggerValue.set(u"Find machine clicked")			

	def OnConnectClick(self):
		self.DebuggerValue.set(u"Connect clicked")			
		
	def OnDisconnectClick(self):
		self.DebuggerValue.set(u"Disconnect clicked")	
		
	def OnMinusXClick(self):
		self.DebuggerValue.set(u"-X clicked")	

	def OnPlusXClick(self):
		self.DebuggerValue.set(u"+X clicked")	

	def OnMinusYClick(self):
		self.DebuggerValue.set(u"-Y clicked")	

	def OnPlusYClick(self):
		self.DebuggerValue.set(u"+Y clicked")			

	def OnMinusZClick(self):
		self.DebuggerValue.set(u"-Z clicked")	

	def OnPlusZClick(self):
		self.DebuggerValue.set(u"+Z clicked")			

	def OnCounterClockWiseClick(self):
		self.DebuggerValue.set(u"CCW clicked")	

	def OnClockWiseClick(self):
		self.DebuggerValue.set(u"CW clicked")					
		
	def OnVacuumOffClick(self):
		self.DebuggerValue.set(u"Vacuum off clicked")	

	def OnVacuumOnClick(self):
		self.DebuggerValue.set(u"Vacuum on clicked")
	
	def OnSendManualGcode(self):
		self.DebuggerValue.set(u"Send Manual Gcode clicked")	
		#  how pass string to this?
		
	def OnFeederBrowseClick(self):
		self.DebuggerValue.set(u"Browse for feeder clicked")	

	def OnCentroidBrowseClick(self):
		self.DebuggerValue.set(u"Browse for centroid clicked")		
		
	def OnHomeClick(self):
		self.DebuggerValue.set(u"Home clicked")
		
	def OnPlayClick(self):
		self.DebuggerValue.set(u"Play clicked")

	def OnPauseClick(self):
		self.DebuggerValue.set(u"Pause clicked")		
		
	def OnStopClick(self):
		self.DebuggerValue.set(u"Stop clicked")

	def SpeedScaleSlide(self,Speed):
		self.DebuggerValue.set(u"Speed "+Speed+"%")

	def VacuumScaleSlide(self,VacuumRate):
		self.DebuggerValue.set(u"Vacuum "+VacuumRate+"%")			
		
	def OnPreviousComponentClick(self):
		self.DebuggerValue.set(u"Previous Component clicked")

	def OnRunComponentClick(self):
		self.DebuggerValue.set(u"Run Component clicked")		
		
	def OnNextComponentClick(self):
		self.DebuggerValue.set(u"Next Component clicked")
	'''
	def OnPreviousGcodeClick(self):
		self.DebuggerValue.set(u"Previous Gcode clicked")

	def OnRunGcodeClick(self):
		self.DebuggerValue.set(u"Run Gcode clicked")		
		
	def OnNextGcodeClick(self):
		self.DebuggerValue.set(u"Next Gcode clicked")
	'''
		
if __name__ == "__main__":
	app = boardforge_tk(None)
	app.title('Board Forge - www.boardforge.com')
	app.mainloop()