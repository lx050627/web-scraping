#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import os
import Student as S
import sys
from time import ctime
import threading
import DB as db
sys.setrecursionlimit(10000)


class Crawler(object):
    def execute(self,name,password):
        print("Start Time:%s" %(ctime()))

        self.info={}
        threads = []
        loginurl = "https://cas2.miun.se/cas/login?service=https%3A%2F%2Fportal.miun.se%" \
                   "2Fc%2Fportal%2Flogin%3Fp_l_id%3D1060514%26_miunRedirect%3Dhttps%253A%252F%252Fportal.miun.se%" \
                   "252Fgroup%252Fstudent"  # url of login page

        postdata = {'username': name, 'password': password}  # student's username and password to login

        self.s = requests.Session()  # get a session
        r = self.s.get(loginurl)  # use "GET" method to access login page

        soup = BeautifulSoup(r.text, 'lxml')  # use bs to generate html tree with the parser "lxml"
        lt = soup.find('input', attrs={'name': 'lt'})['value']  # get the value of "lt"

        postdata['lt'] = lt
        postdata['_eventId'] = "submit"

        r = self.s.post(loginurl, data=postdata)  # use "POST" method to aceess login page with configured post data
        #print(r.text)
        soup = BeautifulSoup(r.text, 'lxml')  # use bs to generate html tree with the parser "lxml"
        try:
            reurl = soup.find('form', attrs={'name': 'acsForm'})['action']  # get the url of redirection
            mainpage = self.s.post(reurl)  # use "POST"method to access redirection page and achieve successful login

            t = threading.Thread(target=self.GetInfo, name="ladokpage")
            threads.append(t)
            t.start()

            papers = []
            paperurl = "https://portal.miun.se/group/student/tentamensresultat"  # url of scanned paper
            paper = self.s.get(paperurl)
            paperpage = BeautifulSoup(paper.text, 'lxml')
            plinks = paperpage.find_all("a", class_="page-link")  # get all the links of pdf files

            for plink in plinks:
                filename = plink.get_text(strip=True) + ".pdf"  # create the name of file\
                place = os.path.abspath('.') + "/" + filename
                papers.append(place)
                t = threading.Thread(target=self.Download, args=(plink['href'], filename), name=filename)
                t.daemon=True
                t.start()

            self.info['papers'] = papers
            print('thread %s is running...%s' % (threading.current_thread().name, ctime()))

            for t in threads:
                t.join()

            print("Scanned Paper Information Completed")
            print("End Time:%s" % ctime())
        except TypeError as e:
            print(e)
            print("Invalid username or incorrect password")

        return self.info

    def Download(self, url, filename):
        print('thread %s is running...%s' % (threading.current_thread().name, ctime()))
        link =self.s.get(url)
        with open(filename, 'wb') as f:
            f.write(link.content)  # write binary content into local file
            print("%s download succeeds %s " % (threading.current_thread().name, ctime()))

    def GetInfo(self):

        print('thread %s is running...%s' % (threading.current_thread().name, ctime()))
        ladokurl = "https://portal.miun.se/group/student/mina-ladok-uppgifter"  # url of ladok page
        ladok = self.s.get(ladokurl)
        ladokpage = BeautifulSoup(ladok.text, 'lxml')
        personinfo = ladokpage.find_all("div", class_="ui-widget ui-widget-content ui-corner-all")[1]
        name = personinfo.h2.string
        info = personinfo.find_all(class_="adressInfo")  # deep down to get more data
        contact = list(info[0].find_all("div")[1].stripped_strings)  # convert generator to list
        phone, email = contact[2:4]  # slice of list
        phone = phone.split(":")[1].lstrip()  # remove whitespace in the left of string
        email = email.split(":")[1].lstrip()
        m = re.match(r'^([a-zA-Z\s]+?)\s([0-9a-zA-Z\-]+)$',
                     name)  # use regular expression to seperate name and personnumber
        name = m.group(1)
        id = m.group(2)
        info[1].h3.extract()  # extract h3 tag from the whole html tree
        address = info[1].get_text().lstrip()
        student = S.Student(name, id, phone, email, address)  # construct new Student instance
        self.info['profile'] = student
        print(self.info['profile'])
        print("Basic Information Completed")
        t = threading.Thread(target=student.InsertDB, name="student storage")
        t.setDaemon(True)
        t.start()

        registration = ladokpage.find("div", id="_TG02_WAR_LpwPortlets_tg02-tabs2").select_one(
            ".table-responsive")  # get html info about courses
        courses = []  # list for all registered courses
        for course in registration.thead.find_next_siblings("tr"):  # deep down
            info = list(course.stripped_strings)
            cinfo = {}  # dictionary for one course info
            cinfo['semester'] = info[0]
            cinfo['code'] = info[1]
            cinfo['title'] = info[2]
            cinfo['program'] = info[3]
            cinfo['startweek'] = info[4]
            cinfo['endweek'] = info[5]
            cinfo['credits'] = info[6]
            cinfo['registration type'] = info[7]
            courses.append(cinfo)  # add a course into the course list
        self.info['courses'] = courses
        print("Course Information Completed")
        t = threading.Thread(target=db.MySQLInsert, args=(courses,),name="courses storage")
        t.setDaemon(True)
        t.start()

        coursegrade = []  # list for grade of each registered course
        gradeinfo = ladokpage.find("div", id="_TG02_WAR_LpwPortlets_tg02-tabs1")  # get data about all grades
        for grade in gradeinfo.select(".parentBody > .hover"):  # get data about overall grade
            grade = list(grade.strings)  # obtain all the strings inside the tag
            cg = {}  # dic for overall grade of one course
            cg['course code'] = grade[2]
            cg['title'] = grade[5]
            cg['credits'] = grade[7]
            cg['grade'] = grade[10].lstrip()
            cg['date'] = grade[13]
            coursegrade.append(cg)  # add the overall grade of a course into list
        # print(coursegrade)

        index = 0  # index for coursegrade list, initially pointing to the first element(course) in the list
        for detailgrade in gradeinfo.select(".childBody"):  # get data about datailed grade
            onecourse = []
            for item in detailgrade.find_all("tr"):  # deal with one exam of one course
                info = list(item.strings)
                # print(info)
                detail = {}  # dic for one exam
                detail['exam code'], detail['title'], detail['credits'], detail['grade'], detail['mark'] = info[3], \
                                                                                                           info[5], \
                                                                                                           info[7], \
                                                                                                           info[10], \
                                                                                                           info[12]
                if (detail['mark'] == " "):  # if specific mark is not given
                    detail['date'] = info[13].lstrip()
                else:  # if specific mark is given
                    detail['date'] = info[14].lstrip()
                onecourse.append(detail)  # add one exam into one course
            # print(onecourse)
            coursegrade[index]['details'] = onecourse  # add info of all exams to the corresponding course as details
            index = index + 1  # point to the next course in the coursegrade list

        self.info['grades'] = coursegrade
        print("Grade Information Completed")
        print('thread %s finishes.%s' % (threading.current_thread().name, ctime()))
        t = threading.Thread(target=db.MongoInsert, args=(name,coursegrade), name="grades storage")
        t.setDaemon(True)
        t.start()









