import JDL_ControlFile
from Tkinter import *

menu = JDL_ControlFile.Menu

class selectionFrame(Frame):
	checks = []
	
	def __init__(self, master = None):
		Frame.__init__(self,master)
		self.initializationProcess()
		self.populateGrid()
			
	def initializationProcess(self):
		self.master.wm_title("Selection Frame")
		self.grid(row=0)
		
	def populateGrid(self):
		categories = self.getCategories()
		c = 0
		for category in categories:
			label = Label(self, text=category[3:-1], font=("Arial", 16)).grid(row = 0, column = c)
			category_options = self.getOptions(category)
			r = 1
			for option in category_options:
				var = IntVar()
				label = Checkbutton(self, text=option, font=("Arial", 14), variable = var, command = self.test).grid(row = r, column = c)
				self.checks.append(var)
				r = r + 1
			c = c + 1
	
	def test(self):
		for item in self.checks:
			print item.get()
		print 
		print 
		
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
	
