import tkinter.ttk as ttk
from tkinter import *
from PIL import ImageTk, Image
import os


class front_db:
    def __init__(self, root):
        self.root = root
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        # use the next line if you also want to get rid of the titlebar
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        self.root.title("Attendance Management System")
        self.root.bind("<Escape>", exit)

        self.background = ImageTk.PhotoImage(file="images/background.jpg")
        self.faceimg = ImageTk.PhotoImage(file="images/face.jpg")
        self.top_icon = ImageTk.PhotoImage(file="images/fronttopleft.jpg")
        self.fdimg = ImageTk.PhotoImage(file= "images/facedetector.jpg")
        self.lgimg = ImageTk.PhotoImage(file = "images/login.jpg")

        # Background Image
        bg_lb = Label(self.root, image=self.background).pack()

        # Top frame
        self.top_frame = Frame(self.root, bg="#0c2454")
        self.top_frame.place(x=0, y=0, relwidth=1)
        # Top Left Image
        self.lb1 = Label(self.top_frame, image=self.top_icon, bd=0, )
        self.lb1.grid(row=0, column=0)

        # Top Title
        self.title = Label(self.top_frame, text="FACE RECOGNIZATION ATTENDANCE SYSTEM", bg="#0c2454", fg="#87a81b",
                           height="3", font='Algerian 37 bold underline', width=36, padx=20)
        self.title.grid(row=0, column=1)

        self.lg_btn = Button(self.root, image=self.fdimg, bd=0, command=self.det)
        self.lg_btn.place(x=250, y=250, )

        self.fd_btn = Button(self.root, image=self.lgimg, bd=0, command=self.login)
        self.fd_btn.place(x=800, y=250,)

    def login(self):
        os.system('python loginpage.py')
        exit()

    def det(self):
        os.system('python detector.py')
        exit()




root=Tk()
objfd = front_db(root)
root.mainloop()
