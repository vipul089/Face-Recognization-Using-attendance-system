import tkinter.ttk as ttk
from tkinter import *
from PIL import ImageTk, Image
import os
import time
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3 as db
import random
from tkinter import messagebox
import smtplib
import cv2
import numpy as np


def samples():
    global empid
    if(name.get()=="" or fname.get()=="" or dob.get()==""):
        messagebox.showerror("Error", "Please First Fill Above Fields")
    else:
        nn=name.get()
        fn=fname.get()
        dobn=dob.get()
        empid=f"{str(nn.lower()[0:4])}{str(fn.lower()[0:2])}{str(dobn[0:2])}"
        sno = str(dobn[0:2]) + str(dobn[3:5]) + str(dobn[6:10])
        face_detect = cv2.CascadeClassifier('backend/haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)
        action = "All Samples Are Collected Successfully"
        sampleNum = 0
        while True:
            ret, img = cam.read();
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sampleNum = sampleNum + 1
                cv2.imwrite("samples/"+str(empid)+"."+str(sno)+"."+str(sampleNum)+".jpeg",gray[y:y+h, x:x+w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.waitKey(100)
            if (sampleNum <= 20):
                cv2.putText(img, str(sampleNum), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("Face", img)
                cv2.waitKey(1)
            else:
                cv2.putText(img, str(action), (20, 450), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)
                cv2.imshow("Face", img)
                cv2.waitKey(1)
                time.sleep(0.5)
                sambtn.configure(bg="Green")
                break
        cam.release()
        cv2.destroyAllWindows()


def back():
    os.system('py manage.py')
    root.destroy()

def remove_all():
    x= tv.get_children()
    if (x != '()'):
        for child in x:
            tv.delete(child)

def show():
    tv.tag_configure('T', font=('Arial 11'))
    query=cur.execute("Select * From Detail")
    total=query.fetchall()
    remove_all()
    for i in total:
        tv.insert('', 'end', values=i, tags='T')

def newid():
    global id,p
    id=StringVar()
    nn=name.get()
    fn=fname.get()
    dobn=dob.get()
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 8
    p = "".join(random.sample(s, passlen))
    id=f"{str(nn.lower()[0:4])}{str(fn.lower()[0:2])}{str(dobn[0:2])}"
    insertinlogin = ("INSERT into Login values(?,?,?)")
    runn1=cur.execute(insertinlogin,(id,p,"User"))
    conn.commit()

def send_email():
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("sajalbansal2010@gmail.com", "2010sajal")
        message = 'Subject: {}\n\n{}'.format("No Reply", f" Hi {name.get()} Your have Successfully Registerd. Please Login Using Following Credentials:- \n id={id} \n Password={p} \n Type = User")
        server.sendmail("sajalbansal2010@gmail.com", email.get(), message)
        server.quit()
    except:
        messagebox.showerror("Error","Email failed to send")

def save():
    dobn=dob.get()
    if (name.get()=="" or fname.get()=="" or email.get()=="" or mob.get()=="" or dob.get()=="" or jd.get()=="" or (sambtn['bg']=="RED")):
        messagebox.showerror("Error", "All Fields Are Mandatory")
    elif (len(mob.get()) < 10):
        messagebox.showerror("Error", "Invalid Mobile Number")
    else:
        newid()
        insertindetail = ("Insert into Detail values (?,?,?,?,?,?,?,?,?)")
        sno = str(dobn[0:2]) + str(dobn[3:5]) + str(dobn[6:10])
        runn2 = cur.execute(insertindetail, (id, name.get(), fname.get(), dob.get(),  jd.get(), email.get(), mob.get(), "YES", sno))
        conn.commit()
        show()
        if (runn2):
            send_email()
            messagebox.showinfo("Success", "User Added Successfully")

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

class Adduser:
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

        self.act = Label(self.dashboard, text="Add User", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
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


        self.frame=LabelFrame(root, bd=5, height=510, width=500, bg="#4D8BA0" )
        self.frame.place(x=20, y=240)

        self.namelb=Label(self.frame, text="Name", font='Arial 16 bold', bg="#4D8BA0", fg="#FFFFFF")
        self.namelb.grid(row=0, column=0, pady=5, padx=10, sticky="W")

        self.fnamelb = Label(self.frame, text="Father Name", font='Arial 16 bold', bg="#4D8BA0", fg="#FFFFFF")
        self.fnamelb.grid(row=1, column=0, pady=5, padx=10, sticky="W")

        self.doblb = Label(self.frame, text="Date Of Birth", font='Arial 16 bold', bg="#4D8BA0", fg="#FFFFFF")
        self.doblb.grid(row=2, column=0, pady=5, padx=10, sticky="W")

        self.jdlb = Label(self.frame, text="Joining Date", font='Arial 16 bold', bg="#4D8BA0", fg="#FFFFFF")
        self.jdlb.grid(row=3, column=0, pady=5, padx=10, sticky="W")

        self.emaillb = Label(self.frame, text="Email Address", font='Arial 16 bold', bg="#4D8BA0", fg="#FFFFFF")
        self.emaillb.grid(row=4, column=0, pady=5, padx=10, sticky="W")

        self.moblb = Label(self.frame, text="Mobile No.", font='Arial 16 bold', bg="#4D8BA0", fg="#FFFFFF")
        self.moblb.grid(row=5, column=0, pady=5, padx=10, sticky="W")

        self.samlb = Label(self.frame, text="Collect Samples", font='Arial 16 bold', bg="#4D8BA0", fg="#FFFFFF")
        self.samlb.grid(row=6, column=0, pady=5, padx=10, sticky="W")

        sbmtbtn=Button(self.frame, text= "Save", font="Arial 16 bold", bg="#4D8BA0", fg="#FFFFFF", bd=2, width=8, command=save)
        sbmtbtn.grid(row=7, columnspan=3, sticky=W, pady=10, padx=50)

        resetbtn = Button(self.frame, text="Reset", font="Arial 16 bold", bg="#4D8BA0", fg="#FFFFFF", bd=2, width=8, command=self.reset_values)
        resetbtn.grid(row=7, columnspan=3,  sticky=E, pady=10, padx=50)

        self.semlb = Label(self.frame, text=":", font="Arial 16 bold", bg="#4D8BA0", fg="#FFFFFF")
        self.semlb.grid(row=0, column=1, pady=5, padx=0)

        self.semlb = Label(self.frame, text=":", font="Arial 16 bold", bg="#4D8BA0", fg="#FFFFFF")
        self.semlb.grid(row=1, column=1, pady=5, padx=0)

        self.semlb = Label(self.frame, text=":", font="Arial 16 bold", bg="#4D8BA0", fg="#FFFFFF")
        self.semlb.grid(row=2, column=1, pady=5, padx=0)

        self.semlb = Label(self.frame, text=":", font="Arial 16 bold", bg="#4D8BA0", fg="#FFFFFF")
        self.semlb.grid(row=3, column=1, pady=5, padx=0)

        self.semlb = Label(self.frame, text=":", font="Arial 16 bold", bg="#4D8BA0", fg="#FFFFFF")
        self.semlb.grid(row=4, column=1, pady=5, padx=0)

        self.semlb = Label(self.frame, text=":", font="Arial 16 bold", bg="#4D8BA0", fg="#FFFFFF")
        self.semlb.grid(row=5, column=1, pady=5, padx=0)

        self.semlb = Label(self.frame, text=":", font="Arial 16 bold", bg="#4D8BA0", fg="#FFFFFF")
        self.semlb.grid(row=6, column=1, pady=5, padx=0)

        today = datetime.today()
        global name, fname, dob, jd, email, mob, sambtn, tv
        name = StringVar()
        fname = StringVar()
        dob = StringVar()
        jd = StringVar()
        email = StringVar()
        mob = StringVar()
        self.name_en=Entry(self.frame, textvariable=name, width=14, font=("Arial", 14), )
        self.name_en.grid(row=0, column=2, pady=5, padx=10, sticky=W)

        self.fname_en = Entry(self.frame, textvariable=fname, width=14, font=("Arial", 14), )
        self.fname_en.grid(row=1, column=2, pady=5, padx=10, sticky=W)

        self.dob_en = DateEntry(self.frame, width=22, background='White',foreground='black', maxdate=today, date_pattern="DD-MM-YYYY",  textvariable=dob)
        self.dob_en.grid(row=2, column=2, pady=10, padx=10,)

        self.jd_en = DateEntry(self.frame, width=22, background='White', foreground='black', maxdate=today,
                                date_pattern="DD-MM-YYYY", textvariable=jd)
        self.jd_en.grid(row=3, column=2, pady=10, padx=10, )

        self.email_en = Entry(self.frame, textvariable=email, width=14, font=("Arial", 14), )
        self.email_en.grid(row=4, column=2, pady=5, padx=10, sticky=W)

        self.mob_en = Entry(self.frame, textvariable=mob, width=14, font=("Arial", 14), )
        self.mob_en.grid(row=5, column=2, pady=5, padx=10, sticky=W)
        reg2 = self.mob_en.register(self.numbercheck)
        self.mob_en.config(validate="key", validatecommand=(reg2, '%P'))


        sambtn = Button(self.frame, text="Click Me!", font=("Arial", 12), height=1, width=16, bg="RED", activebackground="Blue", command=samples )
        sambtn.grid(row=6, column=2, pady=5, padx=10, sticky=W)



        style = ttk.Style()
        style.configure("Treeview", rowheight="30", width=100,)
        style.configure("Treeview.Heading", font=('Arial 14 bold'))
        tv = ttk.Treeview(self.root, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height="11")
        tv.place(x=440, y=240, )
        sb = ttk.Scrollbar(self.root, orient="vertical", command=tv.yview)
        sb.place(x=1325, y=241, height="355")
        hsb = ttk.Scrollbar(self.root, orient="horizontal", command=tv.xview)
        hsb.place(x=441, y=578, width="885")
        tv.configure(yscrollcommand=sb.set, xscrollcommand=hsb.set)
        tv.heading(1, text="Emp ID", )
        tv.column(1, minwidth=50, width=75, stretch=NO, anchor='center')
        tv.heading(2, text="Name")
        tv.column(2, minwidth=100, width=110, stretch=NO, anchor='center')
        tv.heading(3, text="FName")
        tv.column(3, minwidth=100, width=120, stretch=NO, anchor='center')
        tv.heading(4, text="DOB")
        tv.column(4, minwidth=100, width=90, stretch=NO, anchor='center')
        tv.heading(5, text="JD")
        tv.column(5, minwidth=100, width=90, stretch=NO, anchor='center')
        tv.heading(6, text="Email Id")
        tv.column(6, minwidth=100, width=198, stretch=NO, anchor='center')
        tv.heading(7, text="Mob No.")
        tv.column(7, minwidth=100, width=100, stretch=NO, anchor='center')
        tv.heading(8, text="Samples")
        tv.column(8, minwidth=100, width=100, stretch=NO, anchor='center')
        show()

    def time(self):
        self.now= datetime.today().strftime('%I:%M:%S %p')
        self.time_t.config(text=self.now)
        self.time_t.after(1000, self.time)

    def date(self):
        self.now= datetime.today().strftime('%d-%m-%Y')
        self.date_d.config(text=self.now)


    def reset_values(self):
        name.set("")
        fname.set("")
        dob.set(datetime.today().strftime('%d-%m-%Y'))
        jd.set(datetime.today().strftime('%d-%m-%Y'))
        email.set("")
        mob.set("")
        delsamples()


    def numbercheck(self, inp):
        if (len(inp)<11):
            if inp.isdigit():
                return True
            elif inp is "":
                return True
            else:
                return False
        else:
            messagebox.showerror("Error","Invalid Mobile Number")
            return False




def delsamples():
    location = "samples/"
    for i in range(1, 22):
        file = f"{empid}.{i}.jpeg"
        path = os.path.join(location, file)
        os.remove(path)
    sambtn.configure(bg="Red")



if __name__ == '__main__':
    global cur
    conn = db.connect('Attendance.db')
    cur = conn.cursor()
    fileopen()
    root=Tk()
    objd=Adduser(root, empname)
    root.mainloop()
