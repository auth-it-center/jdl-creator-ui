__author__ = 'Steve'

import JDL_ControlFile
import SplashScr
from Tkinter import *
import tkFileDialog
import time
import MainWindowFrame
from AboutWindowFrame import *
import sidebarFrame
import buttonFrame


class GuiHandler:

    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        self.mainWindow = Toplevel(self.root)
        self.mainWindow.protocol("WM_DELETE_WINDOW", self.mainWindow.master.destroy) # close the application if closed
        self.mainWindow.withdraw()
        # self.mainWindow.iconify()

        self.splashWindow = Toplevel(self.root)
        self.mySplash = SplashScr.SplashScreen(self.splashWindow)
        self.mySplash.destroySplashScreen(5)


        self.sidebarFrame = sidebarFrame()
        self.buttonFrame = buttonFrame()

        # set the mainWindow position
        width = 0.5
        height = 0.3
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        w = ws*width
        h = ws*height
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.mainWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.mainFrame = MainWindowFrame.MainWindowFrame(self.mainWindow, myGuiHandler=self)


    def _populate_GUI(self, categoryLabels, fieldLabels):
        print "not implemented"
        # for category in sorted(JDL_ControlFile.Menu):
        #     categoryLabels.append(Label(self.mainFrame, text=category))
        #
        # for i in range(0, len(categoryLabels)-1):
        #     self.mainFrame.columnconfigure(i, pad=3)
        #
        # # print JDL_ControlFile.Menu
        # # for entry in sorted(JDL_ControlFile.Menu):
        # #     fieldLabels[entry](JDL_ControlFile.Menu[entry])
        # #
        # # print type(JDL_ControlFile.Menu)
        #
        # i=0
        # for label in categoryLabels:
        #     label.grid(row=0, column=i)
        #     label.config(font=self.labelFont)
        #     i+=1

    def showSaveWindow(self):
        print "showSaveWindow to be completed after checkboxes"
        filename = tkFileDialog.asksaveasfilename(parent=self.root,
                                                  filetypes=[('jdl files', '.jdl'), ('all files', '.*')],
                                                  initialfile='*.jdl')

        # NOT COMPLETED YET

    def showAboutWindow(self):
        self.AboutWindow = Toplevel(master=self.root)
        self.myAboutWindowFrame = AboutWindowFrame(master=self.AboutWindow)
        self.myAboutWindowFrame.pack(side=TOP)

    def main(self):
        self.root.wm_title("JDL Creator")

        categoryLabels = []
        self.labelFont = ('arial', 18, 'bold')

        fieldLabels = {}
        self._populate_GUI(categoryLabels, fieldLabels)
        # self.root.attributes('-topmost', 1)
        # self.root.update()
        # self.root.attributes('-topmost', 0)

        self.root.update()
        time.sleep(5)
        self.mainWindow.deiconify()
        self.mainWindow.update()

        self.root.mainloop()



# define a point of execution in your file
if __name__=='__main__':
    myGuiHandler = GuiHandler()
    myGuiHandler.main()
