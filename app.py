#encoding：utf-8

from flask import Flask,render_template,request,url_for
#from flask_sqlalchemy import SQLAlchemy
#import config
import db_mongo
import json
import time
import crawler.tt_craw as craw  #bili_danmu
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED  #多线程
executor = ThreadPoolExecutor(2)


app = Flask(__name__)
#app.config.form_object(config)

#@app.route是一个装饰器，作用是：做一个url和视图函数的映射，URL和函数绑定，前端/浏览器访问某个url，就会调用这个函数。
#创建主页路由
@app.route('/')
def index():
    context = {'username': 'heywhale',
               'date':'2020-12-01'
               }  #便于管理参数
    #print (url_for('my_list'))  #返回的是函数对应的网址
    return render_template('index.html',**context)  #模板放在templates文件夹下

'''
login功能实现：将前端传过来的网址存进数据库，并开始爬取数据
api接口前缀：apiPrefix = '/api/v1/'
下面的语句，不用if、else，直接app.route(apiPrefix + '字符串',methods=['post']) api与前端连接传数据过来
craw.test_sec改成craw.bili_spyder
'''
#默认视图函数，只能采用get请求；如果想采用post请求，要写明
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        website = request.form.get('web')  #输入的网址
        #cid = str(uuid.uuid1())  #查询区分的id
        ct = time.localtime(time.time())
        global cid
        cid = str(time.strftime("%Y-%m-%d %H:%M:%S", ct))
        print(cid)
        db_mongo.insert_websites(website, cid)  #存入数据库
        executor.submit(craw.test_sec, 'hello')  #craw.bili_spyder(cid)
        return "正在爬取中，请稍等。5分钟后请跳转'{}'，根据本次的查询时间：'{}'查询".format('127.0.0.1/downloap',cid)



@app.route('/output')
def dm_output():
    result = db_mongo.output_danmu(cid)
    dic_danmu = db_mongo.trans_dm(result)
    return json.dumps(dic_danmu)


# @app.route(apiPrefix + 'getStaffList/<int:job>')
# def getStaffList(job):
#     array = DBUtil.getStaffList(job)  # [('1', '1', '1', '1', '1'), ('1', '1', '2', '3', '4'), ...] 二维数组
#     jsonStaffs = DBUtil.getStaffsFromData(array)
#     # print("jsonStaffs:", jsonStaffs)
#     return json.dumps(jsonStaffs)



if __name__=='__main__':
    #启动一个应用服务器，来接受用户的的请求
    app.run(port=8088,host='127.0.0.1',debug=True)  #debug在正式上线时要去掉











