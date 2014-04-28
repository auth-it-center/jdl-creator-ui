__author__ = 'Steve'

import JDL_ControlFile
import SplashScr
from Tkinter import *
import tkFileDialog
import time
import MainWindowFrame
from AboutWindowFrame import *
from SidebarFrame import SidebarFrame


class GuiHandler:
    def setGeometry(self, rootcontainer=None, container=None, width=0.5, height=0.3):
        """ Sets the geometry of a window
        """
        if (container is None) | (rootcontainer is None):
            raise ReferenceError

        ws = rootcontainer.winfo_screenwidth()
        hs = rootcontainer.winfo_screenheight()
        w = ws * width
        h = ws * height
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        container.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self):
        self.root = Tk()
        self.root.withdraw()

        # Create the main window of the application
        self.mainWindow = Toplevel(self.root)
        self.mainWindow.resizable(0, 0)  # you can set it as resizable in a later version
        self.mainWindow.protocol("WM_DELETE_WINDOW", self.mainWindow.master.destroy)  # close the application if closed
        self.mainWindow.withdraw()
        # self.mainWindow.iconify()

        # Show the splash screen
        self.showSplash()

        # set the mainWindow position
        self.setGeometry(self.root, self.mainWindow)

        # populate the mainWindow
        self.populateMainWindow()

        # self.mainFrame = MainWindowFrame.MainWindowFrame(self.mainWindow, myGuiHandler=self)


    def showSplash(self):
        # Create and show the splash screen for 5 sec.
        self.splashWindow = Toplevel(self.root)
        self.mySplash = SplashScr.SplashScreen(self.splashWindow)
        self.mySplash.destroySplashScreen(5)

    def populateMainWindow(self):
        # The mainWindow consists of:
        # * the menu
        # * the sidebarFrame
        # * the mainWindowFrame
        try:
            # MENU
            self.menuBar = Menu(self.mainWindow)


            filemenu = Menu(self.menuBar, tearoff=0)
            filemenu.add_command(label="Save", command=None)
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=self.root.destroy)
            self.menuBar.add_cascade(label="File", menu=filemenu)

            editmenu = Menu(self.menuBar, tearoff=0)
            editmenu.add_command(label='Select all', command=None)
            editmenu.add_command(label='Clear all', command=None)
            self.menuBar.add_cascade(label='Edit', menu=editmenu)

            helpmenu = Menu(self.menuBar, tearoff=0)
            helpmenu.add_command(label='Help', command=None)
            helpmenu.add_command(label='Examples', command=self.showHelpWindow)
            helpmenu.add_separator()
            helpmenu.add_command(label='About ...', command=self.showAboutWindow)
            self.menuBar.add_cascade(label='Help', menu=helpmenu)
            self.mainWindow.config(menu=self.menuBar)

            raise NotImplementedError

        except NotImplementedError as ee:
            print "Not all functionality has been implemented yet"

        # SIDEBAR
        self.sidebarFrame = SidebarFrame(master=self.mainWindow, myGuiHandler=self)
        # self.sidebarFrame.place(bordermode=OUTSIDE, height=100, width=100)
        self.sidebarFrame.pack(side=LEFT, expand=NO, fill=Y)
        # self.mainWindowFrame = MainWindowFrame.MainWindowFrame(self.mainWindow)
        # self.mainWindowFrame.pack(side=RIGHT)

        # MAIN WINDOW

    def showSaveWindow(self):
        print "showSaveWindow to be completed after checkboxes"
        filename = tkFileDialog.asksaveasfilename(parent=self.root,
                                                  filetypes=[('jdl files', '.jdl'), ('all files', '.*')],
                                                  initialfile='*.jdl')

        raise NotImplementedError
        # NOT COMPLETED YET

    def showAboutWindow(self):
        self.AboutWindow = Toplevel(master=self.root)
        self.myAboutWindowFrame = AboutWindowFrame(master=self.AboutWindow)
        self.myAboutWindowFrame.pack(side=TOP)

    def showHelpWindow(self):
        # raise NotImplementedError
        self.ExamplesWindow = Toplevel(master=self.root)
        self.ExamplesWindow.resizable(0,0)
        self.ExamplesWindow.wm_title("Help")
        self.ExamplesFrame = PanedWindow(master=self.ExamplesWindow, orient=HORIZONTAL, showhandle=True,
                                         )
        # self.ExamplesFrame.proxy_place(self.ExamplesFrame.master.winfo_width()/2, self.ExamplesFrame.master.winfo_height()/2)
        self.ExamplesFrame.config(height=250, width=500)
        self.ExamplesFrame.pack(fill=BOTH, expand=True)
        self.GuiHelpFrame = Frame(master=self.ExamplesFrame)
        self.ExamplesFrame.add(self.GuiHelpFrame)
        self.TerminalHelpFrame = Frame(master=self.ExamplesFrame)
        self.ExamplesFrame.add(self.TerminalHelpFrame)

        for pane in self.ExamplesFrame.panes():
            self.ExamplesFrame.paneconfig(pane, minsize=200, width=self.ExamplesFrame.master.winfo_width()/2-10)

        self.GuiHelpTitle = Label(master=self.GuiHelpFrame, text="GUI application Help")
        self.GuiHelpTitle.pack(side=TOP)
        self.GuiHelp = Text(master=self.GuiHelpFrame)
        self.GuiHelp.pack(side=TOP)
        self.GuiHelp.config(height=220, width=220)
        helpfile = open('guihelp.txt', 'r')
        helpstrings = helpfile.readlines()
        helpfile.close()
        for s in helpstrings:
            self.GuiHelp.insert(END, s)
        self.GuiHelp.config(state=DISABLED, padx=10) # in order not to be editable


        self.TerminalHelpTitle = Label(master=self.TerminalHelpFrame, text="Terminal application Help")
        self.TerminalHelpTitle.pack(side=TOP)
        self.TerminalHelp = Text(master=self.TerminalHelpFrame)
        self.TerminalHelp.pack(side=TOP)
        self.TerminalHelp.config(height=220, width=220)
        helpfile = open('terminalhelp.txt', 'r')
        helpstrings = helpfile.readlines()
        helpfile.close()
        for s in helpstrings:
            self.TerminalHelp.insert(END, s)
        self.TerminalHelp.config(state=DISABLED)

    def main(self):
        self.mainWindow.wm_title("JDL Creator")

        categoryLabels = []
        self.labelFont = ('arial', 18, 'bold')

        # fieldLabels = {}
        # self.populate_GUI(categoryLabels, fieldLabels)
        # self.root.attributes('-topmost', 1)
        # self.root.update()
        # self.root.attributes('-topmost', 0)

        self.root.update()
        time.sleep(5)
        self.mainWindow.deiconify()
        self.mainWindow.update()

        # in order to play nice with OS X
        # self.root.attributes('-topmost', 1)
        # self.root.update()
        # self.root.attributes('-topmost', 0)
        # self.root.update()

        # self.root.iconify()
        # self.root.deiconify()
        # ----------------------------------
        self.root.mainloop()

# define a point of execution in your file
if __name__ == '__main__':
    myGuiHandler = GuiHandler()
    myGuiHandler.main()
