
from pymongo.mongo_client import MongoClient

#


uri = "mongodb+srv://iriscciou:supermon@selfuse.wvpvqks.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["Selfuse"]
col = db["poll"]

dict = {"vote": "Red", "num": 1}
x = col.insert_one(dict)

dic_many = [
    {"vote": "Red", "num": 0}, 
    {"vote": "Blue", "num": 0},
    {"vote": "Yellow", "num": 0},
    {"vote": "Green", "num": 0},
    {"vote": "Purple", "num": 0},
    {"vote": "Orange", "num": 0},
    ]
x = col.insert_many(dic_many)



# aggregate
group = {
   "$group": {
         "_id": "$vote",
         "cnt": {"$sum": "$num"}
   }
}

pipeline = [group]
results = col.aggregate(pipeline)
result_list = list(results)
print(result_list)

# delete all
x = col.delete_many({"num": 1})
