# B站弹幕爬取
## 项目背景
从搭建的网站中输入B站标准网页，即可爬取视频相应弹幕。

## 环境依赖
Flask              1.1.2
Flask-Cors         3.0.9

## 部署步骤
1 打开pycharm终端
2 输入 
* set FLASK_APP=app.py
* flask run

## 目录结构描述
Readme.md                   //介绍文档
app.py                      //应用
templates
    index.html              //首页
    login.html              //输入网址
    output.html             //根据查询时间输出结果
crawler
    bili_danmu.py           //爬取代码
    tt_craw.py              //测试
db_mongo.py                 //数据库连接与存取
venv                        //虚拟环境
tttt.py                     //测试文档

## V1.0.0 版本内容
app.py是基于flask框架建立的，会将网页中输入的网址存入数据库中，待爬取过程结束后，再从数据库中取出结果并呈现
bili_danmu.py是爬取弹幕的具体代码
