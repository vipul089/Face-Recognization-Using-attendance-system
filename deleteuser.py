import tkinter.ttk as ttk
from tkinter import *
from PIL import ImageTk, Image
import os
from datetime import datetime
import sqlite3 as db
from tkinter import messagebox


def back():
    os.system('py manage.py')
    root.destroy()

def remove_all():
    x= tv.get_children()
    if (x != '()'):
        for child in x:
            tv.delete(child)


def delete():
    selected_item = tv.selection()[0]
    delete_detail = cur.execute("DELETE FROM Detail WHERE id= ?",(id_en.get(),))
    delete_login = cur.execute("DELETE FROM Login WHERE id= ?",(id_en.get(),))
    delsamples()
    tv.delete(selected_item)
    messagebox.showinfo("Confirm", "User Successfully Deleted")
    conn.commit()

def delsamples():
    location = "samples/"
    for i in range(1, 22):
        file = f"{id_en.get()}.{sno}.{i}.jpeg"
        path = os.path.join(location, file)
        os.remove(path)



def find():
    global sno
    remove_all()
    if (id_en.get()==""):
        messagebox.showerror("Error", "Please Enter Employee Id")
    else:
        tv.tag_configure('T', font=('Arial 11'))
        query = cur.execute("Select * From Detail where id =?",(id_en.get(),))
        total=query.fetchall()
        if(len(total)==0):
            messagebox.showerror("Error", "No Data Found")
        else:
            tv.insert('', 'end', values=total[0], tags='T')
            sno=total[0][8]
            debtn.config(state="active")


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

class Deleteuser:
    def __init__(self, root, ename):
        global id_en, tv, debtn
        id_en = StringVar()
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

        self.act = Label(self.dashboard, text="Delete User", fg='#472074', font='Arial 18 bold', bg='#93AAAA', )
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
        self.frame.place(x=450, y=240)

        self.namelb=Label(self.frame, text="Employee Id", font='Arial 16 bold', bg="#4D8BA0", fg="#FFFFFF")
        self.namelb.grid(row=0, column=0, pady=5, padx=10, sticky="W")

        sbmtbtn=Button(self.frame, text= "Search", font="Arial 12 bold", bg="#4D8BA0", fg="#FFFFFF", bd=2, width=6, command=find)
        sbmtbtn.grid(row=0, column=2, sticky=W, pady=5, padx=10)

        debtn = Button(self.frame, text="Delete",  font="Arial 12 bold", bg="#4D8BA0", fg="#FFFFFF", bd=2, width=6, command=delete)
        debtn.config(state="disabled")
        debtn.grid(row=0, column=3, sticky=W, pady=5, padx=10)




        self.name_en=Entry(self.frame, textvariable=id_en, width=14, font=("Arial", 12), )
        self.name_en.grid(row=0, column=1, pady=5, padx=10, sticky=W)




        style = ttk.Style()
        style.configure("Treeview", rowheight="30", width=100,)
        style.configure("Treeview.Heading", font=('Arial 14 bold'))
        tv = ttk.Treeview(self.root, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height="5")
        tv.place(x=235, y=320, )
        sb = ttk.Scrollbar(self.root, orient="vertical", command=tv.yview)
        sb.place(x=1145, y=321, height="175")
        hsb = ttk.Scrollbar(self.root, orient="horizontal", command=tv.xview)
        hsb.place(x=236, y=496, width="927")
        tv.configure(yscrollcommand=sb.set, xscrollcommand=hsb.set)
        tv.heading(1, text="Emp ID", )
        tv.column(1, minwidth=50, width=100, stretch=NO, anchor='center')
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





    def time(self):
        self.now= datetime.today().strftime('%I:%M:%S %p')
        self.time_t.config(text=self.now)
        self.time_t.after(1000, self.time)

    def date(self):
        self.now= datetime.today().strftime('%d-%m-%Y')
        self.date_d.config(text=self.now)



if __name__ == '__main__':
    global cur
    conn = db.connect('Attendance.db')
    cur = conn.cursor()
    fileopen()
    root=Tk()
    objd=Deleteuser(root, empname)
    root.mainloop()
