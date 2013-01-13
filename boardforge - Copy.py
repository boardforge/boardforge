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
#   Serial control from http://onehossshay.wordpress.com/2011/08/26/grbl-a-simple-python-interface/
#	File browsing - http://tkinter.unpythonic.net/wiki/tkFileDialog
#	File open - http://www.tutorialspoint.com/python/python_files_io.htm
#	File readlines - http://www.peterbe.com/plog/blogitem-040312-1
#	String split - http://www.webmasterwords.com/python-split-and-join-examples
#	Gcode area listbox - http://www.tutorialspoint.com/python/tk_listbox.htm
#	Gcode area scrollbar - http://effbot.org/zone/tkinter-scrollbar-patterns.htm
# 	Menu - http://www.tutorialspoint.com/python/tk_menubutton.htm

# For gui
import Tkinter, Tkconstants, tkFileDialog

# For serial communication
import serial
import time

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
		
		# Instruction plan viewer
		InstructionPlan = Tkinter.Frame(self,bg=Background)
		InstructionPlan.grid(row=7,column=0,sticky='SEW',padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=3)	
		
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
		
		# Serial port selector		
		SerialPorts = Tkinter.Listbox(ConnectMachine,height=3,width=10)
		SerialPorts.grid(row=0,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=3)
		
		SerialPortsScrollBar = Tkinter.Scrollbar(ConnectMachine)
		SerialPortsScrollBar.grid(row=0,column=1,sticky='E',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=3)
		
		for i in range(15):
			SerialPorts.insert(i,"COM"+str(i+1)+"")
		
		SerialPorts.config(yscrollcommand=SerialPortsScrollBar.set)
		SerialPortsScrollBar.config(command=SerialPorts.yview)		
		
		
		# Connect
		self.SerialConnection = serial.Serial('COM12',115200)
			
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
		self.CentroidList = []
		
		# Browse for file
		CentroidBrowse = Tkinter.Button(LoadCentroid,text=u"Browse for Centroid file...",command=self.OnCentroidBrowseClick)
		CentroidBrowse.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# File loaded
		CentroidLoaded = Tkinter.Label(LoadCentroid,text=u"DRV8818centroid.txt",anchor="w")
		CentroidLoaded.grid(row=0,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		## Load feeder file
		self.FeederList = []
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
		
		## Instruction plan step
		# Home
		Home = Tkinter.Button(InstructionPlan,text=u"Home",command=self.OnHomeClick)
		Home.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Previous Instruction
		PreviousInstruction = Tkinter.Button(InstructionPlan,text=u"Select previous",command=self.OnPreviousInstructionClick)
		PreviousInstruction.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Execute Instruction
		ExecuteInstruction = Tkinter.Button(InstructionPlan,text=u"Execute selected",command=self.OnExecuteInstructionClick)
		ExecuteInstruction.grid(row=2,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Next Instruction
		NextInstruction = Tkinter.Button(InstructionPlan,text=u"Select next",command=self.OnNextInstructionClick)
		NextInstruction.grid(row=3,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		## Instruction plan viewer		
		self.InstructionPlanListBox = Tkinter.Listbox(InstructionPlan,width=90)
		self.InstructionPlanListBox.grid(row=0,column=1,sticky='NSEW',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=4)
	
		InstructionPlanScrollBar = Tkinter.Scrollbar(InstructionPlan)
		InstructionPlanScrollBar.grid(row=0,column=1,sticky='NSE',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=4)
		
		self.InstructionPlanListBox.config(yscrollcommand=InstructionPlanScrollBar.set)
		InstructionPlanScrollBar.config(command=self.InstructionPlanListBox.yview)				
				
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
		# Wake up grbl
		self.SerialConnection.write("\r\n\r\n")
		time.sleep(2)   # Wait for grbl to initialize
		self.SerialConnection.flushInput()  # Flush startup text in serial input
		
	def OnDisconnectClick(self):
		self.DebuggerValue.set(u"Disconnect clicked")
		self.SerialConnection.close()
		
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
		
	def CentroidAndFeederLoaded(self):
		# check if centroid and feeder are loaded	
		if(self.CentroidList and self.FeederList):
			CentroidListLength = len(self.CentroidList) - 1
			# populate instructions list box
			for i in range(CentroidListLength):
				self.InstructionPlanListBox.insert(i,"Pick "+self.CentroidList[i][1]+" "+self.CentroidList[i][10]+" ("+self.CentroidList[i][0]+") from Feeder"+self.FeederList[i][1]+" ("+self.FeederList[i][2]+","+self.FeederList[i][3]+"), rotate "+self.CentroidList[i][9]+" degrees, and place at "+self.CentroidList[i][2]+","+self.CentroidList[i][3]+"")				 
		
			# Generate gcode
			self.Gcode = []
			for i in range(CentroidListLength):
				self.Gcode.append("g0 x"+self.FeederList[i][2]+" y"+self.FeederList[i][3]+" f1600")
				self.Gcode.append("g0 x"+self.CentroidList[i][2]+" y"+self.CentroidList[i][3]+" f1600")
			
			print self.Gcode
			
			for i in range(CentroidListLength):
				print self.Gcode[i]
				self.SerialConnection.write(self.Gcode[i] + '\n') # Send g-code block to grbl
		
		
	def OnCentroidBrowseClick(self):
		self.DebuggerValue.set(u"Browse for centroid clicked")		
		
		# Open the centroid file and convert it into a list of lists, CentroidList
		# The parent list is a list of the file's line numbers.
		# Each child list is of the form [Designator, Footprint, Mid X, Mid Y, Ref X, Ref Y, Pad X, Pad Y, TB, Rotation, Comment]
		CentroidFile = open('C:/Users/jmcalvay/Documents/Dropbox/Projects/GitHub/boardforge/DRV8818centroid.txt','r')
		CentroidLines = CentroidFile.readlines()
		"Read Line: %s" % (CentroidLines)
		CentroidLength = len(CentroidLines) - 1
		
		for i in range(2, CentroidLength):
			CentroidSplitLines = CentroidLines[i].split()
			
			# Remove mil suffix
			CentroidLinesNoMil = []
			SplitLinesLength = len(CentroidSplitLines)
			
			for j in range(SplitLinesLength):
				CentroidLinesNoMil.append(CentroidSplitLines[j].rstrip('mil'))
			
			# Convert mils to inches
			CentroidLinesInches = CentroidLinesNoMil
			
			for j in range(2, 8):
				CentroidLinesInches[j] = str(float(CentroidLinesInches[j])/1000)
			
			self.CentroidList.append(CentroidLinesInches)
		
		self.CentroidAndFeederLoaded()
		
	def OnFeederBrowseClick(self):
		self.DebuggerValue.set(u"Browse for feeder clicked")		
		
		# To do:  make file to list of list conversions a function that gets called by centroid and feeder
		# Open the feeder file and convert it into a list of lists, FeederList
		# The parent list is a list of the file's line numbers.
		# Each child list is of the form [Designator, Feeder, FeederX, FeederY, Ref X, Ref Y, Pad X, Pad Y, TB, Rotation, Comment]
		FeederFile = open('C:/Users/jmcalvay/Documents/Dropbox/Projects/GitHub/boardforge/DRV8818feeder.txt','r')
		FeederLines = FeederFile.readlines()
		"Read Line: %s" % (FeederLines)
		FeederLength = len(FeederLines) - 1
		
		for i in range(2, FeederLength):
			FeederSplitLines = FeederLines[i].split()
			
			# Remove mil suffix
			FeederLinesNoMil = []
			FeederSplitLinesLength = len(FeederSplitLines)
			
			for j in range(FeederSplitLinesLength):
				FeederLinesNoMil.append(FeederSplitLines[j].rstrip('mil'))
			
			# Convert mils to inches
			FeederLinesInches = FeederLinesNoMil
			
			for j in range(2, 8):
				FeederLinesInches[j] = str(float(FeederLinesInches[j])/1000)
			
			self.FeederList.append(FeederLinesInches)		
		
		self.CentroidAndFeederLoaded()
		
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
		
	def OnPreviousInstructionClick(self):
		self.DebuggerValue.set(u"Previous Instruction clicked")

	def OnExecuteInstructionClick(self):
		self.DebuggerValue.set(u"Execute Instruction clicked")		
		
	def OnNextInstructionClick(self):
		self.DebuggerValue.set(u"Next Instruction clicked")
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