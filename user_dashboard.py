import tkinter.ttk as ttk
from tkinter import *
from PIL import ImageTk, Image
import os
from datetime import datetime
import sqlite3 as db

def fileopen():
    global eid, empname
    with open('tempfile.temp', "r") as f:
        data = f.readlines()
        eid = data[0].rstrip()
    conn = db.connect('Attendance.db')
    cur = conn.cursor()
    find_detail_query = cur.execute("Select name from Detail where id= ?", (eid,))
    hh = find_detail_query.fetchone()
    empname=hh[0]
    return eid, empname

def re():
    os.system('py userreport.py')
    root.destroy()

def changepass():
    os.system('py changepass.py')
    root.destroy()

def md():
    os.system('py updatedata.py')
    root.destroy()



def logout():
    os.system('py loginpage.py')
    root.destroy()


class dashboard:
    def __init__(self, root, empname):
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
        self.md_image = ImageTk.PhotoImage(file="images/md.jpg")
        self.re_image = ImageTk.PhotoImage(file="images/report.jpg")
        self.lo_image = ImageTk.PhotoImage(file="images/lo.jpg")
        self.cp_image = ImageTk.PhotoImage(file="images/cp.jpg")

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
        self.dashboard.place(x=0, y=171, relwidth=1, width=100)

        self.bl = Label(self.dashboard, text="     ", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
        self.bl.grid(row=0, column=0, )

        self.dashlb = Label(self.dashboard, text="Welcome :", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
        self.dashlb.grid(row=0, column=1,)

        self.name = Label(self.dashboard, text=empname, compound=LEFT, fg='#472074', font='Arial 18 bold',
                          bg='#93AAAA', )
        self.name.grid(row=0, column=2, )

        self.act = Label(self.dashboard, text="Dashboard", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
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

        self.md_btn = Button(self.root, image=self.md_image, bd=0, command=md)
        self.md_btn.place(x=75, y=250, )

        self.re_btn = Button(self.root, image=self.re_image, bd=0, command=re)
        self.re_btn.place(x=500, y=250, )

        self.cp_btn = Button(self.root, image=self.cp_image, bd=0, command=changepass)
        self.cp_btn.place(x=925, y=250, )

        self.lo_btn = Button(self.root, image=self.lo_image, bd=0, command=logout)
        self.lo_btn.place(x=75, y=480, )

    def time(self):
        self.now = datetime.today().strftime('%I:%M:%S %p')
        self.time_t.config(text=self.now)
        self.time_t.after(1000, self.time)

    def date(self):
        self.now = datetime.today().strftime('%d-%m-%Y')
        self.date_d.config(text=self.now)

if __name__ == '__main__':
    fileopen()
    root=Tk()
    objd=dashboard(root, empname)
    root.mainloop()


