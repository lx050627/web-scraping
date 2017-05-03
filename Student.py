#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from prettytable import PrettyTable
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


# 创建对象的基类:
Base=declarative_base()

class Student(Base):
    #__slots__ = ('name', 'number','phone','email','addr')#restrict the attributes of Class "Student"
    __tablename__ = 'student'#name of table

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
        # 初始化数据库连接:
        engine = create_engine('mysql+pymysql://root:1995627@localhost:3306/miun')

        Base.metadata.create_all(engine)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        # 创建session对象:
        session = DBSession()
        # 添加到session:
        session.merge(self)
        # 提交即保存到数据库:
        session.commit()
        # 关闭session:
        session.close()
        print("Store student in DB finished")

    def printInfo(self):#print the student's basic information in the form of table
        x = PrettyTable(
            ["Name", "Personnumber", "Phone Number", "Email", "Address"])#head of table
        x.align="c"
        x.padding_width = 1
        x.add_row([self.name,self.number,self.phone,self.email,self.addr])#content of each row
        print(x)
        return x.get_string(),x.get_html_string()