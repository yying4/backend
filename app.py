#encoding：utf-8

from flask import Flask,render_template,request,url_for
import db_mongo
import json
import time
import crawler.bili_danmu as craw
#import jsonify
from concurrent.futures import ThreadPoolExecutor  #多线程
executor = ThreadPoolExecutor(2)
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

#@app.route是一个装饰器，作用是：做一个url和视图函数的映射，URL和函数绑定，前端/浏览器访问某个url，就会调用这个函数。
#创建主页路由
@app.route('/')
def index():
    return render_template('index.html')

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
        cid = str(time.strftime("%Y-%m-%d %H:%M:%S", ct))
        #print(cid)
        db_mongo.insert_websites(website, cid)  #存入数据库
        executor.submit(craw.bili_spyder, cid)  #craw.bili_spyder(cid)
        return "正在爬取中，请稍等。5分钟后请打开网页'{}'，输入本次的查询时间：'{}'查询".format('127.0.0.1:5000/output/',cid)


@app.route('/output/',methods=['GET','POST'])
def output():
    if request.method == 'GET':
        return render_template('output.html')
    else:
        cid = str(request.form.get('query_time'))
        result = db_mongo.output_danmu(cid)
        dic_danmu = db_mongo.trans_dm(result)
        dic_danmu=dic_danmu.to_dict('records')
        #re=pd.read_json("test.json", encoding="utf-8", orient='records')
        re = json.dumps(dic_danmu,ensure_ascii=False)
        return re#json.dumps


if __name__=='__main__':
    #启动一个应用服务器，来接受用户的的请求
    #app.run(port=5000,host='127.0.0.1',debug=True)  #debug在正式上线时要去掉
    app.run(port=5000, host='0.0.0.0')  # debug在正式上线时要去掉











