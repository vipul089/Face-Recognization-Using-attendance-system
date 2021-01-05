from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3 as db
import time
import os


class Login_System:
    def login(self):
        conn = db.connect('Attendance.db')
        cur = conn.cursor()
        find_user=("SELECT * FROM Login WHERE  id = ? AND pass = ? AND type = ?")
        cur.execute(find_user, (self.uname.get(),self.passw.get(),self.optionvalue.get()))
        results=cur.fetchone()
        if (self.uname.get()=="" or self.passw.get()=="" or self.optionvalue.get()=="Choose"):
            messagebox.showerror("Error", "All Fields Are Required")

        elif results is None:
            messagebox.showerror("Error", "Data Not Found")

        else:
            find_detail_query=cur.execute("Select name from Detail where id= ?",(self.uname.get(),))
            find_detail_result=find_detail_query.fetchone()
            creds = 'tempfile.temp'
            with open(creds, 'w') as f:
                f.write(results[0] + "\n")
                f.write(self.optionvalue.get() + "\n")
                f.close()
            if results[0]==self.uname.get() and results[1]==self.passw.get() and results[2] == "Admin":
                messagebox.showinfo("Successfull", f"Welcome {find_detail_result[0]}")
                name = results[1]
                time.sleep(0.1)
                os.system('python admin_dashboard.py')
                self.root.destroy()

            elif results[0] == self.uname.get() and results[1] == self.passw.get() and results[2] == "User":
                messagebox.showinfo("Successfull", f"Welcome {find_detail_result[0]}")
                name = results[1]
                time.sleep(0.1)
                os.system('python user_dashboard.py')
                self.root.destroy()
            else:
                messagebox.showinfo("Error", "Something Went Wrong ")
        cur.close()
        conn.commit()
        conn.close()


    def quit(self):
        MsgBox = messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'question')
        if MsgBox == 'yes':
            self.root.destroy()

    def forget(self):
        os.system('python forget.py')
        self.root.destroy()

    def __init__(self, root):
        global name
        self.root = root
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        self.root.title("Attendance Management System")
        self.root.bind("<Escape>", exit)

        # variables
        self.uname=StringVar()
        self.passw=StringVar()
        self.optionvalue=StringVar()


        # images
        self.background=ImageTk.PhotoImage(file="images/background.jpg")
        self.man_icon=ImageTk.PhotoImage(file="images/man.jpg")
        self.user_icon=ImageTk.PhotoImage(file="images/user.jpg")
        self.pass_icon=ImageTk.PhotoImage(file="images/pass.jpg")
        self.top_icon=ImageTk.PhotoImage(file="images/fronttopleft.jpg")

        self.admin_icon=ImageTk.PhotoImage(file="images/admin.jpg")

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
        self.Logo_lb=Label(self.Login_frame, image=self.man_icon,compound=TOP, text="Login :-", bg="#112034", font=("Arial", 22, "bold", "underline"), fg="White").grid(row=0, columnspan=3, pady=20)

        # Username
        self.user_lb=Label(self.Login_frame, text="Username", image=self.user_icon, compound=LEFT, font=("Arial", 20, "bold"), bg="#112034", fg="white",)
        self.user_lb.grid(row=1, column=0,  padx=20, sticky=W)

        # Username Semicolon
        self.usersem = Label(self.Login_frame, text=":",bg="#112034", fg="white", font=("Arial", 20, "bold"),)
        self.usersem.grid(row=1, column=1,)

        # Password
        self.pwd_lb = Label(self.Login_frame, text="Password", image=self.pass_icon, compound=LEFT, font=("Arial", 20, "bold"), bg="#112034", fg="white", )
        self.pwd_lb.grid(row=2, column=0, padx=20, sticky=W)

        # Password Semicolon
        self.pwdsem = Label(self.Login_frame, text=":", bg="#112034", fg="white",font=("Arial", 20, "bold"),)
        self.pwdsem.grid(row=2, column=1,)

        # Type
        self.type_lb = Label(self.Login_frame, text="User Type", image=self.admin_icon, compound=LEFT, font=("Arial", 20, "bold"), bg="#112034", fg="white", )
        self.type_lb.grid(row=3, column=0, padx=20, sticky=W)

        # Type Semicolon
        self.type_sem = Label(self.Login_frame, text=":", bg="#112034", fg="white", font=("Arial", 20, "bold"), )
        self.type_sem.grid(row=3, column=1, )


        # Username Entry
        self.user_txt=Entry(self.Login_frame,  textvariable=self.uname, width=14, font=("Arial", 14, "bold"),)
        self.user_txt.grid(row=1, column=2, padx=20, sticky=W)

        # Password Entry
        self.pwd_txt = Entry(self.Login_frame, width=14, show="*", textvariable=self.passw, font=("Arial", 14, "bold"),)
        self.pwd_txt.grid(row=2, column=2, padx=20, sticky=W)

        # Type Entry
        optionvalue=["Admin", "User"]
        self.optionvalue.set("Choose")
        self.type_txt = OptionMenu(self.Login_frame, self.optionvalue, *optionvalue )
        self.type_txt.config(fg="White",font=("Arial", 18, "bold"), bg="#112034", highlightthickness=0)
        self.type_txt["menu"].config(fg="White",font=("Arial", 18, "bold"), bg="#112034" ,)
        self.type_txt.grid(row=3, column=2, padx=20, sticky=W)

        # Forget Password
        self.fg_btn = Button(self.Login_frame, text="Forgot Password", bd=0, fg="White", font=("Arial", 14, "bold"), activebackground="#112034", activeforeground="darkblue", bg="#112034", command= self.forget)
        self.fg_btn.grid(row=4, columnspan=3, sticky=E, padx=12)


        # Login Button
        self.login_btn = Button(self.Login_frame, text="LOGIN", command=self.login,  width=12, height=1,)
        self.login_btn.grid(row=5,  pady=20, sticky=E)


        # Quit Button
        self.login_btn = Button(self.Login_frame, text="QUIT", command=self.quit, width=12, height=1,)
        self.login_btn.grid(row=5, column=2, sticky=W, pady=20, )


if __name__ == '__main__':
    if(os.path.exists("tempfile.temp")):
        os.remove('tempfile.temp')
    root=Tk()
    objl=Login_System(root)
    # print(name)
    root.mainloop()
