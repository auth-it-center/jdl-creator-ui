from Tkinter import *
from PIL import Image, ImageTk

class CheckableCategory(Frame):
  def __init__(self, master=None, cat_text=None, \
  image_off=None, image_on=None, state=NORMAL, command=None):
    Frame.__init__(self, master)
    if command is None:
      command=self.changeState
    self.isChecked = None
    self.checkbutton = Checkbutton(master=self, image=image_off, \
    selectimage=image_on, state=state, variable=self.isChecked, \
    command=command)
    self.label = Label(master=self, text=cat_text)
    self.state = state
    self.checkbutton.pack(side=LEFT)
    self.label.pack(side=RIGHT)

  def changeState(self):
    raise NotImplementedError

if __name__=='__main__':
  root = Tk()
  mainWindow = Toplevel(master=root)
  label = Label(master=mainWindow, text="sometextadsfa")
  label.pack()
  img_off = ImageTk.PhotoImage(Image.open('./Resources/triangle-small.jpg'))
  img_on = ImageTk.PhotoImage(Image.open('./Resources/triangle-small-on.jpg'))
  obj = CheckableCategory(master=mainWindow, cat_text='check_text_sample', \
   image_off=img_off, image_on=img_on)
  obj.pack()

  root.mainloop()
