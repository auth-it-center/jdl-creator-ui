__author__ = 'Steve'


from Tkinter import *
import time

class SplashScreen(Frame):
    def __init__(self, master=None, width=0.4, height=0.25, useFactor=True):
        Frame.__init__(self, master)
        self.pack(side=TOP, fill=BOTH, expand=YES)

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = (useFactor and ws*width) or width
        h = (useFactor and ws*height) or height
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.master.overrideredirect(True)
        self.lift()
        self.populateSplashScreen()

    def destroyMe(self):
        self.master.destroy()
        # self.master.withdraw()

    def populateSplashScreen(self):
        # root = Toplevel()
        self.config(bg="#990000")
    
        titleLabel = Label(self, text="Welcome to JDL Creator 2.0\n\n\n", pady=25)
        supportLabel = Label(self, text="More info at\n\t(support@grid.auth.gr)")
        titleLabel.pack(side=TOP, expand=YES)
        titleLabel.config(bg="#990000", fg="#ffffff", justify=CENTER, font=("arial", 25))
        supportLabel.pack(side=BOTTOM, expand=YES)
        supportLabel.config(bg="#990000", fg="#ffffff", justify=CENTER, font=("arial", 20))
    
        myCanvas = Canvas(self)
        myCanvas.pack(side=BOTTOM, expand=YES)
        myCanvasBounds = (int(myCanvas.cget("width")), int(myCanvas.cget("height")))
        print myCanvasBounds
        lineSize = 100
        myCanvas.create_line(10, 90, 300, 90, fill='white')
        myCanvas.config(bg="#990000", highlightbackground="#990000")
        myCanvas.create_line(10, 100, 100, 100, fill='white', width=2)
        # myCanvas.create_line(myCanvasBounds[0]/2-lineSize/2, myCanvasBounds[1]-1, myCanvasBounds[0]/2+lineSize/2, myCanvasBounds[1]-1, width=2)


    def destroySplashScreen(self, timeToSleep=0):
        if timeToSleep > 0:
            # root.after(timeToSleep*1000, printMessage)
            self.master.after(timeToSleep*1000, self.destroyMe)

if __name__ == '__main__':
    root = Tk()
    mainWindow = Toplevel(root)
    root.withdraw()
    mySP = SplashScreen(mainWindow)
    mySP.populateSplashScreen()
    mySP.destroySplashScreen(5)
    mainWindow.attributes('-topmost', 1)
    mainWindow.update()
    mainWindow.attributes('-topmost', 0)
    mainWindow.mainloop()
