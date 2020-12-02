# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 11:05:46 2020
"""

import pandas as pd
import requests
import re  #正则表达式
#import csv
import time
import json
import db_mongo

'''
代码目前存在的问题：
1、不清内存的情况下，再次运行会警告
2、消耗时间较长，设置了time.sleep
3、代码语句有些冗余
'''

#1.url
#url='https://api.bilibili.com/x/v2/dm/history?type=1&oid=226204073&date=2020-11-24'
#url_bv='https://www.bilibili.com/video/BV1x54y1e7zf'
#get_date(url_bv)

#获取稿件上传日期
def get_date(url_bv):
    html_doc = get_html_text(url_bv)
    res = re.compile('<meta data-vue-meta="true" itemprop="uploadDate" content="(.*?)"><meta data-vue-meta="true" itemprop="datePublished"')
    update_time = re.findall(res,html_doc)
    update_date = update_time[0][0:10]
    return update_date


def get_oid(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bvid + '&jsonp=jsonp'
    res = requests.get(url).text
    time.sleep(1)
    json_dict = json.loads(res)
    return json_dict["data"][0]["cid"]


#2.模拟浏览器发送请求和接收响应
def single_crawler(url,date_str,bvid,danmu_info,cid):
    html_doc = get_html_text(url)
    send_info = parse(html_doc,bvid,cid)
    danmu_info = save_single_data(send_info,date_str,danmu_info)
    return danmu_info


def get_html_text(url):
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            "cookie":"buvid3=B730947B-B62F-41B1-8661-97AE0C9B36D1190974infoc; LIVE_BUVID=AUTO9115747358394634; CURRENT_FNVAL=80; blackside_state=1; rpdid=|()k)uJ~R~J0J'ulmm)klu~R; DedeUserID=96096179; DedeUserID__ckMd5=f54ca0f19cc1ce0d; SESSDATA=6ccf20a6%2C1615377275%2C01b13*91; bili_jct=6ffce1cc5f03715c738deaf7245295cf; bsource=search_baidu; _uuid=390F45C0-209A-A0EF-8DD2-8DB6DEA1968920839infoc; sid=660qd07c; PVID=2; bfe_id=1e33d9ad1cb29251013800c68af42315"
    }
    response = requests.get(url,headers=headers)  #用计算机语言代替点击网页这个动作
    time.sleep(1)
    #乱码问题
    html_doc = response.content.decode('utf-8')
    return html_doc
    

#3.解析网页内容  弹幕
def parse(html_doc,bvid,cid):
    #弹幕内容
    res = re.compile('<d.*?>(.*?)</d>')
    danmu = re.findall(res,html_doc)
    #弹幕其他信息
    result = re.compile('<d p="(.*?)">')
    send = re.findall(result,html_doc)
    send_info = field_transform(danmu,send,bvid,cid)
    return send_info


#4.保存数据
def save_single_data(send_info,date_str,danmu_info):
    for row in send_info:
        if row[3] == date_str:
            danmu_info.append(row)
        else:
            break
    return danmu_info

# def save_header_csv(header,path):
#     with open(path,'a',newline='',encoding='utf-8-sig') as f:
#         writer = csv.writer(f)
#         writer.writerow(header)
#
# def save_csv(send_info,path,date_str):
#     with open(path,'a',newline='',encoding='utf-8-sig') as f:
#         writer = csv.writer(f)
#         for row in send_info:
#             if row[2] == date_str:
#                 writer.writerow(row)
#             else:
#                 break


#字段整理
def field_transform(danmu,send,bvid,cid):
    send_info=[]
    if len(danmu)==len(send):
        for i in range(len(danmu)):
            bv = 'BV' + bvid
            sp = send[i].split(',')
            user_id = sp[6]
            send_time,send_date,send_month = date_transform(int(sp[4]))
            dm_time = time_transform(float(sp[0]))
            text = danmu[i]
            send_single = [cid,bv,dm_time,send_date,send_month,send_time,text,user_id]
            send_info.append(send_single)
        return send_info
    else:
        print('ERROR：弹幕匹配出错')


#发送时间、发送日、发送月份的格式转换
def date_transform(seconds):
    timeArray = time.localtime(seconds)#秒数
    send_time = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))
    send_date = str(time.strftime("%Y-%m-%d", timeArray))
    send_month = str(time.strftime("%Y-%m", timeArray))
    return send_time,send_date,send_month


# 弹幕对应的出现时间的格式转化
def time_transform(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    dm_time = str("%d:%02d:%02d" % (h, m, s))
    return dm_time


def main_func(web_bv,cid):
    #当前时间
    timeArray = time.localtime(time.time())
    current_time = time.strftime("%Y-%m-%d", timeArray)
    #bv列表
    result_bv = re.compile('https://www.bilibili.com/video/BV(\w*)')
    bvid_list = re.findall(result_bv,web_bv)
    danmu_info=[]
    #表头
    header = ['query_time','BV_id','dm_time','send_date','send_month','send_time','text','user_id']
    #header = ['查询时间','BV号','弹幕对应的出现时间','发送日','发送月份','发送时间','弹幕内容','发送人id']
    #save_header_csv(header,path)
    
    for bvid in bvid_list:
        oid = str(get_oid(bvid))
        url_bv = 'https://www.bilibili.com/video/BV' + str(bvid)
        update_date = get_date(url_bv)
        date_duration = pd.Series(pd.date_range(start = update_date,end = current_time))
        for date in date_duration:
            date_str = str(date)[:10]
            url = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid=' + oid + '&date=' + date_str
            danmu_info = single_crawler(url,date_str,bvid,danmu_info,cid)
    danmu_if=pd.DataFrame(danmu_info,columns=header)
    return danmu_if


def bili_spyder(cid):
    #连接数据库，取出网址，整合成长字符串，存储在web_bv
    web_bv = db_mongo.html_str(cid)
    #web_bv='https://www.bilibili.com/video/BV1ND4y1X7fh ,https://www.bilibili.com/video/BV1PT4y1c74Z?from=search&seid=2841731650331385722'
    danmu_info = main_func(web_bv,cid)
    mydb = db_mongo.connect_mongo().app
    mycol = mydb.danmu
    mycol.insert_many(json.loads(danmu_info.T.to_json()).values())  #爬取结果存进数据库中
    # mycol.insert_one({'test':1, "age":2})
    # print(danmu_info)
    mycol = mydb.danmu
    for x in mycol.find({'query_time':'2020-12-02 12:51:46'}):
        print(x)

#cid='2020-12-02 12:51:46'
#对应的窗口输入为：https://www.bilibili.com/video/BV13y4y1S7nJ,https://www.bilibili.com/video/BV1ry4y167ib,https://www.bilibili.com/video/BV1yz4y1o7uT
#bili_spyder(cid)


'''
url = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid=226204073&date=2020-11-24'

bvid=bvid_list[0]

https://www.bilibili.com/video/BV1x54y1e7zf
https://api.bilibili.com/x/v2/dm/history?type=1&oid=258722895&date=2020-11-24
https://api.bilibili.com/x/v2/dm/history?type=1&oid=226204073&date=2020-11-24
https://www.bilibili.com/video/BV1ND4y1X7fh
'''


