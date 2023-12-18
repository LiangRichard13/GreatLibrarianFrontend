# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *
from App.utils.token import encode, decode
from App.utils.MD5_ID import creat_md5_id
import os


# 用户头像文件操作
class Icon(Resource):
    def get(self):
        return jsonify({'url': User.query.filter(User.user_id == request.json['uid'])[0].user_iconUrl})

    def post(self):
        user = User.query.filter(User.user_id == request.args['uid'])[0]
        file = request.files.get('iconFile')  # 获取到头像图片
        file_dir = os.path.join("App", "data", "icon")
        os.makedirs(file_dir, exist_ok=True)  # 创建多层文件夹
        fileName = 'icon_' + user.user_id + '.' + file.filename.split('.')[-1]  # 文件名为icon_+用户Id
        fileUrl = os.path.join(file_dir, fileName)
        user.user_iconUrl = fileUrl
        try:
            file.save(fileUrl)
            db.session.commit()
            return jsonify({'success': True, 'url': fileUrl})
        except OSError as oe:  # 文件处理异常
            return jsonify({'success': False, 'message': oe})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': e})


# 用户修改个人信息
class UpdateUser(Resource):
    def post(self):
        print("this is UpdateUser")
        user_id = request.json['id']
        user = User.query.filter(User.user_id == user_id)[0]  # 通过ID值查找user
        user.user_name = request.json['name']
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
        users = User.query.filter(User.user_id == request.json['id'])
        if list(users):
            user = users[0]
            data = {'name': user.user_name, 'tel': user.user_tel, 'email': user.user_email,
                    "iconUrl": user.user_iconUrl}
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


# 修改用户ip地址，用户登出
class LoginOut(Resource):
    def put(self):
        try:
            user = User.query.filter(User.user_id == request.args['uid'])[0]
            user.user_IP = None
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            print(e)
            return jsonify({'success': False, 'massage': e})


# 定义全局 用户列表字典集合【key:uid,value:用户状态（0:同一局域网,1:好友在线,-1:好友非在线）】
userIdDict = {}


# 获取同一局域网下的所有用户id
def getSameNetUsers(user_id, ip):
    '''
    :param user_id:
    :param ip:
    :return: userIdDict
    '''
    global userIdDict
    for user in User.query.filter(User.user_IP == ip):
        if user.user_id != user_id and user.user_id not in userIdDict:
            userIdDict[user.user_id] = 0


# 获取好友的用户id
def getFriends(user_id, ip):
    '''
    :param user_id:
    :param ip:
    :return: userIdDict
    '''
    global userIdDict
    for friend in FriendShip.query.filter(FriendShip.userid == user_id):
        user = User.query.filter(User.user_authToken == friend.friend_token)[0]
        userIdDict[user.user_id] = 1 if user.user_IP == ip else -1


# 获取用户列表
class GetUserList(Resource):
    def get(self):
        user_id = request.args['id']  # 获取当前用户id
        ip = request.remote_addr
        # 1、获取当前局域网下的所有用户id
        getSameNetUsers(user_id, ip)
        # 2、获取好友的用户id
        getFriends(user_id, ip)
        # 3、根据id进行数据封装
        data = [{'id': user.user_id, 'name': user.user_name, 'icon': user.user_iconUrl, 'ip': user.user_IP,
                 'state': userIdDict[user.user_id]} for user in User.query.filter(User.user_id.in_(userIdDict.keys()))]
        return jsonify({'data': data})
