# @Author: LiXiang
# @Time: 2023/11/2 14:56
# @version: 1.0
import os

from flask import Flask
from .extensions import init_extensions
# 导入url路由【重要！！！】
from .urls import *
from flask_cors import *
from sqlalchemy import event
from sqlalchemy.engine import Engine
from App.utils.log import setup_logging


def create_app():
    app = Flask(__name__, static_folder='data')
    setup_logging()
    # 配置数据库
    db_uri = 'sqlite:///sqlite3.db'  # sqlite配置
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁止对象追踪修改
    app.config['conda_env'] = 'GL'  # 选择conda环境
    # app.config['conda_env'] = os.environ.get('SELECTED_ENV')  # 选择conda环境【使用start.sh启动】
    # 初始化插件
    init_extensions(app=app)
    # 初始化CORS扩展并配置允许的来源
    CORS(app, resources={r"/*": {"origins": ["http://192.168.70.12:*"]}}, methods=['GET', 'POST', 'DELETE', 'PUT'])

    # 在这里添加事件监听，以在每次数据库连接时启用外键约束
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite:"):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return app
