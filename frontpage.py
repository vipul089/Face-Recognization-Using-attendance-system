import tkinter.ttk as ttk
from tkinter import *
from PIL import ImageTk, Image
import os
import time


class FrontPage:
    def __init__(self, root):
        self.root = root
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        # use the next line if you also want to get rid of the titlebar
        root.overrideredirect(1)
        root.pack_propagate(0)
        root.geometry("%dx%d+0+0" % (w, h))
        self.root.title("Attendance Management System")
        self.root.bind("<Escape>", exit)

        # images
        self.background = ImageTk.PhotoImage(file="images/background.jpg")
        self.faceimg = ImageTk.PhotoImage(file="images/face.jpg")
        self.top_icon = ImageTk.PhotoImage(file="images/fronttopleft.jpg")
        self.bottom_image = ImageTk.PhotoImage(file="images/frontrightbottom.jpg")

        # Background Image
        bg_lb = Label(self.root, image=self.background).pack()

        # Top frame
        self.top_frame = Frame(self.root, bg="#0c2454")
        self.top_frame.place(x=0, y=0, relwidth=1)
        # Top Left Image
        self.lb1 = Label(self.top_frame, image=self.top_icon, bd=0,)
        self.lb1.grid(row=0, column=0)

        # Top Title
        self.title = Label(self.top_frame, text="FACE RECOGNIZATION ATTENDANCE SYSTEM", bg="#0c2454", fg="#87a81b",height="3", font='Algerian 37 bold underline', width=36, padx=20)
        self.title.grid(row=0, column=1)

        # Code For Middle Frame
        self.framemiddle = Frame(self.root,)
        self.framemiddle.place(x=420, y=200)

        # Code For Front Center Image
        self.centerimg=Label(self.framemiddle, image=self.faceimg, bd=0,)
        self.centerimg.grid(row=0, column=0)

        
        #Code for about
        self.bottom_frame = Frame(self.root,)
        self.bottom_frame.place(x=1160, y=600)

        self.botimglb = Label(self.bottom_frame, image=self.bottom_image, bd=0)
        self.botimglb.grid(row=0, columnspan=2)

        self.bottomlbl = Label(self.bottom_frame, text="Designed & Developed By:", wraplength=100, width=10, anchor="w", justify=LEFT, font='Arial 11 bold', bg="#0c2454", fg="#87a81b", )
        self.bottomlbl.grid(row=1, column=0)

        self.bottomlb2 = Label(self.bottom_frame, text="Sajal Bansal, Vipul Goyal & Abhinav Joshi", wraplength=100, width=11, justify=LEFT, anchor="w", font='Arial 11 bold', bg="#0c2454", fg="White", )
        self.bottomlb2.grid(row=1, column=1)

        # Code For Progress Bar
        self.pgbar = ttk.Progressbar(self.root, length=502, orient=HORIZONTAL, value=0, mode="determinate",)
        self.pgbar.place(x=420, y=515)
        self.next()


    def next(self):
        for i in range(101):
            time.sleep(0.03)
            self.pgbar['value']=i+1
            self.pgbar.update()
        os.system('python front_dashboard.py')
        exit()

    



root=Tk()
objf=FrontPage(root)
root.mainloop()


