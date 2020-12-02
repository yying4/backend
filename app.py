#encoding：utf-8

from flask import Flask,render_template,request,url_for
#from flask_sqlalchemy import SQLAlchemy
#import config
import db_mongo
import uuid
import time
import crawler.tt_craw as craw  #bili_danmu
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED  #多线程
executor = ThreadPoolExecutor(2)


app = Flask(__name__)
#app.config.form_object(config)

#@app.route是一个装饰器，作用是：做一个url和视图函数的映射
#创建主页路由
@app.route('/')
def index():
    context = {'username': 'heywhale',
               'date':'2020-12-01'
               }  #便于管理参数
    #print (url_for('my_list'))  #返回的是函数对应的网址
    return render_template('index.html',**context)  #模板放在templates文件夹下


#默认视图函数，只能采用get请求；如果想采用post请求，要写明
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        website = request.form.get('web')  #输入的网址
        #cid = str(uuid.uuid1())  #查询区分的id
        ct = time.localtime(time.time())
        cid = str(time.strftime("%Y-%m-%d %H:%M:%S", ct))
        print(cid)
        db_mongo.insert_websites(website, cid)  #存入数据库
        executor.submit(craw.test_sec, 'hello')  #craw.bili_spyder(cid)
        return "正在爬取中，请稍等。5分钟后请跳转'{}'，根据本次的查询时间：'{}'查询".format('127.0.0.1/downloap',cid)

        # with ThreadPoolExecutor(max_workers=3) as t:
        #     obj1 = t.submit(craw.first_out, 1)
        #     obj2 = t.submit(craw.test_sec, cid)
        #     all_task = [obj1, obj2]
        #     wait(all_task, return_when=FIRST_COMPLETED)
        #     print('finish')

        #craw.main_func(cid)
        #print ('website:',website)


if __name__=='__main__':
    #启动一个应用服务器，来接受用户的的请求
    app.run(port=8088,host='127.0.0.1',debug=True)  #debug在正式上线时要去掉











