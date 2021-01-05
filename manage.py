import tkinter.ttk as ttk
from tkinter import *
from PIL import ImageTk, Image
import os
import time
from datetime import datetime
import sqlite3 as db

def back():
    os.system('py admin_dashboard.py')
    root.destroy()

def au():
    os.system('py adduser.py')
    root.destroy()

def eu():
    os.system('py updateuser.py')
    root.destroy()


def du():
    os.system('py deleteuser.py')
    root.destroy()

class Manage:
    def __init__(self, root, ename):
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
        self.bottom_image = ImageTk.PhotoImage(file="images/frontrightbottom.jpg")
        self.au_image = ImageTk.PhotoImage(file="images/au.jpg")
        self.eu_image = ImageTk.PhotoImage(file="images/eu.jpg")
        self.du_image = ImageTk.PhotoImage(file="images/du.jpg")

        bb = Image.open("images/back.png")
        self.back_image = ImageTk.PhotoImage(bb)

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

        # Dashboard Bar
        self.dashboard = Frame(self.root, bg='#93AAAA', )
        self.dashboard.place(x=0, y=171, relwidth=1,)

        self.back = Button(self.dashboard,  image=self.back_image, bg='#93AAAA', bd=0, activebackground = "#78A1C5", command=back)
        self.back.grid(row=0, column=0, )

        self.dashlb = Label(self.dashboard, text="Welcome :", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
        self.dashlb.grid(row=0, column=1, )

        self.name = Label(self.dashboard, text=ename, compound=LEFT, fg='#472074', font='Arial 18 bold',
                          bg='#93AAAA', )
        self.name.grid(row=0, column=2, )

        self.act = Label(self.dashboard, text="Manage User", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
        self.act.grid(row=0, column=3, padx=230, )

        self.time_lb = Label(self.dashboard, text="Time:", fg='#472074', font='Arial 18 bold', bg='#93AAAA')
        self.time_lb.grid(row=0, column=4, )

        self.time_t = Label(self.dashboard, fg='#472074', font='Arial 18 bold', bg='#93AAAA')
        self.time_t.grid(row=0, column=5, )
        self.time()

        self.time_lb = Label(self.dashboard, text=" | ", fg='#472074', font='Arial 16 bold', bg='#93AAAA')
        self.time_lb.grid(row=0, column=6, )

        self.date_lb = Label(self.dashboard, text="Date:", fg='#472074', font='Arial 18 bold', bg='#93AAAA')
        self.date_lb.grid(row=0, column=7, )

        self.date_d = Label(self.dashboard, compound=LEFT, fg='#472074', font='Arial 18 bold', bg='#93AAAA')
        self.date_d.grid(row=0, column=8, )
        self.date()

        self.au_btn = Button(self.root, image=self.au_image, bd=0, command=au)
        self.au_btn.place(x=75, y=250, )

        self.eu_btn = Button(self.root, image=self.eu_image, bd=0, command=eu)
        self.eu_btn.place(x=500, y=250, )

        self.du_btn = Button(self.root, image=self.du_image, bd=0, command=du )
        self.du_btn.place(x=925, y=250, )



    def time(self):
        self.now= datetime.today().strftime('%I:%M:%S %p')
        self.time_t.config(text=self.now)
        self.time_t.after(1000, self.time)

    def date(self):
        self.now= datetime.today().strftime('%d-%m-%Y')
        self.date_d.config(text=self.now)

def fileopen():
    global eid, empname
    with open('tempfile.temp', "r") as f:
        data = f.readlines()
        eid = data[0].rstrip()
    conn = db.connect('Attendance.db')
    cur = conn.cursor()
    find_detail_query = cur.execute("Select name from Detail where id= ?", (eid,))
    empname = find_detail_query.fetchone()
    return eid, empname



if __name__ == '__main__':
    fileopen()
    root=Tk()
    objd=Manage(root, empname)
    root.mainloop()


