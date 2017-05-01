#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
from prettytable import PrettyTable
import Crawler as C
from PIL import Image, ImageTk
import Mail
import Pdf
import os

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.c=C.Crawler()

    def createWidgets(self):
        self.w = Label(self, text="Login in to your Student's Portal at Mid Sweden University")
        self.w.pack()
        self.lu = Label(self, text="Username:")
        self.lu.pack()
        self.usernameInput = Entry(self)
        self.usernameInput.pack()
        self.lp = Label(self, text="Password:")
        self.lp.pack()
        self.pwInput = Entry(self,show = '*')
        self.pwInput.pack()
        self.beginButton = Button(self, text='OK!', command=self.execute)
        self.beginButton.pack()

        image = Image.open("logo.jpg")#open the logn file
        w, h = image.size## get the size of image
        image.thumbnail((w // 2, h // 2))  # reduce the size to the half
        photo = ImageTk.PhotoImage(image)
        self.logo = Label(image=photo)
        self.logo.image = photo  # keep a reference!
        self.logo.pack(side="right")


    def execute(self):#execute crawler program
        name = self.usernameInput.get()
        pw = self.pwInput.get()
        info=self.c.execute(name,pw)
        self.profile=info['profile']
        self.courses=info['courses']
        self.grades=info['grades']
        self.papers = info['papers']
        self.htmlresult=self.show()

    def service(self):
        service = Tk()
        service.title("Service")
        elabel = Label(service, text="Destination Email Address")
        elabel.grid(row=0)
        self.einput = Entry(service)
        self.einput.grid(row=0,column=1)
        ebutton = Button(service, text='Send', command=self.sendmail)
        ebutton.grid(row=0,column=2)
        elabel = Label(service, text="Convert to PDF File")
        elabel.grid(row=1, column=0)
        ebutton = Button(service, text='Ok', command=self.topdf)
        ebutton.grid(row=1, column=1)

    def topdf(self):
        Pdf.htmltopdf(self.htmlresult, self.profile.name)

    def sendmail(self):
        des=self.einput.get()
        Mail.SendMail(self.profile.name, des, self.htmlresult,self.papers)

    def show(self):#display the result in another new window
        display = Tk()
        display.title("Result")

        emailButton = Button(display, text='Services', command=self.service)
        emailButton.pack(side=TOP,fill=Y)

        htmlcontent=""
        l1= Label(display, text="Basic Personal Information")
        l1.pack()
        S1 = Scrollbar(display)
        T1 = Text(display, height=5, width=150)
        S1.pack(side=RIGHT, fill=Y)
        T1.pack(fill=Y)
        S1.config(command=T1.yview)
        T1.config(yscrollcommand=S1.set)
        text,html=self.profile.printInfo()
        T1.insert(END, text)
        htmlcontent+="<h2 align='center'>Basic Personal Information</h2>"+'<br>'+html+'<br><br>'

        l2 = Label(display, text="Registered Courses")
        l2.pack()
        S2 = Scrollbar(display)
        T2 = Text(display, height=8, width=150)
        S2.pack(side=RIGHT, fill=Y)
        T2.pack(fill=Y)
        S2.config(command=T2.yview)
        T2.config(yscrollcommand=S2.set)
        text,html =self.printcourses(self.courses)
        T2.insert(END, text)
        htmlcontent += "<h2 align='center'>Registered Courses</h2>" + '<br>' + html + '<br><br>'

        l3 = Label(display, text="Course Grades")
        l3.pack()
        S3 = Scrollbar(display)
        T3 = Text(display, height=15, width=150)
        S3.pack(side=RIGHT, fill=Y)
        T3.pack(fill=Y)
        S3.config(command=T3.yview)
        T3.config(yscrollcommand=S3.set)
        text, html=self.printgrades(self.grades)
        T3.insert(END, text)
        htmlcontent += "<h2 align='center'>Course Grades</h2>" + '<br>' + html + '<br><br>'

        l4 = Label(display, text="Scanned Papers")
        l4.pack()
        S4 = Scrollbar(display)
        T4 = Text(display, height=2, width=150)
        S4.pack(side=RIGHT, fill=Y)
        T4.pack(fill=Y)
        S4.config(command=T4.yview)
        T4.config(yscrollcommand=S4.set)
        files=""
        names=""
        for item in self.papers:
            files+=item+'\n'
            names+=os.path.split(item)[1]+"<br>"
        T4.insert(END, files)
        htmlcontent += "<h2 align='center'>Scanned Papers</h2>" + '<br>' + names + '<br>'

        return htmlcontent

    def printcourses(self, courses):  # print all courses info in the form of table
        x = PrettyTable(["Semester", "Code", "Title", "Program", "Start Week", "End Week", "Credits",
                         "Registration Type"])  # head of table
        x.align = "c"
        x.padding_width = 1
        for course in courses:
            x.add_row([course['semester'], course['code'], course['title'], course['program'],
                       course['startweek'], course['endweek'], course['credits'],
                       course['registration type']])  # contents of one row
        print(x)
        return x.get_string(),x.get_html_string()

    def printgrades(self, grades):  # print all course grades in the form of table
        x = PrettyTable(["Course code", "Exam code", "Title", "Credits", "Grade", "Marks", "Date"])  # head of table
        x.align = "c"
        x.padding_width = 1
        s = "******"
        # print(len(grades))
        for grade in grades:
            x.add_row([grade['course code'], "", grade['title'], grade['credits'], grade['grade'], "", grade['date']])
            for item in grade['details']:
                x.add_row(
                    [" ", item['exam code'], item['title'], item['credits'], item['grade'], item['mark'], item['date']])
            x.add_row([2 * s, 2 * s, 10 * s, s, s, s, 2 * s])
        print(x.get_string())
        return x.get_string(),x.get_html_string()

app = Application()
    # set the title of window
app.master.title('MIUN Helper')
    # main loop
app.mainloop()