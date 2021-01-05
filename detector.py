import cv2
import numpy as np
import sqlite3
import os
import smtplib
import time
from pygame import mixer
import datetime
from tkinter import messagebox

reco = cv2.face.LBPHFaceRecognizer_create();
reco.read("backend/trainningData.yml")
face_detect = cv2.CascadeClassifier('backend/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

def send_email(msg, reciever):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("sajalbansal2010@gmail.com", "2010sajal")
        server.sendmail("sajalbansal2010@gmail.com", reciever, msg)
        server.quit()
    except:
        messagebox.showerror("Error","Email failed to send")


def play():
    insert()
    mixer.init()
    mixer.music.load('backend/thankyou.mp3')
    mixer.music.play()

def insert():
    conn = sqlite3.connect("Attendance.db")
    cur = conn.cursor()
    run = cur.execute("Select Count() FROM attdata where id = ? and date = ? and dept_time is NULL", (profile[0], dt,))
    a = run.fetchone()[0]
    if (a==0):
        insertinattdata = ("Insert into attdata (id, date, arr_time) values (?,?,?)")
        runn = cur.execute(insertinattdata, (profile[0], dt, ct))
        message = 'Subject: {}\n\n{}'.format("No Reply",f" Hi {profile[1]} Your have Arrived at {ct} on {dt} . ")
        send_email(message, profile[5])

    else:
        runn1 = cur.execute("Select * from attdata where id = ? and date = ? and dept_time is NULL", (profile[0], dt,))
        at=runn1.fetchone()[2]
        if(runn1 is not None):
            format = '%I:%M:%S %p'
            wh=str(datetime.datetime.strptime(ct, format) - datetime.datetime.strptime(at, format))
            insertdt = ("Update attdata set dept_time = ?, work_time = ? where id = ? and date= ? and dept_time is NULL")
            ex=cur.execute(insertdt, (ct, wh, profile[0], dt,))
            message = 'Subject: {}\n\n{}'.format("No Reply",f" Hi {profile[1]} Your have Departure at {ct} . Your Working Time is {wh} . on {dt} . ")
            send_email(message, profile[5])
    conn.commit()
    conn.close()


def getProfile(id):
    conn=sqlite3.connect("Attendance.db")
    cursor=conn.execute("SELECT * FROM Detail where sno = ?",(str(id),))
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
fontface = cv2.FONT_HERSHEY_COMPLEX_SMALL
fontscale = 1.2
fontcolor = (0, 0, 255)

while True:
    global dt
    ret, img =cam.read();
    gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, 1.3,5)
    dt = str(datetime.date.today().strftime('%d-%m-%Y'))
    tt = time.localtime()
    ct = time.strftime("%I:%M:%S %p", tt)
    cv2.putText(img, 'Date: ' + dt + ' | Time: ' + ct, (40, 30), fontface, fontscale, fontcolor)
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)
        id,conf=reco.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)
        if(profile!=None):
            cv2.putText(img, 'EmpID : ' + str(profile[0]), (x, y + h + 30), fontface, fontscale, fontcolor)
            cv2.putText(img, 'Name : '+str(profile[1]), (x, y + h+60), fontface, fontscale, fontcolor)
    cv2.imshow("Face", img)
    if(cv2.waitKey(1) & 0xFF ==ord('+')):
        play()
        break
cam.release()
cv2.destroyAllWindows()
