from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3 as db
import os
import requests
import random
from twilio.rest import Client


def quit():
    MsgBox = messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'question')
    if MsgBox == 'yes':
        root.destroy()
def send_sms(bodysms, tono):
    account_sid = "AC76e2425b471a6dbf7f34207d49908003"
    auth_token = "5355c0cf48e276a7f32b657afd684ad8"
    client = Client(account_sid, auth_token)
    sms=client.messages.create(
        from_="+12817243143",
        body=bodysms,
        to="+91"+tono)




def forget():
    global eid
    eid=empid.get()
    conn = db.connect('Attendance.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Detail WHERE id = (?)',(eid,))
    results=cur.fetchone()
    if (empid.get()==""):
        messagebox.showerror("Error", "Please Enter Empid")
    elif results is None:
        messagebox.showerror("Error", "Data Not Found")
    else:
        if results[0]==empid.get():
            mob=results[6]
            mobs=mob[6:10]
            msgbox = messagebox.askokcancel("Confirm",f"OTP Sent To XXXXXX{mobs}")
            if msgbox == True:
                ra = random.randrange(1000, 9999)
                with open(creds, 'w') as f:  # Creates a document using the variable we made at the top.
                    f.write(empid.get()+"\n")  # nameE is the variable we were storing the input to. Tkinter makes us use .get() to get the actual string.
                    f.write(str(ra))
                    f.close()
                # response = sendPostRequest(URL, 'TOHBPM4TJ3T7WAHS6JILW1LSAOH1P903', 'SOHLJTCYR0HUTURL', 'stage',
                #                        mob, '8393089650',  f"Your One Time Password is {ra} For Resetting Your Password.")
                response = send_sms(f"Your One Time Password is {ra} For Resetting Your Password.", mob)
                os.system("py forgetotp.py")
                root.destroy()
                return eid

    cur.close()
    conn.commit()
    conn.close()

class Forget:
    def __init__(self, root, empid):
        self.root = root
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        self.root.title("Attendance Management System")
        self.root.bind("<Escape>", exit)




        # images
        self.background=ImageTk.PhotoImage(file="images/background.jpg")
        self.man_icon=ImageTk.PhotoImage(file="images/man.jpg")
        self.user_icon=ImageTk.PhotoImage(file="images/user.jpg")
        self.top_icon=ImageTk.PhotoImage(file="images/fronttopleft.jpg")
        self.otp_icon=ImageTk.PhotoImage(file="images/otp.png")

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

        # Login Frame
        self.Login_frame=LabelFrame(self.root, bg="#112034", )
        self.Login_frame.place(x=460,y=200,)

        # Main Icon
        self.Logo_lb=Label(self.Login_frame, image=self.man_icon,compound=TOP, text="Forget Password:-", bg="#112034", font=("Arial", 22, "bold", "underline"), fg="White").grid(row=0, columnspan=3, pady=20)

        # Username
        self.user_lb=Label(self.Login_frame, text="Emp Id", image=self.user_icon, compound=LEFT, font=("Arial", 20, "bold"), bg="#112034", fg="white",)
        self.user_lb.grid(row=1, column=0,  padx=20, sticky=W)

        # Username Semicolon
        self.usersem = Label(self.Login_frame, text=":",bg="#112034", fg="white", font=("Arial", 20, "bold"),)
        self.usersem.grid(row=1, column=1,)

        # Username Entry
        self.user_txt=Entry(self.Login_frame, textvariable=empid, width=14, font=("Arial", 14, "bold"),)
        self.user_txt.grid(row=1, column=2, padx=20, sticky=W)

        # Login Button
        self.otp_btn = Button(self.Login_frame, text="Generate OTP", command=forget,  width=12, height=1,)
        self.otp_btn.grid(row=5, columnspan=3, sticky=W, pady=20, padx=80)


        # Quit Button
        self.login_btn = Button(self.Login_frame, text="QUIT", command=quit, width=12, height=1,)
        self.login_btn.grid(row=5, columnspan=3,  sticky=E,  pady=20, padx=80 )





if __name__ == "__main__":
    creds = 'tempfile.temp'
    root=Tk()
    # variables
    global empid
    empid = StringVar()
    objl=Forget(root, empid)
    root.mainloop()
