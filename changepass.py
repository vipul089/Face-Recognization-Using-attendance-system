from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3 as db
from datetime import datetime
import os

def quit():
    MsgBox = messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'question')
    if MsgBox == 'yes':
        root.destroy()





def update():
    conn = db.connect('Attendance.db')
    cur = conn.cursor()
    run = cur.execute("Select pass from Login WHERE id= ?", (eid,))
    results = cur.fetchone()
    if (opass.get()=="" or passw.get()=="" or passwr.get()==""):
        messagebox.showerror("Error", "All Fields Are Required")
    elif(passw.get() != passwr.get() and opass.get()!=results[0] ):
        messagebox.showerror("Error", "You Have Entered Wrong Password or Mismatched")
    else:
        update_query = ("UPDATE Login SET pass = ? WHERE id= ?")
        runn = cur.execute(update_query, (passw.get(), eid))
        if runn:
            msg=messagebox.showinfo("Successfull", "Password Changed Successfully")
            if msg=='ok':
                if (etype=="Admin"):
                    os.system('py admin_dashboard.py')
                    root.destroy()
                else:
                    os.system('py user_dashboard.py')
                    root.destroy()
        else:
            messagebox.showerror("Oops", "Something Went Wrong")

    cur.close()
    conn.commit()
    conn.close()

def back():
    if etype=="User":
        os.system('py user_dashboard.py')
    else:
        os.system('py admin_dashboard.py')
    root.destroy()

class ChangePass:
    def __init__(self, root, passw, passwr, empname, opass ):
        self.root = root
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        self.root.title("Attendance Management System")
        self.root.bind("<Escape>", exit)




        # images
        self.background=ImageTk.PhotoImage(file="images/background.jpg")
        self.man_icon=ImageTk.PhotoImage(file="images/man.jpg")
        self.pass_icon = ImageTk.PhotoImage(file="images/pass.jpg")
        self.top_icon=ImageTk.PhotoImage(file="images/fronttopleft.jpg")
        bb = Image.open("images/back.png")
        self.back_image = ImageTk.PhotoImage(bb)

        # Background Image
        bg_lb = Label(self.root, image=self.background).pack()

        # Top frame
        self.top_frame=Frame(self.root, bg="#112034")
        self.top_frame.place(x=0, y=0, relwidth=1)

        # Top Left Image
        self.lb1=Label(self.top_frame, image=self.top_icon, bd=0)
        self.lb1.grid(row=0, column=0)

        # Top Title
        self.title=Label(self.top_frame, text="FACE RECOGNIZATION ATTENDANCE SYSTEM",bg="#112034", fg="#87a81b", height="3", font='Algerian 37 bold underline', width=36, padx=20)
        self.title.grid(row=0, column=1)

        # Dashboard Bar
        self.dashboard = Frame(self.root, bg='#93AAAA', )
        self.dashboard.place(x=0, y=171, relwidth=1, width=100)


        self.back = Button(self.dashboard, image=self.back_image, bg='#93AAAA', bd=0, activebackground="#78A1C5",
                           command=back)
        self.back.grid(row=0, column=0, )

        self.dashlb = Label(self.dashboard, text="Welcome :", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
        self.dashlb.grid(row=0, column=1, )

        self.name = Label(self.dashboard, text = empname, compound=LEFT, fg='#472074', font='Arial 18 bold',
                          bg='#93AAAA', )
        self.name.grid(row=0, column=2, )

        self.act = Label(self.dashboard, text="Change Password", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
        self.act.grid(row=0, column=3, padx=160, )

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

        # Login Frame
        self.Login_frame=LabelFrame(self.root, bg="#112034", )
        self.Login_frame.place(x=460,y=230,)

        # Main Icon
        self.Logo_lb=Label(self.Login_frame, image=self.man_icon,compound=TOP, text="Change Password:-", bg="#112034", font=("Arial", 22, "bold", "underline"), fg="White").grid(row=0, columnspan=3, pady=20)

        # Username
        self.user_lb = Label(self.Login_frame, text="Old Password", image=self.pass_icon, compound=LEFT,
                             font=("Arial", 20, "bold"), bg="#112034", fg="white",)
        self.user_lb.grid(row=1, column=0, padx=20, sticky=W)

        # Username Semicolon
        self.usersem = Label(self.Login_frame, text=":", bg="#112034", fg="white", font=("Arial", 20, "bold"), )
        self.usersem.grid(row=1, column=1, )

        # Username Entry

        self.user_txt = Entry(self.Login_frame, width=14, font=("Arial", 14, "bold"), textvariable= opass, show="*" )
        self.user_txt.grid(row=1, column=2, padx=20, sticky=W)

        # Username
        self.user_lb=Label(self.Login_frame, text="Password", image=self.pass_icon, compound=LEFT, font=("Arial", 20, "bold"), bg="#112034", fg="white")
        self.user_lb.grid(row=2, column=0,  padx=20, sticky=W)

        # Username Semicolon
        self.usersem = Label(self.Login_frame, text=":",bg="#112034", fg="white", font=("Arial", 20, "bold"),)
        self.usersem.grid(row=2, column=1,)

        # Username Entry
        self.user_txt=Entry(self.Login_frame, width=14, font=("Arial", 14, "bold"), textvariable=passw, show="*")
        self.user_txt.grid(row=2, column=2, padx=20, sticky=W)

        # Username
        self.user_lb = Label(self.Login_frame, text="Re-Enter", image=self.pass_icon, compound=LEFT,
                             font=("Arial", 20, "bold"), bg="#112034", fg="white")
        self.user_lb.grid(row=3, column=0, padx=20, sticky=W)

        # Username Semicolon
        self.usersem = Label(self.Login_frame, text=":", bg="#112034", fg="white", font=("Arial", 20, "bold"), )
        self.usersem.grid(row=3, column=1, )

        # Username Entry
        self.user_txt = Entry(self.Login_frame, width=14, font=("Arial", 14, "bold"), textvariable=passwr, show="*")
        self.user_txt.grid(row=3, column=2, padx=20, sticky=W)


        # Submit Button
        self.success_btn = Button(self.Login_frame, text="Update", width=12, height=1, justify=CENTER, command=update)
        self.success_btn.grid(row=4, columnspan=3,  pady=20, sticky=W, padx=80)

        # Quit Button
        self.resend_btn = Button(self.Login_frame, text="Quit", width=12, height=1, command=quit, )
        self.resend_btn.grid(row=4, columnspan=3, sticky=E, pady=20, padx=80)

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
    passw = StringVar()
    passwr = StringVar()
    opass = StringVar()
    objo = ChangePass(root, passw, passwr, ename, opass)
    root.mainloop()
