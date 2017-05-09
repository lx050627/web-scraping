#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from prettytable import PrettyTable
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String
import threading
from time import ctime


# create the base class of obejct
Base=declarative_base()

class Student(Base):
    __tablename__ = 'student'#name of table

    #define table structure
    name=Column(String(20))
    number=Column(String(20),primary_key=True)
    phone=Column(String(20))
    email=Column(String(30))
    addr =Column(String(100))


    def __init__(self, name, number,phone,email,addr):#construction function
        self.name = name
        self.number=number
        self.phone=phone
        self.email=email
        self.addr=addr

    def InsertDB(self):
        print('thread %s is running...%s' % (threading.current_thread().name, ctime()))
        # initilize the connection to db
        engine = create_engine('mysql+pymysql://root:1995627@localhost:3306/miun')
        # create the table if it does not exist
        Base.metadata.create_all(engine)
        # create DBSession class
        DBSession = sessionmaker(bind=engine)
        # create a session
        session = DBSession()
        # add/update Student instance in the db
        session.merge(self)
        # submit it to db
        session.commit()
        # close session
        session.close()
        print("Student Insert Done")

    def printInfo(self):#print the student's basic information in the form of table
        x = PrettyTable(
            ["Name", "Personnumber", "Phone Number", "Email", "Address"])#head of table
        x.align="c"
        x.padding_width = 1
        x.add_row([self.name,self.number,self.phone,self.email,self.addr])#content of each row
        print(x)
        return x.get_string(),x.get_html_string()#return the string and html from at the same time