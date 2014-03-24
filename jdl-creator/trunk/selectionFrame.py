import JDL_ControlFile
from Tkinter import *

menu = JDL_ControlFile.Menu

class selectionFrame(Frame):
	checks = []
	
	def __init__(self, master = None):
		Frame.__init__(self,master)
		self.initializationProcess()
		self.populateFrame()
			
	def initializationProcess(self):
		self.master.wm_title("Selection Frame")
		self.grid()
		
	def populateFrame(self):
		categories = self.getCategories()
		c = 0
		for category in categories:
			label = Label(self, text=category[3:-1], font=("Arial", 16, "bold")).grid(row = 0, column = c, ipadx=15)
			category_options = self.getOptions(category)
			r = 1
			for option in category_options:
				var = IntVar()
				check = Checkbutton(self, text=option, font=("Arial", 14), variable = var, command = self.getNumbersOfOptions).grid(row = r, column = c)
				self.checks.append(var)
				r = r + 1
			c = c + 1
		
	def getNumbersOfOptions(self):
		options = []
		counter = 0
		for item in self.checks:
			counter = counter + 1
			if item.get():
				options.append(counter)
		print options
		
	def getCategories(self):
		Categories = []
		i = 0
		for key in menu:
			Categories.append(key)
		Categories.sort()
		return Categories
		
	def getOptions(self,column):
		Options = menu[column]
		return Options
							
		
if __name__ == "__main__":
	root = Tk()
	sF = selectionFrame(master=root)
	root.mainloop()
	
