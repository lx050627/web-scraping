#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from prettytable import PrettyTable

class Student(object):
    __slots__ = ('name', 'number','phone','email','addr')#restrict the attributes of Class "Student"

    def __init__(self, name, number,phone,email,addr):#construction function
        self.name = name
        self.number=number
        self.phone=phone
        self.email=email
        self.addr=addr

    def printInfo(self):#print the student's basic information in the form of table
        x = PrettyTable(
            ["Name", "Personnumber", "Phone Number", "Email", "Address"])#head of table
        x.align="c"
        x.padding_width = 1
        x.add_row([self.name,self.number,self.phone,self.email,self.addr])#content of each row
        print(x)
        return x.get_string(),x.get_html_string()