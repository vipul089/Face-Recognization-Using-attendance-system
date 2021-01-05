from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkcalendar import DateEntry
import time
import sqlite3 as db
from datetime import datetime
import os

def back():
    if etype=="User":
        os.system('py user_dashboard.py')
    else:
        os.system('py admin_dashboard.py')
    root.destroy()


def deen():
    if(v.get()==1):
        cal1.config(state="normal")
        sbtn.config(state="active")
        cal2.config(state="disabled")
        cal3.config(state="disabled")
    elif(v.get() == 2):
        cal2.config(state="active")
        cal3.config(state="active")
        sbtn.config(state="active")
        cal1.config(state="disabled")


def remove_all():
    x= tv.get_children()
    if (x != '()'):
        for child in x:
            tv.delete(child)


def search():

    conn = db.connect('Attendance.db')
    cur = conn.cursor()
    tv.tag_configure('T', font=('Arial 14'))
    if (v.get() == 1):
        remove_all()
        find_time_query = cur.execute("Select * from attdata where id= ?",(cal1.get(),))
        attdata = find_time_query.fetchall()
        for i in attdata:
            tv.insert('', 'end', values=i, tags='T')
    elif(v.get()==2):
        remove_all()
        find_time_query = cur.execute("Select * from attdata where date BETWEEN ? AND ?", (cal2.get(), cal3.get()))
        attdata = find_time_query.fetchall()
        for i in attdata:
            tv.insert('', 'end', values=i, tags='T')
    conn.commit()
    conn.close()


class Report:
    def __init__(self, root, empname):
        self.root = root
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        self.root.title("Attendance Management System")
        self.root.bind("<Escape>", exit)

        today = datetime.today()
        # images
        self.background = ImageTk.PhotoImage(file="images/background.jpg")
        self.man_icon = ImageTk.PhotoImage(file="images/man.jpg")
        self.pass_icon = ImageTk.PhotoImage(file="images/pass.jpg")
        self.top_icon = ImageTk.PhotoImage(file="images/fronttopleft.jpg")
        bb = Image.open("images/back.png")
        self.back_image = ImageTk.PhotoImage(bb)

        # Background Image
        bg_lb = Label(self.root, image=self.background).pack()

        # Top frame
        self.top_frame = Frame(self.root, bg="#112034")
        self.top_frame.place(x=0, y=0, relwidth=1)

        # Top Left Image
        self.lb1 = Label(self.top_frame, image=self.top_icon, bd=0)
        self.lb1.grid(row=0, column=0)

        # Top Title
        self.title = Label(self.top_frame, text="FACE RECOGNIZATION ATTENDANCE SYSTEM", bg="#112034", fg="#87a81b",
                           height="3", font='Algerian 37 bold underline', width=36, padx=20)
        self.title.grid(row=0, column=1)

        # Dashboard Bar
        self.dashboard = Frame(self.root, bg='#93AAAA', )
        self.dashboard.place(x=0, y=171, relwidth=1, width=100)

        self.back = Button(self.dashboard, image=self.back_image, bg='#93AAAA', bd=0, activebackground="#78A1C5",
                           command=back)
        self.back.grid(row=0, column=0, )

        self.dashlb = Label(self.dashboard, text="Welcome :", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
        self.dashlb.grid(row=0, column=1, )

        self.name = Label(self.dashboard, text=empname, compound=LEFT, fg='#472074', font='Arial 18 bold',
                          bg='#93AAAA', )
        self.name.grid(row=0, column=2, )

        self.act = Label(self.dashboard, text="Report", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
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

        # Search Frame
        self.Login_frame = LabelFrame(self.root, bd=5, )
        self.Login_frame.place(x=200, y=230)

        global v
        v = IntVar()

        global radio_btn1, cal1, cal2, cal3, radio_btn2, cal1t, cal2t, cal3t
        cal1t = StringVar()
        cal2t = StringVar()
        cal3t = StringVar()

        radio_btn1 = Radiobutton(self.Login_frame, text="Emp Id", font='Arial 14 bold', value=1, command=deen, variable=v)
        radio_btn1.grid(row=0, column=0)

        cal1 = Entry(self.Login_frame, width=12, background='White', foreground='black', textvariable=cal1t)
        cal1.config(state="disabled")
        cal1.grid(row=0, column=1, ipady=2)

        lbor = Label(self.Login_frame, text="OR", font='Arial 14 bold')
        lbor.grid(row=0, column=2, ipadx=50, ipady=2)

        radio_btn2 = Radiobutton(self.Login_frame, text="Start Date", font='Arial 14 bold', value=2, command=deen,
                                 variable=v)
        radio_btn2.grid(row=0, column=3)
        cal2 = DateEntry(self.Login_frame, width=12, background='White', foreground='black', maxdate=today,
                         date_pattern="DD-MM-YYYY", textvariable=cal2t)
        cal2.config(state="disabled")
        cal2.grid(row=0, column=4, ipady=2)

        lbto = Label(self.Login_frame, text="To", font='Arial 14 bold')
        lbto.grid(row=0, column=5, ipadx=50, ipady=2)

        lbed = Label(self.Login_frame, text="End Date", font='Arial 14 bold')
        lbed.grid(row=0, column=6, ipady=2, padx=5)

        cal3 = DateEntry(self.Login_frame, width=12, background='White', foreground='black', maxdate=today,
                         date_pattern="DD-MM-YYYY", textvariable=cal3t)
        cal3.config(state="disabled")
        cal3.grid(row=0, column=7, ipady=2)

        global sbtn
        sbtn = Button(self.Login_frame, text="Search", font='Arial 14 bold', state="disabled", command=search, )
        sbtn.grid(row=0, column=8, padx=20)

        global tv, style
        style = ttk.Style()
        style.configure("Treeview", rowheight="30")
        style.configure("Treeview.Heading", font=('Arial 16 bold'))
        tv = ttk.Treeview(self.root, columns=(1, 2, 3, 4, 5), show="headings", height="14")
        tv.place(x=200, y=290, )
        sb = ttk.Scrollbar(self.root, orient="vertical", command=tv.yview)
        sb.place(x=1165, y=291, height="444")
        # sb.pack(side='right', fill='y')
        tv.configure(yscrollcommand=sb.set)
        tv.heading(1, text="Employee ID", )
        tv.column(1, minwidth=100, width=180, stretch=NO, anchor='center')
        tv.heading(2, text="Date")
        tv.column(2, minwidth=100, width=200, stretch=NO, anchor='center')
        tv.heading(3, text="Arrival Time")
        tv.column(3, minwidth=100, width=200, stretch=NO, anchor='center')
        tv.heading(4, text="Departure Time")
        tv.column(4, minwidth=100, width=200, stretch=NO, anchor='center')
        tv.heading(5, text="Working Hours")
        tv.column(5, minwidth=100, width=200, stretch=NO, anchor='center')

    def time(self):
        self.now = datetime.today().strftime('%I:%M:%S %p')
        self.time_t.config(text=self.now)
        self.time_t.after(1000, self.time)

    def date(self):
        self.now = datetime.today().strftime('%d-%m-%Y')
        self.date_d.config(text=self.now)


def fileopen():
    global eid, etype, ename
    with open('tempfile.temp', "r") as f:
        data = f.readlines()
        eid = data[0].rstrip()
        etype = data[1].rstrip()
    conn = db.connect('Attendance.db')
    cur = conn.cursor()
    find_detail_query = cur.execute("Select name from Detail where id= ?", (eid,))
    hh = find_detail_query.fetchone()
    ename = hh[0]
    conn.commit()
    conn.close()
    return eid, etype, ename


if __name__ == '__main__':
    fileopen()
    root = Tk()
    objf = Report(root, ename)
    root.mainloop()
