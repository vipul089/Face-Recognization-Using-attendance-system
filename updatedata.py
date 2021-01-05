from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3 as db
from datetime import datetime
import os
from twilio.rest import Client
import random
import smtplib
import requests


# get request
# def sendPostRequest():
#     global ra
#     ra = random.randrange(1000, 9999)
#     req_params = {
#         'apikey':'TOHBPM4TJ3T7WAHS6JILW1LSAOH1P903',
#         'secret':'SOHLJTCYR0HUTURL',
#         'usetype':'stage',
#         'phone': mno,
#         'message':f"Your One Time Password For Updating Data is {ra} .",
#         'senderid':'8393089650'
#     }
#     return requests.post('https://www.sms4india.com/api/v1/sendCampaign', req_params)




def send_email():
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("sajalbansal2010@gmail.com", "2010sajal")
        message = 'Subject: {}\n\n{}'.format("No Reply", f" Hi {name} Your Data Updated Successfully.")
        server.sendmail("sajalbansal2010@gmail.com", mail_txt.get(), message)
        server.quit()
    except:
        messagebox.showerror("Error","Email failed to send")




def quit():
    MsgBox = messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'question')
    if MsgBox == 'yes':
        root.destroy()

def send_sms():
    global ra
    ra = random.randrange(1000, 9999)
    account_sid = "AC76e2425b471a6dbf7f34207d49908003"
    auth_token = "5355c0cf48e276a7f32b657afd684ad8"
    client = Client(account_sid, auth_token)
    sms=client.messages.create(
        from_="+12817243143",
        body= f"Your One Time Password For Updating Data is {ra} .",
        to="+91"+mno)



def genotp():
    if(mno == "" or mail ==""):
        messagebox.showerror("Error", "All Fields Are Mandatory")
    elif(len(user_mob.get())<10):
        messagebox.showerror("Error","Invalid Mobile Number")
    else:
        global otp
        otp=StringVar()
        success_btn.config(state="disabled")
        resend_btn.config(state="disabled")
        # response = sendPostRequest()
        send_sms()
        otp_lbf = LabelFrame(root, bg="#4D8BA0", fg="white",  bd=5 )
        otp_lbf.place(x=460, y=485)
        otp_lb = Label(otp_lbf, text="Enter Otp", font=("Arial", 20, "bold"),width=11, bg="#4D8BA0", fg="white", anchor=W)
        otp_lb.grid(row=0, column=0, padx=20,)

        otpsem = Label(otp_lbf, text=":", bg="#4D8BA0", fg="white", font=("Arial", 20, "bold"), )
        otpsem.grid(row=0, column=1,padx=5 )

        # Username Entry

        otp_ent = Entry(otp_lbf, width=17, font=("Arial", 13, "bold"), show="*" )
        otp_ent.config(textvariable=otp)
        otp_ent.grid(row=0, column=2, padx=18,)

        save_btn = Button(otp_lbf, text="Save", width=12, height=1, justify=CENTER, command=save)
        save_btn.grid(row=1, columnspan=3, pady=20, sticky=W, padx=80)

        # Quit Button
        quit_btn = Button(otp_lbf, text="Quit", width=12, height=1, command=quit, )
        quit_btn.grid(row=1, columnspan=3, sticky=E, pady=20, padx=80)



def save():

    if (otp.get() == ""):
        messagebox.showerror("Error", "Please Fill Otp")
    elif(otp.get() != str(ra)):
        messagebox.showerror("Error", "Please Enter Valid Otp")

    else:
        conn = db.connect('Attendance.db')
        cur = conn.cursor()
        up = ("Update Detail Set email = ? , mobno = ? WHERE id= ?")
        runn = cur.execute(up, (mail_txt.get(), user_mob.get(), eid,))
        if runn:
            send_email()
            msg = messagebox.showinfo("Successfull", "Data Updated Successfully")
            if msg == 'ok':
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

class Update:
    def __init__(self, root, name, mail, mno):
        root = root
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        root.title("Attendance Management System")
        root.bind("<Escape>", exit)


        # images
        self.background=ImageTk.PhotoImage(file="images/background.jpg")
        self.top_icon=ImageTk.PhotoImage(file="images/fronttopleft.jpg")
        bb = Image.open("images/back.png")
        self.back_image = ImageTk.PhotoImage(bb)

        # Background Image
        bg_lb = Label(root, image=self.background).pack()

        # Top frame
        self.top_frame=Frame(root, bg="#112034")
        self.top_frame.place(x=0, y=0, relwidth=1)

        # Top Left Image
        self.lb1=Label(self.top_frame, image=self.top_icon, bd=0)
        self.lb1.grid(row=0, column=0)

        # Top Title
        self.title=Label(self.top_frame, text="FACE RECOGNIZATION ATTENDANCE SYSTEM",bg="#112034", fg="#87a81b", height="3", font='Algerian 37 bold underline', width=36, padx=20)
        self.title.grid(row=0, column=1)

        # Dashboard Bar
        self.dashboard = Frame(root, bg='#93AAAA', )
        self.dashboard.place(x=0, y=171, relwidth=1, width=100)


        self.back = Button(self.dashboard, image=self.back_image, bg='#93AAAA', bd=0, activebackground="#78A1C5",
                           command=back)
        self.back.grid(row=0, column=0, )

        self.dashlb = Label(self.dashboard, text="Welcome :", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
        self.dashlb.grid(row=0, column=1, )

        self.name = Label(self.dashboard, text = name, compound=LEFT, fg='#472074', font='Arial 18 bold',
                          bg='#93AAAA', )
        self.name.grid(row=0, column=2, )

        self.act = Label(self.dashboard, text="Update Data", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
        self.act.grid(row=0, column=3, padx=200, )

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
        self.Login_frame=LabelFrame(root, bg="#4D8BA0", bd=5)
        self.Login_frame.place(x=460,y=260,)

        # Username
        self.user_lb = Label(self.Login_frame, text="Emp Id",
                             font=("Arial", 20, "bold"), bg="#4D8BA0", fg="white",)
        self.user_lb.grid(row=1, column=0, padx=20, sticky=W)

        # Username Semicolon
        self.usersem = Label(self.Login_frame, text=":", bg="#4D8BA0", fg="white", font=("Arial", 20, "bold"), )
        self.usersem.grid(row=1, column=1, )

        # Username Entry
        self.user_txt = Entry(self.Login_frame, width=14, font=("Arial", 14, "bold"), )
        self.user_txt.insert(0, eid)
        self.user_txt.config(state='disabled')
        self.user_txt.grid(row=1, column=2, padx=20, sticky=W)

        # Username
        self.user_lb=Label(self.Login_frame, text="Name", compound=LEFT, font=("Arial", 20, "bold"), bg="#4D8BA0", fg="white")
        self.user_lb.grid(row=2, column=0,  padx=20, sticky=W)

        # Username Semicolon
        self.usersem = Label(self.Login_frame, text=":",bg="#4D8BA0", fg="white", font=("Arial", 20, "bold"),)
        self.usersem.grid(row=2, column=1,)

        # Username Entry
        self.user_txt=Entry(self.Login_frame, width=14, font=("Arial", 14, "bold"),)
        self.user_txt.insert(0,name)
        self.user_txt.config(state='disabled')
        self.user_txt.grid(row=2, column=2, padx=20, sticky=W)

        # Username
        self.user_lb = Label(self.Login_frame, text="Email Address",
                             font=("Arial", 20, "bold"), bg="#4D8BA0", fg="white")
        self.user_lb.grid(row=3, column=0, padx=20, sticky=W)

        # Username Semicolon
        self.usersem = Label(self.Login_frame, text=":", bg="#4D8BA0", fg="white", font=("Arial", 20, "bold"), )
        self.usersem.grid(row=3, column=1, )

        global mail_txt
        # Username Entry
        mail_txt = Entry(self.Login_frame, width=14, font=("Arial", 14, "bold"),)
        mail_txt.insert(0, mail)
        mail_txt.grid(row=3, column=2, padx=20, sticky=W)

        # Username
        self.usermob_lb = Label(self.Login_frame, text="Mobile No.",
                             font=("Arial", 20, "bold"), bg="#4D8BA0", fg="white")
        self.usermob_lb.grid(row=4, column=0, padx=20, sticky=W)

        # Username Semicolon
        self.usermobsem = Label(self.Login_frame, text=":", bg="#4D8BA0", fg="white", font=("Arial", 20, "bold"), )
        self.usermobsem.grid(row=4, column=1, )

        global user_mob
        # Username Entry
        user_mob = Entry(self.Login_frame, width=14, font=("Arial", 14, "bold"))
        user_mob.insert(0, mno)
        user_mob.grid(row=4, column=2, padx=20, sticky=W)
        reg2 = user_mob.register(self.numbercheck)
        user_mob.config(validate="key", validatecommand=(reg2, '%P'))

        # Submit Button
        global success_btn, resend_btn
        success_btn = Button(self.Login_frame, text="Generate Otp", width=12, height=1, justify=CENTER, command=genotp)
        success_btn.grid(row=5, columnspan=3,  pady=20, sticky=W, padx=80)

        # Quit Button
        resend_btn = Button(self.Login_frame, text="Quit", width=12, height=1, command=quit, )
        resend_btn.grid(row=5, columnspan=3, sticky=E, pady=20, padx=80)


    def time(self):
        self.now = datetime.today().strftime('%I:%M:%S %p')
        self.time_t.config(text=self.now)
        self.time_t.after(1000, self.time)

    def date(self):
        self.now = datetime.today().strftime('%d-%m-%Y')
        self.date_d.config(text=self.now)

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


def fileopen():
    global eid, etype
    with open('tempfile.temp', "r") as f:
        data = f.readlines()
        eid = data[0].rstrip()
        etype = data[1].rstrip()
    return eid, etype

def fetch():
    global name, mail, mno
    conn = db.connect('Attendance.db')
    cur = conn.cursor()
    run = cur.execute("Select name, email, mobno from Detail WHERE id= ?", (eid,))
    results = cur.fetchone()
    name = results[0]
    mail = results[1]
    mno = results[2]
    return name, mail, mno

    cur.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    fileopen()
    fetch()
    root = Tk()
    objo = Update(root, name, mail, mno)
    root.mainloop()
