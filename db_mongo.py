import pymongo

#线上连接
def connect_mongo():
    MONGO_USER = "swen"
    MONGO_PSW = "swen123456"
    MONGO_HOST = "47.101.35.73"
    MONGO_PORT = "27017"
    myclient = pymongo.MongoClient('mongodb://{0}:{1}@{2}:{3}'.format(MONGO_USER, MONGO_PSW, MONGO_HOST, MONGO_PORT))
    return myclient
    #mydb = myclient.app
    #mycol = mydb.danmu

#从websites表中将网址取出
def find_websites(cid):
    client = connect_mongo()  #连接数据库
    db = client.app  # 数据库名为app
    collections=db.websites  #表名websites，创建一下----
    result=collections.find({'cid':cid})  #获取所有数据
    client.close()  #关闭连接
    return result

#根据cid取出数据
def html_str(cid):
    webs=find_websites(cid)
    webs_str=''
    for web in webs:
        web_str=web['web']
        webs_str = webs_str + web_str +','
    print('从数据库中取出的字符串为',webs_str)
    return webs_str

#插入数据到websites表中
def insert_websites(website ,cid):
    client = connect_mongo()  #连接数据库
    db = client.app
    collections=db.websites
    web_input={'web':website ,'cid':cid}
    result=collections.insert_one(web_input)  #插入数据
    client.close()  #关闭连接
    return result

#insert_website('www.hah.com','234567654')


#本地
'''''''''
def connect_website(cid):
    client = pymongo.MongoClient(host='127.0.0.1:27017')  #连接本地数据库
    db = client.Bilibili_danmu  # 数据库名为Bilibili_danmu
    collections=db.website  #表名website
    result=collections.find({'cid':cid})  #获取所有数据
    client.close()  #关闭连接
    return result

#根据cid取出数据
def html_str(cid):
    webs=connect_website(cid)
    webs_str=''
    for web in webs:
        web_str=web['web']
        webs_str = webs_str + web_str +','
    print('从数据库中取出的字符串为',webs_str)
    return webs_str

#插入数据
def insert_website(website ,cid):
    client = pymongo.MongoClient(host='127.0.0.1:27017')  #连接本地数据库
    db = client.Bilibili_danmu
    collections=db.website
    web_input={'web':website ,'cid':cid}
    result=collections.insert_one(web_input)  #插入数据
    client.close()  #关闭连接
    return result

#insert_website('www.hah.com')
'''''''''



