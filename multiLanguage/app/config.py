import os
# 调试模式
DEBUG = True

# session 
SECRET_KEY = os.urandom(24)
# 本地数据密码是rootroot, 119.23.218.150的是123456
#数据库连接配置
# HOSTNAME = "119.23.218.150"
HOSTNAME = "118.190.2.84"
PORT = '3306'
DATABASE='multiLanguage'
USERNAME='root'
PASSWORD='Linghong2017'
# PASSWORD='123456'
DB_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN =True