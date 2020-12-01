#encoding：utf-8

from flask import Flask,render_template,request,url_for
#from flask_sqlalchemy import SQLAlchemy
#import config
import db_mongo

app = Flask(__name__)
#app.config.form_object(config)
#db=SQLAlchemy(app)



#@app.route是一个装饰器，作用是：做一个url和视图函数的映射
#创建主页路由
@app.route('/')
def index():
    context = {'username': 'heywhale',
               'date':'2020-12-01'
               }  #便于管理参数
    #print (url_for('my_list'))  #返回的是函数对应的网址
    return render_template('index.html',**context)  #模板放在templates文件夹下

#url传参数
@app.route('/article/<id>')
def article(id):
    return u'您请求的参数是：%s'% id

#url反转
@app.route('/list/')
def my_list():
    return 'list'

#默认视图函数，只能采用get请求
#如果你想采用post请求，那么要写明
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    else:
        website=request.form.get('web')
        db_mongo.insert_website(website)
        print ('website:',website)
        return "请稍等……"


if __name__=='__main__':
    #启动一个应用服务器，来接受用户的的请求
    app.run(port=8088,host='127.0.0.1',debug=True)  #debug在正式上线时要去掉






#创建注册页面路由
#@app.route('/register',methods=['GET','POST'])
#def register():
#    if request.method == 'GET':
 #       return render_template('login.html')
  #  else:
   #     uname =request.form['username']
    #    email=request.form['email']
     #   uurl=request.form['url']
      #  upwd=request.form['password']
       # savetosql(uname,email,uurl,upwd)
        #return return render_template('login.html')










