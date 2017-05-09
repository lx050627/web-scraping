from pymongo import MongoClient
import threading
from time import ctime
import pymysql

def MongoInsert(name,doc):
    mongo=MongoClient(host="localhost",port=27017)#establish a connection to specific host and port
    db=mongo["grade"]#get database
    name=name.lower().replace(' ','')#transform the name
    collection=db[name]#get collection
    print('thread %s is running...%s' % (threading.current_thread().name, ctime()))
    for item in doc:
        item['_id']=item['course code']
        collection.save(item)
        #if exists and same, do nothing;if exists but different,update;if not exist, insert
    print("Grades Insert Done")

def MySQLInsert(doc):
    db = pymysql.connect("localhost","root","1995627","miun")
    cursor = db.cursor()# get cursor

    sql = 'INSERT INTO courses (semester,code,title,program,startweek,endweek,credits,registration) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE '\
          'semester=%s,code=%s,title=%s,program=%s,startweek=%s,endweek=%s,credits=%s,registration=%s'


    for item in doc:
        cursor.execute(sql,(item["semester"],item['code'],item['title'],item['program'],item['startweek'],item['endweek'],item['credits'],item['registration type'],
                            item["semester"],item['code'],item['title'],item['program'],item['startweek'],item['endweek'],item['credits'],item['registration type'])
                       )

    db.commit()
    print('thread %s is running...%s' % (threading.current_thread().name, ctime()))
    db.close()
    print("Courses Insert Done")
