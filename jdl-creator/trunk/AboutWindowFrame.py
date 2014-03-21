__author__ = 'Steve'

from Tkinter import *


class AboutWindowFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.wm_title("About")
        self.contentLabel = Label(self)
        content = self.loadFromFile()
        sumString = ''
        for string in content:
            sumString = sumString+'\n'+string
        self.contentLabel.config(text=sumString, bg='#E0E0E0')
        self.contentLabel.pack(side=TOP)

        # CreatorsLabel = Label(self, text="Created by Stefanos Laskaridis\n\tfor the Grid Infrastructure\n")
        # VersionLabel = Label(self, text="Version 0.1")
        #
        # CreatorsLabel.pack(side=TOP)
        # # CreatorsLabel.config(font=)
        # VersionLabel.pack(side=TOP)

    def loadFromFile(self):
        file = open('about.txt', 'r')
        content = file.readlines()
        return content

if __name__=="__main__":
    root = Tk()
    aboutFrame = AboutWindowFrame(master=root)
    aboutFrame.pack(side=TOP)
    root.mainloop()