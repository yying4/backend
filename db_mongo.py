import pymongo

def connect_website():
    client = pymongo.MongoClient(host='127.0.0.1:27017')  #连接本地数据库
    db = client.Bilibili_danmu  # 数据库名为Bilibili_danmu
    collections=db.website  #表名website
    result=collections.find()  #获取所有数据
    client.close()  #关闭连接
    return result

# webs=connect_website()
# webs_str=''
# for web in webs:
#     web_str=web['web']
#     webs_str = webs_str + web_str +','
#
# print(webs_str)

#
def insert_website(website):
    client = pymongo.MongoClient(host='127.0.0.1:27017')  #连接本地数据库
    db = client.Bilibili_danmu
    collections=db.website
    web_input={'web':website}
    result=collections.insert_one(web_input)  #插入数据
    client.close()  #关闭连接
    return result

#insert_website('www.hah.com')


