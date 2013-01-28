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
#	File opening and parsing
#		File browsing - http://tkinter.unpythonic.net/wiki/tkFileDialog
#		File open - http://www.tutorialspoint.com/python/python_files_io.htm
#		File readlines - http://www.peterbe.com/plog/blogitem-040312-1
#		String split - http://www.webmasterwords.com/python-split-and-join-examples
#	Listboxes
#		Gcode area listbox - http://www.tutorialspoint.com/python/tk_listbox.htm
#		Gcode area scrollbar - http://effbot.org/zone/tkinter-scrollbar-patterns.htm
#	Multithreading - http://www.tutorialspoint.com/python/python_multithreading.htm
#   Serial control - http://onehossshay.wordpress.com/2011/08/26/grbl-a-simple-python-interface/
#	Windows - http://effbot.org/tkinterbook/toplevel.htm


# Import libraries for gui
import Tkinter, Tkconstants, tkFileDialog

# Import libraries for serial communication
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
		## Operation
		Status = Tkinter.Frame(self,bg=Background)
		Status.grid(row=0,column=0,padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=3)
		
		InstructionPlan = Tkinter.Frame(self,bg=Background)
		InstructionPlan.grid(row=1,column=0,padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=3)	
		
		AutomaticControl = Tkinter.Frame(self,bg=Background)
		AutomaticControl.grid(row=2,column=0,padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=3)			
		
		## Setup
		ConnectMachine = Tkinter.Frame(self,bg=Background)
		ConnectMachine.grid(row=3,column=0,padx=SummaryCellPadding,pady=SummaryCellPadding,columnspan=3)				

		# Board locations		
		BoardLocationsSummary = Tkinter.Frame(self,bg=Background)
		BoardLocationsSummary.grid(row=4,column=0,sticky='NW',padx=SummaryCellPadding,pady=SummaryCellPadding)		
		
		BoardLocations = Tkinter.Toplevel()
		BoardLocations.title("Set board locations manually")
		
		SetBoardLocations = Tkinter.Frame(BoardLocations,bg=Background)
		SetBoardLocations.grid(row=0,column=0,sticky='NW',padx=SummaryCellPadding,pady=SummaryCellPadding)		

		# Feeder lane locations
		FeederLaneLocationsSummary = Tkinter.Frame(self,bg=Background)
		FeederLaneLocationsSummary.grid(row=4,column=1,sticky='NW',padx=SummaryCellPadding,pady=SummaryCellPadding)	

		FeederLaneLocations = Tkinter.Toplevel()
		FeederLaneLocations.title("Set feeder lane locations manually")
		
		SetFeederLocations = Tkinter.Frame(FeederLaneLocations,bg=Background)
		SetFeederLocations.grid(row=0,column=0,sticky='NW',padx=SummaryCellPadding,pady=SummaryCellPadding)			
		
		# Component locations
		ComponentLocationsSummary = Tkinter.Frame(self,bg=Background)
		ComponentLocationsSummary.grid(row=4,column=2,sticky='NW',padx=SummaryCellPadding,pady=SummaryCellPadding)	
					
		# Jog
		JogWindow = Tkinter.Toplevel()
		JogWindow.title("Jog")		
		
		JogFrame = Tkinter.Frame(JogWindow,bg=Background)
		JogFrame.grid(row=8,column=0,padx=SummaryCellPadding,pady=SummaryCellPadding)		
		
		
		### Layout details
		## Machine status
		StatusLabel = Tkinter.Label(Status,text=u"\n X:  5.0 inches     Y:  6.0 inches     Z:  1.0 inches     Rotation: 90 degrees     Vacuum:  ON")
		StatusLabel.grid(row=0,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		## Instruction plan and vision	
		# Previous Instruction
		PreviousInstruction = Tkinter.Button(InstructionPlan,text=u"Select previous",command=self.OnPreviousInstructionClick)
		PreviousInstruction.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Execute Instruction
		ExecuteInstruction = Tkinter.Button(InstructionPlan,text=u"Execute selected",command=self.OnExecuteInstructionClick)
		ExecuteInstruction.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Next Instruction
		NextInstruction = Tkinter.Button(InstructionPlan,text=u"Select next",command=self.OnNextInstructionClick)
		NextInstruction.grid(row=2,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Instruction plan viewer		
		self.InstructionPlanListBox = Tkinter.Listbox(InstructionPlan,width=90)
		self.InstructionPlanListBox.grid(row=0,column=1,sticky='NSEW',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=3)
	
		InstructionPlanScrollBar = Tkinter.Scrollbar(InstructionPlan)
		InstructionPlanScrollBar.grid(row=0,column=1,sticky='NSE',padx=DetailsCellPadding,pady=DetailsCellPadding,rowspan=3)
		
		self.InstructionPlanListBox.config(yscrollcommand=InstructionPlanScrollBar.set)
		InstructionPlanScrollBar.config(command=self.InstructionPlanListBox.yview)				
		
		# Vision
		Vision = Tkinter.Label(InstructionPlan,text=u"Vision",fg='white',bg='black',width='35',height='10')
		Vision.grid(row=1,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)					
		
		
		## Automatic controls			
		# Feed rate
		FeedRateLabel = Tkinter.Label(AutomaticControl,text=u"Feed rate",anchor="w")
		FeedRateLabel.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		FeedRateScale = Tkinter.Scale(AutomaticControl,orient='horizontal',command=self.FeedRateScaleSlide)
		FeedRateScale.grid(row=0,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Play
		Play = Tkinter.Button(AutomaticControl,text=u"Play",command=self.OnPlayClick)
		Play.grid(row=0,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)		

		# Pause
		self.IsPaused = Tkinter.BooleanVar()
		self.IsPaused = False
		print self.IsPaused
		
		Pause = Tkinter.Button(AutomaticControl,text=u"PAUSE",command=self.OnPauseClick,bg='red',fg='white')
		Pause.grid(row=0,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)	

		# Stop
		Stop = Tkinter.Button(AutomaticControl,text=u"Stop",command=self.OnStopClick)
		Stop.grid(row=0,column=4,padx=DetailsCellPadding,pady=DetailsCellPadding)				

		# Debugger
		self.DebuggerValue = Tkinter.StringVar()
		label = Tkinter.Label(AutomaticControl,textvariable=self.DebuggerValue,anchor="w",bg="white")
		label.grid(row=0,column=5,padx=DetailsCellPadding,pady=DetailsCellPadding)
		self.DebuggerValue.set(u"Debugger")
				
		
		## Connect machine		
		# Find Machine
		FindMachine = Tkinter.Button(ConnectMachine,text=u"Find machine",command=self.OnFindMachineClick)
		FindMachine.grid(row=0,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)
				
		# Serial port selector
		SerialPort = Tkinter.StringVar()
		SerialPort.set("COM1")
		SerialPortList = Tkinter.OptionMenu(ConnectMachine, SerialPort, "COM1","COM2","COM3",command=self.SerialPortSelected)
		SerialPortList.grid(row=0,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Connect
		# self.SerialConnection = serial.Serial('COM12',115200)
		Connect = Tkinter.Button(ConnectMachine,text=u"Connect",command=self.OnConnectClick)
		Connect.grid(row=0,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)	
		
		# Disconnect
		Disconnect = Tkinter.Button(ConnectMachine,text=u"Disconnect",command=self.OnDisconnectClick)
		Disconnect.grid(row=0,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# ConnectionStatus
		ConnectionStatus = Tkinter.Label(ConnectMachine,text=u"Connected on COM8",anchor="w")
		ConnectionStatus.grid(row=0,column=4,padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		
		## Set board locations
		BoardLocationsLabel = Tkinter.Label(BoardLocationsSummary,text=u"Set board locations",anchor="w")
		BoardLocationsLabel.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)

		# Set board locations manually
		LocateBoardsManually = Tkinter.Button(BoardLocationsSummary,text=u"Manually...",command=self.OnLocateBoardsManuallyClick)
		LocateBoardsManually.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Find board locations with vision
		LocateBoardsVision = Tkinter.Button(BoardLocationsSummary,text=u"With vision...",command=self.OnLocateBoardsVisionClick)
		LocateBoardsVision.grid(row=2,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Browse for file
		LocateBoardsFile = Tkinter.Button(BoardLocationsSummary,text=u"From file...",command=self.OnLocateBoardsFileClick)
		LocateBoardsFile.grid(row=3,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		# Board A origin
		SummaryBoardAOriginLabel = Tkinter.Label(BoardLocationsSummary,text=u"Board A origin:  X: 1 in, Y: 2 in, Z: 3 in, A:  5 degrees")
		SummaryBoardAOriginLabel.grid(row=4,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)		
			
		# Board B origin
		SummaryBoardAOriginLabel = Tkinter.Label(BoardLocationsSummary,text=u"Board B origin:  X: 1 in, Y: 2 in, Z: 3 in, A:  5 degrees")
		SummaryBoardAOriginLabel.grid(row=5,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)			
		
		# Save board locations
		SaveBoardLocations = Tkinter.Button(BoardLocationsSummary,text=u"Save board locations to file...",command=self.OnSaveBoardLocationsClick)
		SaveBoardLocations.grid(row=6,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)		
		
		
		## Manually set board locations
		BoardLabel = Tkinter.Label(SetBoardLocations,text=u"Relate points on the digital board to points on physical boards")
		BoardLabel.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=6)	

		# Digital reference 1
		DigitalReference1Label = Tkinter.Label(SetBoardLocations,text=u"Digital reference 1")
		DigitalReference1Label.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		DigitalReference1XLabel = Tkinter.Label(SetBoardLocations,text=u"X: ")
		DigitalReference1XLabel.grid(row=1,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		self.DigitalReference1X = Tkinter.StringVar()
		self.entry = Tkinter.Entry(SetBoardLocations,textvariable=self.DigitalReference1X,width='5')
		self.entry.grid(row=1,column=2,sticky='W')
		self.DigitalReference1X.set(u"")
		
		DigitalReference1YLabel = Tkinter.Label(SetBoardLocations,text=u"Y: ")
		DigitalReference1YLabel.grid(row=1,column=3,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		self.DigitalReference1Y = Tkinter.StringVar()
		self.entry = Tkinter.Entry(SetBoardLocations,textvariable=self.DigitalReference1Y,width='5')
		self.entry.grid(row=1,column=4,sticky='W')
		self.DigitalReference1Y.set(u"")	

		SetDigitalReference1 = Tkinter.Button(SetBoardLocations,text=u"Set",command=self.OnSetDigitalReference1Click)
		SetDigitalReference1.grid(row=1,column=5,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		

		# Digital reference 2
		DigitalReference2Label = Tkinter.Label(SetBoardLocations,text=u"Digital reference 2")
		DigitalReference2Label.grid(row=2,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		DigitalReference2XLabel = Tkinter.Label(SetBoardLocations,text=u"X: ")
		DigitalReference2XLabel.grid(row=2,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		self.DigitalReference2X = Tkinter.StringVar()
		self.entry = Tkinter.Entry(SetBoardLocations,textvariable=self.DigitalReference2X,width='5')
		self.entry.grid(row=2,column=2,sticky='W')
		self.DigitalReference2X.set(u"")
		
		DigitalReference2YLabel = Tkinter.Label(SetBoardLocations,text=u"Y: ")
		DigitalReference2YLabel.grid(row=2,column=3,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		self.DigitalReference2Y = Tkinter.StringVar()
		self.entry = Tkinter.Entry(SetBoardLocations,textvariable=self.DigitalReference2Y,width='5')
		self.entry.grid(row=2,column=4,sticky='W')
		self.DigitalReference2Y.set(u"")	

		SetDigitalReference2 = Tkinter.Button(SetBoardLocations,text=u"Set",command=self.OnSetDigitalReference2Click)
		SetDigitalReference2.grid(row=2,column=5,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		# Board A
		BoardALabel = Tkinter.Label(SetBoardLocations,text=u"\nBoard A")
		BoardALabel.grid(row=3,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=6)			
		
		# Reference 1		
		BoardAPhysicalBoardReference1Label = Tkinter.Button(SetBoardLocations,text=u"Set physical reference 1...",command=self.OnSetBoardAPhysicalReference1Click)
		BoardAPhysicalBoardReference1Label.grid(row=4,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		GetBoardAPhysicalReference1 = Tkinter.Label(SetBoardLocations,text=u"X: 1 in, Y: 2 in")
		GetBoardAPhysicalReference1.grid(row=4,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=5)	
		
		# Reference 2
		BoardAPhysicalBoardReference2Label = Tkinter.Button(SetBoardLocations,text=u"Set physical reference 2...",command=self.OnSetBoardAPhysicalReference2Click)
		BoardAPhysicalBoardReference2Label.grid(row=5,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		GetBoardAPhysicalReference2 = Tkinter.Label(SetBoardLocations,text=u"X: 1 in, Y: 2 in")
		GetBoardAPhysicalReference2.grid(row=5,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=5)	

		# Origin
		BoardAOriginLabel = Tkinter.Label(SetBoardLocations,text=u"Origin:  ")
		BoardAOriginLabel.grid(row=6,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		BoardAOrigin = Tkinter.Label(SetBoardLocations,text=u"X: 1 in, Y: 2 in, Z: 3 in, A:  5 degrees")
		BoardAOrigin.grid(row=6,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=5)			
		
		# Board B
		BoardBLabel = Tkinter.Label(SetBoardLocations,text=u"\nBoard B")
		BoardBLabel.grid(row=7,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=6)			
		
		# Reference 1		
		BoardBPhysicalBoardReference1Label = Tkinter.Button(SetBoardLocations,text=u"Set physical reference 1...",command=self.OnSetBoardBPhysicalReference1Click)
		BoardBPhysicalBoardReference1Label.grid(row=8,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		GetBoardBPhysicalReference1 = Tkinter.Label(SetBoardLocations,text=u"X: 1 in, Y: 2 in")
		GetBoardBPhysicalReference1.grid(row=8,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=5)	
			
		# Reference 2
		BoardBPhysicalBoardReference2Label = Tkinter.Button(SetBoardLocations,text=u"Set physical reference 2...",command=self.OnSetBoardBPhysicalReference2Click)
		BoardBPhysicalBoardReference2Label.grid(row=9,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		GetBoardBPhysicalReference2 = Tkinter.Label(SetBoardLocations,text=u"X: 1 in, Y: 2 in")
		GetBoardBPhysicalReference2.grid(row=9,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=5)	
		
		# Origin
		BoardBOriginLabel = Tkinter.Label(SetBoardLocations,text=u"Origin:  ")
		BoardBOriginLabel.grid(row=10,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		BoardBOrigin = Tkinter.Label(SetBoardLocations,text=u"X: 1 in, Y: 2 in, Z: 3 in, A:  5 degrees \n")
		BoardBOrigin.grid(row=10,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=5)			

		# Done button
		BoardLocationsDone = Tkinter.Button(SetBoardLocations,text=u"Done",command=self.OnBoardLocationsDoneClick)
		BoardLocationsDone.grid(row=11,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=5)		
		

		## Set feeder lane locations
		FeederLaneLocationsLabel = Tkinter.Label(FeederLaneLocationsSummary,text=u"Set feeder lane locations",anchor="w")
		FeederLaneLocationsLabel.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)

		# Set feeder locations manually
		LocateFeederLanesManually = Tkinter.Button(FeederLaneLocationsSummary,text=u"Manually...",command=self.OnLocateFeederLanesManuallyClick)
		LocateFeederLanesManually.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Find feeder locations with vision
		LocateFeederLanesVision = Tkinter.Button(FeederLaneLocationsSummary,text=u"With vision...",command=self.OnLocateFeederLanesVisionClick)
		LocateFeederLanesVision.grid(row=2,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Browse for file
		LocateFeederLanesFile = Tkinter.Button(FeederLaneLocationsSummary,text=u"From file...",command=self.OnLocateFeederLanesFileClick)
		LocateFeederLanesFile.grid(row=3,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	
			
		# Feeder group A label
		SummaryFeederGroupA = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder group A",anchor="w")
		SummaryFeederGroupA.grid(row=4,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
			
		# Feeder lane A1
		SummaryFeederA1Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane A1 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederA1Location.grid(row=5,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane A2
		SummaryFeederA2Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane A2 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederA2Location.grid(row=6,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		

		# Feeder lane A3
		SummaryFeederA3Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane A3 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederA3Location.grid(row=7,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane A4
		SummaryFeederA4Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane A4 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederA4Location.grid(row=8,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		

		# Feeder lane A5
		SummaryFeederA5Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane A5 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederA5Location.grid(row=9,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)				

		# Feeder group B label
		SummaryFeederGroupB = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder group B",anchor="w")
		SummaryFeederGroupB.grid(row=4,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
			
		# Feeder lane B1
		SummaryFeederB1Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane B1 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederB1Location.grid(row=5,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane B2
		SummaryFeederB2Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane B2 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederB2Location.grid(row=6,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane B3
		SummaryFeederB3Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane B3 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederB3Location.grid(row=7,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane B4
		SummaryFeederB4Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane B4 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederB4Location.grid(row=8,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane B5
		SummaryFeederB5Location = Tkinter.Label(FeederLaneLocationsSummary,text=u"Feeder lane B5 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		SummaryFeederB5Location.grid(row=9,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Save feeder lane locations
		SaveFeederLaneLocations = Tkinter.Button(FeederLaneLocationsSummary,text=u"Save feeder lane locations to file...",command=self.OnSaveFeederLaneLocationsClick)
		SaveFeederLaneLocations.grid(row=10,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		
		## Set feeder lane locations manually
		# Feeder group A label
		FeederGroupA = Tkinter.Label(SetFeederLocations,text=u"Feeder group A",anchor="w")
		FeederGroupA.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		# Feeder group A fiducial 1 set location
		FeederAFiducial1SetLocation = Tkinter.Button(SetFeederLocations,text=u"Set fiducial 1 location...",command=self.OnFeederGroupAFiducial1Click)
		FeederAFiducial1SetLocation.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder group A fiducial 1 location
		FeederAFiducial2GetLocation = Tkinter.Label(SetFeederLocations,text=u"X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederAFiducial2GetLocation.grid(row=1,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Feeder group A fiducial 2 set location
		FeederAFiducial2SetLocation = Tkinter.Button(SetFeederLocations,text=u"Set fiducial 2 location...",command=self.OnFeederGroupAFiducial2Click)
		FeederAFiducial2SetLocation.grid(row=2,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder group A fiducial 2 location
		FeederAFiducial2GetLocation = Tkinter.Label(SetFeederLocations,text=u"X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederAFiducial2GetLocation.grid(row=2,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			

		# FeederA1 label
		FeederA1LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane A1 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederA1LocationLabel.grid(row=3,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)

		# FeederA2 label
		FeederA2LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane A2 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederA2LocationLabel.grid(row=4,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)		

		# FeederA3 label
		FeederA3LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane A3 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederA3LocationLabel.grid(row=5,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)

		# FeederA4 label
		FeederA4LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane A4 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederA4LocationLabel.grid(row=6,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)		

		# FeederA5 label
		FeederA5LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane A5 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederA5LocationLabel.grid(row=7,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)			
		
		# Feeder group B label
		FeederGroupB = Tkinter.Label(SetFeederLocations,text=u"\nFeeder group B",anchor="w")
		FeederGroupB.grid(row=8,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Feeder group B fiducial 1 set location
		FeederBFiducial1SetLocation = Tkinter.Button(SetFeederLocations,text=u"Set fiducial 1 location...",command=self.OnFeederGroupBFiducial1Click)
		FeederBFiducial1SetLocation.grid(row=9,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder group B fiducial 1 location
		FeederBFiducial2GetLocation = Tkinter.Label(SetFeederLocations,text=u"X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederBFiducial2GetLocation.grid(row=9,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Feeder group B fiducial 2 set location
		FeederBFiducial2SetLocation = Tkinter.Button(SetFeederLocations,text=u"Set fiducial 2 location...",command=self.OnFeederGroupBFiducial2Click)
		FeederBFiducial2SetLocation.grid(row=10,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder group B fiducial 2 location
		FeederBFiducial2GetLocation = Tkinter.Label(SetFeederLocations,text=u"X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederBFiducial2GetLocation.grid(row=10,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)						

		# FeederB1 label
		FeederB1LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane B1 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederB1LocationLabel.grid(row=11,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)

		# FeederB2 label
		FeederB2LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane B2 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederB2LocationLabel.grid(row=12,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)		

		# FeederB3 label
		FeederB3LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane B3 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederB3LocationLabel.grid(row=13,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)

		# FeederB4 label
		FeederB4LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane B4 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederB4LocationLabel.grid(row=14,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)		

		# FeederB5 label
		FeederB5LocationLabel = Tkinter.Label(SetFeederLocations,text=u"Feeder lane B5 X: 0 in, Y: 1 in, Z: 2 in",anchor="w")
		FeederB5LocationLabel.grid(row=15,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)		
		
		
		## Set component locations
		FeederLaneLocationsLabel = Tkinter.Label(ComponentLocationsSummary,text=u"Set component locations",anchor="w")
		FeederLaneLocationsLabel.grid(row=0,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=4)

		# Load centroid file	
		self.CentroidList = []
		
		CentroidBrowse = Tkinter.Button(ComponentLocationsSummary,text=u"Load centroid file...",command=self.OnCentroidBrowseClick)
		CentroidBrowse.grid(row=1,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=4)
				
		# Load component locations file
		LocateComponentsFile = Tkinter.Button(ComponentLocationsSummary,text=u"Load component locations from file...",command=self.OnLocateComponentsFileClick)
		LocateComponentsFile.grid(row=2,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=4)
		
		# Feeder group A
		FeederGroupALabel = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder group A",anchor="w")
		FeederGroupALabel.grid(row=3,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=4)			
		
		# Feeder lane A1 component
		FeederA1Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane A1",anchor="w")
		FeederA1Label.grid(row=4,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederA1ComponentStr = Tkinter.StringVar()
		FeederA1ComponentStr.set("R1")
		FeederA1Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederA1ComponentStr, "R1","R2","R3",command=self.FeederA1ComponentSelected)
		FeederA1Component.grid(row=4,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane A2 component
		FeederA2Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane A2",anchor="w")
		FeederA2Label.grid(row=5,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederA2ComponentStr = Tkinter.StringVar()
		FeederA2ComponentStr.set("R1")
		FeederA2Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederA2ComponentStr, "R1","R2","R3",command=self.FeederA2ComponentSelected)
		FeederA2Component.grid(row=5,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane A3 component
		FeederA3Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane A3",anchor="w")
		FeederA3Label.grid(row=6,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederA3ComponentStr = Tkinter.StringVar()
		FeederA3ComponentStr.set("R1")
		FeederA3Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederA3ComponentStr, "R1","R2","R3",command=self.FeederA3ComponentSelected)
		FeederA3Component.grid(row=6,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane A4 component
		FeederA4Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane A4",anchor="w")
		FeederA4Label.grid(row=7,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederA4ComponentStr = Tkinter.StringVar()
		FeederA4ComponentStr.set("R1")
		FeederA4Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederA4ComponentStr, "R1","R2","R3",command=self.FeederA4ComponentSelected)
		FeederA4Component.grid(row=7,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane A5 component
		FeederA5Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane A5",anchor="w")
		FeederA5Label.grid(row=8,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederA5ComponentStr = Tkinter.StringVar()
		FeederA5ComponentStr.set("R1")
		FeederA5Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederA5ComponentStr, "R1","R2","R3",command=self.FeederA5ComponentSelected)
		FeederA5Component.grid(row=8,column=1,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Feeder group B
		FeederGroupBLabel = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder group B",anchor="w")
		FeederGroupBLabel.grid(row=3,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)			
		
		# Feeder lane B1 component
		FeederB1Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane B1",anchor="w")
		FeederB1Label.grid(row=4,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederB1ComponentStr = Tkinter.StringVar()
		FeederB1ComponentStr.set("R1")
		FeederB1Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederB1ComponentStr, "R1","R2","R3",command=self.FeederB1ComponentSelected)
		FeederB1Component.grid(row=4,column=3,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane B2 component
		FeederB2Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane B2",anchor="w")
		FeederB2Label.grid(row=5,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederB2ComponentStr = Tkinter.StringVar()
		FeederB2ComponentStr.set("R1")
		FeederB2Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederB2ComponentStr, "R1","R2","R3",command=self.FeederB2ComponentSelected)
		FeederB2Component.grid(row=5,column=3,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane B3 component
		FeederB3Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane B3",anchor="w")
		FeederB3Label.grid(row=6,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederB3ComponentStr = Tkinter.StringVar()
		FeederB3ComponentStr.set("R1")
		FeederB3Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederB3ComponentStr, "R1","R2","R3",command=self.FeederB3ComponentSelected)
		FeederB3Component.grid(row=6,column=3,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane B4 component
		FeederB4Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane B4",anchor="w")
		FeederB4Label.grid(row=7,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederB4ComponentStr = Tkinter.StringVar()
		FeederB4ComponentStr.set("R1")
		FeederB4Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederB4ComponentStr, "R1","R2","R3",command=self.FeederB4ComponentSelected)
		FeederB4Component.grid(row=7,column=3,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)

		# Feeder lane B5 component
		FeederB5Label = Tkinter.Label(ComponentLocationsSummary,text=u"Feeder lane B5",anchor="w")
		FeederB5Label.grid(row=8,column=2,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)	

		FeederB5ComponentStr = Tkinter.StringVar()
		FeederB5ComponentStr.set("R1")
		FeederB5Component = Tkinter.OptionMenu(ComponentLocationsSummary, FeederB5ComponentStr, "R1","R2","R3",command=self.FeederB5ComponentSelected)
		FeederB5Component.grid(row=8,column=3,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding)			
		
		# Save component locations to file
		ComponentSave = Tkinter.Button(ComponentLocationsSummary,text=u"Save component locations to file...",command=self.OnComponentSaveClick)
		ComponentSave.grid(row=9,column=0,sticky='W',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=4)		
		
		
		## Jog dialog
		# Minus X
		MinusX = Tkinter.Button(JogFrame,text=u"-X",command=self.OnMinusXClick)
		MinusX.grid(row=1,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Plus X
		PlusX = Tkinter.Button(JogFrame,text=u"+X",command=self.OnPlusXClick)
		PlusX.grid(row=1,column=2,padx=DetailsCellPadding,pady=DetailsCellPadding)						
		
		# Minus Y
		MinusY = Tkinter.Button(JogFrame,text=u"-Y",command=self.OnMinusYClick)
		MinusY.grid(row=2,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Plus Y
		PlusY = Tkinter.Button(JogFrame,text=u"+Y",command=self.OnPlusYClick)
		PlusY.grid(row=0,column=1,padx=DetailsCellPadding,pady=DetailsCellPadding)						
		
		# Minus Z
		MinusZ = Tkinter.Button(JogFrame,text=u"-Z",command=self.OnMinusZClick)
		MinusZ.grid(row=0,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)		
		
		# Plus Z
		PlusZ = Tkinter.Button(JogFrame,text=u"+Z",command=self.OnPlusZClick)
		PlusZ.grid(row=2,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=2)				
		
		# Current position
		CurrentPosition = Tkinter.Label(JogFrame,text=u"X:  5.0 inches     Y:  6.0 inches     Z:  1.0 inches")
		CurrentPosition.grid(row=3,column=0,padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=4)		
		
		# Units
		UnitsLabel = Tkinter.Label(JogFrame,text=u"Units (in)",anchor="w")
		UnitsLabel.grid(row=4,column=3,padx=DetailsCellPadding,pady=DetailsCellPadding)
		
		UnitsStr = Tkinter.StringVar()
		UnitsStr.set("0.001")
		UnitsDropDown = Tkinter.OptionMenu(JogFrame, UnitsStr, "0.001","0.01","0.1",command=self.UnitsSelected)
		UnitsDropDown.grid(row=4,column=4,padx=DetailsCellPadding,pady=DetailsCellPadding)		
		
		# Done button
		JogDone = Tkinter.Button(JogFrame,text=u"Done",command=self.OnJogDoneClick)
		JogDone.grid(row=5,column=0,sticky='E',padx=DetailsCellPadding,pady=DetailsCellPadding,columnspan=5)

		
		# Create list to store gcode when centroid and feeder are loaded
		self.Gcode = []
		
		# Manage resizing
		self.grid_columnconfigure(0,weight=1) # enable resizing
		self.resizable(True,True) # enable x resizing and enable y resizing
		self.update() # disable automatic resizing
		self.geometry(self.geometry()) # disable automatic resizing

		
	### Button click events
	## Step
	def OnPreviousInstructionClick(self):
		self.DebuggerValue.set(u"Previous Instruction clicked")

	def OnExecuteInstructionClick(self):
		self.DebuggerValue.set(u"Execute Instruction clicked")		
		
	def OnNextInstructionClick(self):
		self.DebuggerValue.set(u"Next Instruction clicked")	
	
	
	## Automatic
	def FeedRateScaleSlide(self,FeedRate):
		self.DebuggerValue.set(u"Feed rate "+FeedRate+"%")		
		
	def OnPlayClick(self):
		self.DebuggerValue.set(u"Play clicked")
		# If centroid and feeder lists are populated, then send gcode to machine
		if(self.CentroidList and self.FeederList):
			CentroidListLength = len(self.CentroidList) - 1
			
			for i in range(CentroidListLength):
				if(self.IsPaused == False):
					print self.Gcode[i]
					self.SerialConnection.write(self.Gcode[i] + '\n')
					time.sleep(0.25)			

	def OnPauseClick(self):
		self.DebuggerValue.set(u"Pause clicked")		
		self.IsPaused = not(self.IsPaused)
		print self.IsPaused
		
	def OnStopClick(self):
		self.DebuggerValue.set(u"Stop clicked")

		
	## Connect machine
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
		
	def SerialPortSelected(self,SerialPort):
		self.DebuggerValue.set(u"Serial port selected:  "+SerialPort)
		
	def OnDisconnectClick(self):
		self.DebuggerValue.set(u"Disconnect clicked")
		self.SerialConnection.close()			

	## Locate boards
	# Summary
	def OnLocateBoardsManuallyClick(self):
		self.DebuggerValue.set(u"Locate boards manually clicked")
		
	def OnLocateBoardsVisionClick(self):
		self.DebuggerValue.set(u"Locate boards with vision clicked")		
		
	def OnLocateBoardsFileClick(self):
		self.DebuggerValue.set(u"Locate boards from file clicked")	

	def OnSaveBoardLocationsClick(self):
		self.DebuggerValue.set(u"Save board locations clicked")			
		
	# Manually		
	def OnSetDigitalReference1Click(self):
		self.DebuggerValue.set(u"Digital reference 1 X: "+self.DigitalReference1X.get()+", Y: "+self.DigitalReference1Y.get())

	def OnSetDigitalReference2Click(self):
		self.DebuggerValue.set(u"Digital reference 2 X: "+self.DigitalReference2X.get()+", Y: "+self.DigitalReference2Y.get())		
		
	def OnSetBoardAPhysicalReference1Click(self):
		self.DebuggerValue.set(u"Board A physical reference 1 clicked")

	def OnSetBoardAPhysicalReference2Click(self):
		self.DebuggerValue.set(u"Board A physical reference 2 clicked")	

	def OnSetBoardBPhysicalReference1Click(self):
		self.DebuggerValue.set(u"Board B physical reference 1 clicked")

	def OnSetBoardBPhysicalReference2Click(self):
		self.DebuggerValue.set(u"Board B physical reference 2 clicked")			

	def OnBoardLocationsDoneClick(self):
		self.DebuggerValue.set(u"Board locations done clicked")			

	## Locate feeders
	# Summary
	def OnLocateFeederLanesManuallyClick(self):
		self.DebuggerValue.set(u"Locate feeder lanes manually clicked")
		
	def OnLocateFeederLanesVisionClick(self):
		self.DebuggerValue.set(u"Locate feeder lanes with vision clicked")		
		
	def OnLocateFeederLanesFileClick(self):
		self.DebuggerValue.set(u"Locate feeder lanes from file clicked")		
	
	def OnSaveFeederLaneLocationsClick(self):
		self.DebuggerValue.set(u"Save feeder lane locations clicked")	
		
	# Manually	
	def OnFeederGroupAFiducial1Click(self):
		self.DebuggerValue.set(u"Set Feeder group A Fiducial 1 location clicked")		
		
	def OnFeederGroupAFiducial2Click(self):
		self.DebuggerValue.set(u"Set Feeder group A Fiducial 2 location clicked")		

	def OnFeederGroupBFiducial1Click(self):
		self.DebuggerValue.set(u"Set Feeder group B Fiducial 1 location clicked")
		
	def OnFeederGroupBFiducial2Click(self):
		self.DebuggerValue.set(u"Set Feeder group B Fiducial 2 location clicked")			

	def OnFeederLaneLocationsDoneClick(self):
		self.DebuggerValue.set(u"Feeder lane locations done clicked")		
		
	## Locate components
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
		
		# print self.CentroidList
		
		self.CentroidAndFeederLoaded()		
			
	def OnLocateComponentsFileClick(self):
		self.DebuggerValue.set(u"Browse for component location clicked")		

	def FeederA1ComponentSelected(self,FeederA1ComponentStr):
		self.DebuggerValue.set(u"Feeder A1 component selected:  "+FeederA1ComponentStr)
		
	def FeederA2ComponentSelected(self,FeederA2ComponentStr):
		self.DebuggerValue.set(u"Feeder A2 component selected:  "+FeederA2ComponentStr)				
				
	def FeederA3ComponentSelected(self,FeederA3ComponentStr):
		self.DebuggerValue.set(u"Feeder A3 component selected:  "+FeederA3ComponentStr)		
				
	def FeederA4ComponentSelected(self,FeederA4ComponentStr):
		self.DebuggerValue.set(u"Feeder A4 component selected:  "+FeederA4ComponentStr)

	def FeederA5ComponentSelected(self,FeederA5ComponentStr):
		self.DebuggerValue.set(u"Feeder A5 component selected:  "+FeederA5ComponentStr)		
		
	def FeederB1ComponentSelected(self,FeederB1ComponentStr):
		self.DebuggerValue.set(u"Feeder B1 component selected:  "+FeederB1ComponentStr)
		
	def FeederB2ComponentSelected(self,FeederB2ComponentStr):
		self.DebuggerValue.set(u"Feeder B2 component selected:  "+FeederB2ComponentStr)		
		
	def FeederB3ComponentSelected(self,FeederB3ComponentStr):
		self.DebuggerValue.set(u"Feeder B3 component selected:  "+FeederB3ComponentStr)		
				
	def FeederB4ComponentSelected(self,FeederB4ComponentStr):
		self.DebuggerValue.set(u"Feeder B4 component selected:  "+FeederB4ComponentStr)

	def FeederB5ComponentSelected(self,FeederB5ComponentStr):
		self.DebuggerValue.set(u"Feeder B5 component selected:  "+FeederB5ComponentStr)			

	def OnComponentSaveClick(self):
		self.DebuggerValue.set(u"Save component locations to file clicked")		
		
	## Populate instruction plan
	def CentroidAndFeederLoaded(self):
		# check if centroid and feeder are loaded	
		if(self.CentroidList and self.FeederList):
			CentroidListLength = len(self.CentroidList) - 1
			# populate instructions list box
			for i in range(CentroidListLength):
				self.InstructionPlanListBox.insert(i,"Pick "+self.CentroidList[i][1]+" "+self.CentroidList[i][10]+" ("+self.CentroidList[i][0]+") from Feeder"+self.FeederList[i][1]+" ("+self.FeederList[i][2]+","+self.FeederList[i][3]+"), rotate "+self.CentroidList[i][9]+" degrees, and place at "+self.CentroidList[i][2]+","+self.CentroidList[i][3]+"")				 
		
			# Generate gcode
			for i in range(CentroidListLength):
				self.Gcode.append("g0 x"+self.FeederList[i][2]+" y"+self.FeederList[i][3]+" f1600")
				self.Gcode.append("g0 x"+self.CentroidList[i][2]+" y"+self.CentroidList[i][3]+" f1600")
	
	
	## Jog
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

	def UnitsSelected(self,UnitStr):
		self.DebuggerValue.set(u"Units:  "+UnitStr)		

	def OnJogDoneClick(self):
		self.DebuggerValue.set(u"Jog done clicked")		
	
	# Define board and feeder locations
	def OnBoardFeederBrowseClick(self):
		self.DebuggerValue.set(u"Browse for board and feeder location file clicked")		
		
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
	
	
	
if __name__ == "__main__":
	app = boardforge_tk(None)
	app.title('Board Forge - www.boardforge.com')
	app.mainloop()