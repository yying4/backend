#encoding：utf-8

# mongodb+://username:password@host:post/database

dialect='mysql'
driver='mysqldb'
username='root'
password='root'
host='127.0.0.1'
port='2206'
database='db_danmu'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(dialect,driver,username,password,host,port,database)


