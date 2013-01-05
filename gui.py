#    This file is part of Board Forge (TM) www.boardforge.com
#
#    Board Forge (TM) is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Board Forge is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Board Forge (TM).  If not, see <http://www.gnu.org/licenses/>.

'''
# from http://www.daniweb.com/software-development/python/threads/191210/python-gui-programming#
#!/usr/bin/env python

# display an image using Tkinter
import Tkinter as tk
root = tk.Tk()

# pick an image file you have in your working directory
# or use full path, Tkinter only reads .gif image files
# (filenames are case sensitive on Ubuntu/Linux)
image_file = "logo.gif"
photo = tk.PhotoImage(file=image_file)
root.title(image_file)

# put the image on a typical widget
label = tk.Label(root,image=photo)
label.pack(padx=5, pady=5)
root.mainloop()
'''

# from http://sebsauvage.net/python/gui/
import Tkinter

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		self.grid()
		
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
		
		# Manage resizing
		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,False)
		self.update()
		self.geometry(self.geometry())
		
		# Focus on text box
		self.entry.focus_set()
		self.entry.selection_range(0,Tkinter.END)
		
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
if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('Board Forge - www.boardforge.com')
	app.mainloop()