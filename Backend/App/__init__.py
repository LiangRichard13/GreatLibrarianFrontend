# @Author: LiXiang
# @Time: 2023/11/2 14:56
# @version: 1.0
from flask import Flask, send_from_directory
from .extensions import init_extensions
# 导入url路由【重要！！！】
from .urls import *
from flask_cors import *


def create_app():
    app = Flask(__name__, static_folder='data')
    # 配置数据库
    db_uri = 'sqlite:///sqlite3.db'  # sqlite配置
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁止对象追踪修改
    # 初始化插件
    init_extensions(app=app)
    # 初始化CORS扩展并配置允许的来源
    # CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
    CORS(app, resources=r'/*', origins="http://localhost:8080", methods=['GET', 'POST', 'DELETE', 'PUT'])
    return app

# @app.route('/data/<path:filename>')
# def icon(filename):
#     return send_from_directory(app.static_folder, filename)
