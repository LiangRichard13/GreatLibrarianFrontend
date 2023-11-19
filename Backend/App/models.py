# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0

from .extensions import db


class User(db.Model):
    __tablename__ = 'tb_user'
    user_id = db.Column(db.String(30), primary_key=True)  # 用户ID
    user_name = db.Column(db.String(30))
    user_tel = db.Column(db.String(30), unique=True)  # 唯一约束
    user_email = db.Column(db.String(30), unique=True)  # 唯一约束
    user_password = db.Column(db.String(30), nullable=False)  # 不为空值
    user_IP = db.Column(db.String(30))  # 用户IP
    user_iconUrl = db.Column(db.String(80))  # 用户头像Url

    apiKeys = db.relationship('APIKey', backref='user', lazy='dynamic')
    testProjects = db.relationship('TestProject', backref='user', lazy='dynamic')

    def __str__(self):
        if self.user_tel:
            return f'id:{self.user_id}\tname:{self.user_name}\ttel:{self.user_tel}'
        if self.user_email:
            return f'id:{self.user_id}\tname:{self.user_name}\temail:{self.user_email}'


class APIKey(db.Model):
    __tablename__ = 'tb_APIKey'
    apiKey_id = db.Column(db.String(30), primary_key=True)
    apiKey_name = db.Column(db.String(30))  # 模型名称
    apiKey_value = db.Column(db.String(30))  # APIKey值
    apiKey_auth = db.Column(db.String(30))  # 鉴权秘钥
    userid = db.Column(db.String(30), db.ForeignKey(User.user_id))  # 用户ID---外键


# 用户测试实验信息
class TestProject(db.Model):
    __tablename__ = 'tb_TestProject'
    testProject_id = db.Column(db.String(30), primary_key=True)  # 测试实验信息ID
    testProject_name = db.Column(db.String(30))  # 测试项目名称
    testProject_time = db.Column(db.DateTime)  # 测试时间
    testProject_caseNum = db.Column(db.Integer)  # 测试项目包含测试数据条目
    testProject_LLMName = db.Column(db.String(30))  # APIKey中的name字段
    userid = db.Column(db.String(30), db.ForeignKey(User.user_id))  # 用户ID---外键


'''class SharedFile(db.Model):
    __tablename__ = 'tb_sharedFile'
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(50))
    file_url = db.Column(db.String(80), nullable=False)  # 不为空值
    file_userId = db.Column(db.Integer, db.ForeignKey(User.id))  # 外键,关联到用户表的主键，实现⼀对多关系，'''
