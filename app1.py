from flask import Flask
import pymongo
app = Flask(__name__)

from crawler.bili_danmu import main_func

myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb = myclient["app"]
print(mydb)
# mycol = mydb["表名"]
# for x in mycol.find():

@app.route('/')
def hello_world():
    return 'Hello, World!'