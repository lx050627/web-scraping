from pymongo import MongoClient
import pymongo

def MongoInsert(name,doc):
    mongo=MongoClient(host="localhost",port=27017)
    db=mongo["grade"]
    name=name.lower().replace(' ','')
    collection=db[name]
    for item in doc:
        item['_id']=item['course code']
        collection.save(item)
    print("Insert Done")
