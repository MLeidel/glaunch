# glaunch.pyw
# Michael Leidel (2020)
from tkinter import *
import webbrowser
import subprocess
import os, sys
from PIL import Image, ImageTk

#   cd \python\glaunch
#   python glaunch.py

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        with open("glaunch.ini") as f:
            self.lst1 = f.readlines()
        #for l in lst1:
        i = 0
        for l in self.lst1:
            lst2 = l.split("|")
            png = lst2[0]
            cmd = lst2[1].strip()
            load = Image.open("mif/" + png)
            render = ImageTk.PhotoImage(load)
            self.img = Button(self, image=render,
                              command=lambda i=i: self.btn_click(i))
            self.img.image = render
            self.img.pack()
            i += 1


    def btn_click(self, i):
        l = self.lst1[i].split("|")
        cmd = l[1].strip()
        if cmd.startswith("http"):
            webbrowser.open(cmd)
        else:
            lcmd = cmd.split(" ")  # convert the command line into a python List
            subprocess.Popen(lcmd)

def on_closing(e=None):
    ''' save position on exit
        executes at WM_DELETE_WINDOW event - see below '''
    with open("winfo", "w") as fout:
        fout.write(root.geometry())
    root.destroy()

root = Tk()
app = Window(root)

# change working directory to path for this file
p = os.path.realpath(__file__)
os.chdir(os.path.dirname(p))

# position the window
if os.path.isfile("winfo"):
    with open("winfo") as f:
        lcoor = f.read()
    root.geometry(lcoor.strip())
else:  # each button is 30 thus 30 x 9 = 270
    root.geometry('28x270+1+420') # WxH+left+top

# set the title bar icon image
photo = ImageTk.PhotoImage(Image.open("app_icon.png"))
root.iconphoto(False, photo)

root.protocol("WM_DELETE_WINDOW", on_closing)  # save position on exit
root.attributes("-topmost", True)

if len(sys.argv) == 1:  # with no arguments don't display the window caption bar
    root.overrideredirect(True)
    # with an argument the caption bar will display
    # thus allowing you to position the window.

root.mainloop()
