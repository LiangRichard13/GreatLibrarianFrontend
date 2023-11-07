# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0

from .extensions import db


class User(db.Model):
    __tablename__ = 'tb_user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(30))
    user_tel = db.Column(db.String(30), unique=True)  # 唯一约束
    user_email = db.Column(db.String(30), unique=True)  # 唯一约束
    user_password = db.Column(db.String(30), nullable=False)  # 不为空值
    user_APIKey = db.Column(db.String(30))

    def __str__(self):
        if self.user_tel:
            return f'id:{self.user_id}\tname:{self.user_name}\ttel:{self.user_tel}'
        if self.user_email:
            return f'id:{self.user_id}\tname:{self.user_name}\temail:{self.user_email}'
