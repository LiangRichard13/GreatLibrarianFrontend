# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *
from App.utils.token import encode, decode
from App.utils.MD5_ID import creat_md5_id


# 用户修改个人信息
class UpdateUser(Resource):
    def post(self):
        print("this is UpdateUser")
        user_id = request.json['id']
        user = User.query.filter(User.user_id == user_id)[0]  # 通过ID值查找user
        user.user_name = request.json['name']
        file = request.files.get('icon')  # 获取到头像图片
        fileUrl = './icon/icon_' + user_id + '.' + file.filename.split('.')[-1]  # 存储文件名为icon_+用户Id
        file.save(fileUrl)
        user.user_iconUrl = fileUrl
        try:
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'massage': e})


# 通过用户id获取信息
class FindById(Resource):
    def post(self):
        print("this is findById")
        users = User.query.filter(User.user_id == request.json['id'])
        if list(users):
            user = users[0]
            data = {'name': user.user_name, 'tel': user.user_tel, 'email': user.user_email, }
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': False, 'massage': 'not find'})


# 用户通过Token登录
class LoginToken(Resource):
    def post(self):
        print("this is login Token 后端post请求处理")
        return jsonify({'success': decode(request.json['token'])})
        '''result_decode = decode(request.json['token'])
        if not result_decode:
            return jsonify({'success': False})
        else:
            data = {'id': result_decode['data']['id'], 'username': result_decode['data']['username'], }
            return jsonify({'success': True})
            # return jsonify({'success': True, 'data': data})'''


# 用户注册
class Register(Resource):
    def post(self):
        user = User(user_id=creat_md5_id()[:15],
                    user_name=request.json['username'],
                    user_tel=request.json['tel'],
                    user_email=request.json['email'],
                    user_password=request.json['password'],
                    user_authToken=creat_md5_id()[:5])
        try:
            db.session.add(user)  # 加入数据库
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            if list(User.query.filter(User.user_tel == user.user_tel)):
                print(f'存在tel注册失败:{e}')
                return jsonify({'success': False, 'message': 'tel has existed'})
            elif list(User.query.filter(User.user_email == user.user_email)):
                print(f'存在email注册失败:{e}')
                return jsonify({'success': False, 'message': 'email has existed'})


# 用户登录
class Login(Resource):
    def post(self):
        global users
        login_type = request.json['type']  # 用户登录类型
        username = request.json['loginName']  # 用户登录输入【tel/email】
        password = request.json['password']  # 用户登录密码
        remember = request.json['remember']  # 用户免登录
        if login_type == 'tel':
            users = User.query.filter(User.user_tel == username)
        if login_type == 'email':
            users = User.query.filter(User.user_email == username)
        if not list(users):  # 用户不存在
            print('未找到用户信息')
            return jsonify({'success': False, 'data': None, 'message': 'invalid tel or email'})
        else:
            user = users[0]
            if password == user.user_password:
                user_id = user.user_id
                data = {'id': user_id}
                # print(f'需要token:{remember}')
                if remember:
                    data['loginToken'] = encode(user_id, 60)  # 免登录
                else:
                    data['loginToken'] = encode(user_id, 10)  # 无需免登录
                user.user_IP = request.remote_addr  # 获取本地ip地址
                try:
                    db.session.add(user)  # 加入数据库
                    db.session.commit()
                except Exception as e:  # 数据库插入操作异常处理
                    db.session.rollback()  # 回滚
                    db.session.flush()  # 刷新，清空缓存
                    print(e)
                return jsonify({'success': True, 'data': data})
            else:
                print('登录密码错误')
                return jsonify({'success': False, 'data': None, 'message': 'password is wrong'})


# 获取当前局域网下所有的用户信息
class GetSameNetUsers(Resource):
    def get(self):
        user_id = request.args['id']  # 获取当前用户id
        ip = request.remote_addr
        users = User.query.filter(User.user_IP == ip)
        print("同一局域网下的所有用户:")
        for user in users:
            if user.user_id != user_id:
                print(user)


class AddFriendShip(Resource):
    def get(self):
        user_id = request.args['id']  # 获取当前用户id
        friend_id = request.args['id']  # 获取好友的id
