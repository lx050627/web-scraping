from pymongo import MongoClient
import pymongo
import pymysql

def MongoInsert(name,doc):
    mongo=MongoClient(host="localhost",port=27017)#establish a connection to specific host and port
    db=mongo["grade"]#get database
    name=name.lower().replace(' ','')#transform the name
    collection=db[name]#get collection
    for item in doc:
        item['_id']=item['course code']
        collection.save(item)
        #if exists and same, do nothing;if exists but different,update;if not exist, insert
    print("Insert Done")

def MySQLInsert(doc):
    db = pymysql.connect("localhost","root","1995627","miun")
    cursor = db.cursor()# get cursor

    sql = 'INSERT INTO courses (semester,code,title,program,startweek,endweek,credits,registration) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'

    for item in doc:
        cursor.execute(sql,(item["semester"],item['code'],item['title'],item['program'],item['startweek'],item['endweek'],item['credits'],item['registration type']))

    db.commit()
    db.close()
    print("Courses Insert Done")
