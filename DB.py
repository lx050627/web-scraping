from pymongo import MongoClient
import pymongo

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
