#encoding：utf-8

import pymongo
import pandas as pd
import json
#线上连接
def connect_mongo():
    MONGO_USER = "hey"  #"swen"
    MONGO_PSW = "233333"  #"swen123456"
    MONGO_HOST = "127.0.0.1"  #"47.101.35.73"
    MONGO_PORT = "27017"
    myclient = pymongo.MongoClient('mongodb://{0}:{1}@{2}:{3}'.format(MONGO_USER, MONGO_PSW, MONGO_HOST, MONGO_PORT))
    return myclient
    #mydb = myclient.app
    #mycol = mydb.danmu

#1-1、根据cid从websites表中将网址取出
def find_websites(cid):
    client = connect_mongo()  #连接数据库
    db = client.app  # 数据库名为app
    collections=db.websites  #表名websites，创建一下----
    result=collections.find({'cid':cid})  #获取所有数据
    client.close()  #关闭连接
    return result

#1-2、如果有多条web，将他们合并取出，然后被bili_danmu调用爬取
def html_str(cid):
    webs=find_websites(cid)
    webs_str=''
    for web in webs:
        web_str=web['web']
        webs_str = webs_str + web_str +','
    print('从数据库中取出的字符串为',webs_str)
    return webs_str

#app：插入数据到websites表中
def insert_websites(website ,cid):
    client = connect_mongo()  #连接数据库
    db = client.app
    collections=db.websites
    web_input={'web':website ,'cid':cid}
    result=collections.insert_one(web_input)  #插入数据
    client.close()  #关闭连接
    return result

#insert_website('www.hah.com','234567654')

#app：2-1根据cid从danmu表中取出相应数据
def output_danmu(cid):
    client = connect_mongo()  #连接数据库
    db = client.app  # 数据库名为app
    collections=db.danmu  #表名danmu
    result=collections.find({'query_time':cid})  #获取所有数据
    client.close()  #关闭连接
    return result

#2-2-1 数据转换json
def trans_dm(result):
    header = ['query_time', 'BV_id', 'dm_time', 'send_date', 'send_month', 'send_time', 'text', 'user_id']
    row_df = pd.DataFrame(columns=header)
    for row in result:
        del row['_id']
        row_df = row_df.append(row, ignore_index=True)
    dic_danmu = row_df.to_dict('records')
    re = json.dumps(dic_danmu, ensure_ascii=False)
    return re

#2-2-2 数据转换
def trans_dm2(result):
    #header = ['query_time', 'BV_id', 'dm_time', 'send_date', 'send_month', 'send_time', 'text', 'user_id']
    #row_df = pd.DataFrame(columns=header)
    row_df = {}
    i=0
    for row in result:
        i+=1
        del row['_id']
        row_df[i] = row
        #row_df = row_df.append(row, ignore_index=True)
        #print(row_df)
    #df_json = row_df.to_json(orient="records", force_ascii=False)
    #print(df_json.dtype)
    return row_df


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



