__author__ = 'Steve'

from Tkinter import *

class MainWindowFrame(Frame):
    def __init__(self, master=None, timestampToStart=0, myGuiHandler=None):
        Frame.__init__(self, master)
        # self.after(timestampToStart*1000, self.initializationProcess)
        self.initializationProcess(myGuiHandler)


    def initializationProcess(self, myGuiHandler):
        self.myGuiHandler = myGuiHandler
        if (self.master != None):
            self.master.wm_title("Jdl Creator")
            self.pack(side=TOP, fill=BOTH, expand=YES)
        # self.master.overrideredirect(True)
        self.lift()
        self.populateFrame()



    def populateFrame(self):
        if (not self.myGuiHandler == None):
            self.CreateFileButton = Button(master=self, text="Create File", command=self.myGuiHandler.showSaveWindow)
            self.CreateFileButton.pack(side=BOTTOM)
            self.AboutButton = Button(master=self, text='About', command=self.myGuiHandler.showAboutWindow)
            self.AboutButton.pack(side =LEFT)


    def main(self):
        print "hello"
        # do nothing


if __name__ == "__main__":
    root = Tk()
    window = MainWindowFrame(root)
    window.main()

    root.mainloop()