#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
from prettytable import PrettyTable
import Crawler as C
from PIL import Image, ImageTk
import Mail
import Pdf
import os
import threading
import DrawGraph as Draw


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.c=C.Crawler()#crawler module

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
        self.beginButton = Button(self, text='OK!', command=self.execute)#register the function
        self.beginButton.pack()

        image = Image.open("logo.jpg")#open the logn file
        w, h = image.size## get the size of image
        image.thumbnail((w // 2, h // 2))  # reduce the size to the half
        photo = ImageTk.PhotoImage(image)
        self.logo = Label(image=photo)
        self.logo.image = photo  # keep a reference!
        self.logo.pack(side="right")


    def execute(self):#execute crawler program
        name = self.usernameInput.get()#get the username and password from input box
        pw = self.pwInput.get()
        if(name!="" and pw!=""):
            info = self.c.execute(name, pw)
            #print("INFo"+info)
            if(info!={}):
                self.profile = info['profile']
                self.courses = info['courses']
                self.grades = info['grades']
                self.papers = info['papers']
                self.htmlresult = self.show()  # display the results in GUI and return the html from

    def service(self):
        service = Tk()
        service.title("Service")
        elabel = Label(service, text="Destination Email Address")
        elabel.grid(row=0)#grid layout manager
        self.einput = Entry(service)
        self.einput.grid(row=0,column=1)
        ebutton = Button(service, text='Send', command=self.sendmail)
        ebutton.grid(row=0,column=2)
        elabel = Label(service, text="Convert to PDF File")
        elabel.grid(row=1, column=0)
        ebutton = Button(service, text='Ok', command=self.topdf)
        ebutton.grid(row=1, column=1)
        elabel = Label(service, text="Grades Summary")
        elabel.grid(row=2, column=0)
        ebutton = Button(service, text='Pie Chart', command=self.pie)
        ebutton.grid(row=2, column=1)
        ebutton = Button(service, text='Bar Chart', command=self.bar)
        ebutton.grid(row=2, column=2)

    def aggregate(self):
        numbers = [0, 0, 0, 0, 0, 0]
        for course in self.grades:  # summarize the number of each grade
            if (course['grade'] == 'A'):
                numbers[0] += 1
            elif (course['grade'] == 'B'):
                numbers[1] += 1
            elif (course['grade'] == 'C'):
                numbers[2] += 1
            elif (course['grade'] == 'D'):
                numbers[3] += 1
            elif (course['grade'] == 'E'):
                numbers[4] += 1
            elif (course['grade'] == 'F'):
                numbers[5] += 1
            else:
                pass
        return numbers

    def pie(self):
        data=self.aggregate()
        Draw.draw_pie(data)

    def bar(self):
        data = self.aggregate()
        Draw.draw_bar(data)

    def topdf(self):#when click on "Convert to PDF" button
        Pdf.htmltopdf(self.htmlresult, self.profile.name)

    def sendmail(self):#when click on "Send" button
        des=self.einput.get()# get the receiver's email from input box
        t = threading.Thread(target=Mail.SendMail, args=(self.profile.name, des, self.htmlresult,self.papers), name="Mail")
        t.setDaemon(True)
        t.start()

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
        htmlcontent+="<div align='center'><h2>Basic Personal Information</h2><br>"+html+'</div><br><br>'

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
        htmlcontent += "<div align='center'><h2>Registered Courses</h2><br>"+ html + '</div><br><br>'

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
        htmlcontent += "<div align='center'><h2>Course Grades</h2><br>" + html + '</div><br><br>'

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
        names="<div class='paper'>"+names+"</div>"
        htmlcontent += "<div align='center'><h2>Scanned Papers</h2><br>" + names + '</div><br>'

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
        return x.get_string(),x.get_html_string()#return the string and html from at the same time

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
        #return x.get_string(),x.get_html_string(attributes={"style":"color: red; font-size: 20px"})#return the string and html from at the same time
        return x.get_string(),x.get_html_string()
app = Application()
    # set the title of window
app.master.title('MIUN Helper')
    # main loop
app.mainloop()