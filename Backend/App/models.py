# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0

from .extensions import db


# 用户信息表
class User(db.Model):
    __tablename__ = 'tb_user'
    user_id = db.Column(db.String(30), primary_key=True)  # 用户ID
    user_name = db.Column(db.String(30))
    user_tel = db.Column(db.String(30), unique=True)  # 唯一约束
    user_email = db.Column(db.String(30), unique=True)  # 唯一约束
    user_password = db.Column(db.String(30), nullable=False)  # 不为空值
    user_IP = db.Column(db.String(30))  # 用户IP
    user_iconUrl = db.Column(db.String(80))  # 用户头像Url
    user_authToken = db.Column(db.String(30))  # 用户密钥

    apiKeys = db.relationship('APIKey', backref='user', lazy='dynamic')

    def __str__(self):
        if self.user_tel:
            return f'id:{self.user_id}\tname:{self.user_name}\ttel:{self.user_tel}'
        if self.user_email:
            return f'id:{self.user_id}\tname:{self.user_name}\temail:{self.user_email}'


# 用户好友关系表
class FriendShip(db.Model):
    __tablename__ = 'tb_friendship'
    friendship_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 好友关系id值，自增
    userid = db.Column(db.String(30), db.ForeignKey(User.user_id), nullable=False)  # 用户ID---外键
    friendship_token = db.Column(db.String(30), nullable=False)  # 好友的token密钥
    friendship_createTime = db.Column(db.DateTime, nullable=False)  # 好友创建的时间


# APIKey信息表
class APIKey(db.Model):
    __tablename__ = 'tb_APIKey'
    apiKey_id = db.Column(db.String(30), primary_key=True)
    apiKey_name = db.Column(db.String(30))  # 模型名称
    apiKey_value = db.Column(db.String(30))  # APIKey值
    apiKey_auth = db.Column(db.String(30))  # 鉴权秘钥
    userid = db.Column(db.String(30), db.ForeignKey(User.user_id))  # 用户ID---外键


# 项目数据表
class Project(db.Model):
    __tablename__ = 'tb_Project'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 项目id值，自增
    project_name = db.Column(db.String(80))  # 项目名称
    project_info = db.Column(db.String(200))  # 项目描述
    project_LLM = db.Column(db.String(200))  # 项目内可用的LLM
    project_DataSet = db.Column(db.String(200))  # 数据集
    userId = db.Column(db.String(30), db.ForeignKey(User.user_id))  # 用户ID---外键


# 用户测试实验信息
class TestProject(db.Model):
    __tablename__ = 'tb_TestProject'
    testProject_id = db.Column(db.String(30), primary_key=True)  # 测试实验信息ID
    testProject_time = db.Column(db.DateTime)  # 测试时间
    testProject_LLMs = db.Column(db.String(100))  # APIKey中的name字段【指定大模型】
    testProject_dataSet = db.Column(db.String(100))  # 实验所用的数据集路径
    projectId = db.Column(db.Integer, db.ForeignKey(Project.project_id))  # 项目ID---外键
