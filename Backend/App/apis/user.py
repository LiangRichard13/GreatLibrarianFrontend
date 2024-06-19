# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0
import os

from flask import jsonify, request
from flask_restful import Resource

from App.models import db, User, FriendShip
from App.utils.MD5_ID import creat_md5_id
from App.utils.backend_path import BackendPath
from App.utils.my_token import encode, decode


# 用户头像文件操作
class Icon(Resource):
    def get(self):
        return jsonify({'url': User.query.filter(User.user_id == request.args['uid']).first().user_iconUrl})

    def post(self):
        user = User.query.filter(User.user_id == request.args['uid']).first()
        file = request.files.get('iconFile')  # 获取到头像图片
        file_dir = os.path.join(BackendPath(), "App", "data", "icon")
        os.makedirs(file_dir, exist_ok=True)  # 创建多层文件夹
        fileName = 'icon_' + user.user_id + '.' + file.filename.split('.')[-1]  # 文件名为icon_+用户Id
        fileUrl = os.path.join(file_dir, fileName)
        user.user_iconUrl = os.path.join("App", "data", "icon", fileName)
        try:
            for file_in_dir in os.listdir(file_dir):
                if file_in_dir.startswith('icon_' + user.user_id):
                    os.remove(os.path.join(file_dir, file_in_dir))  # 删除同名文件
                    break
            file.save(fileUrl)
            db.session.commit()
            return jsonify({'success': True, 'url': fileUrl})
        except OSError as oe:  # 文件处理异常
            return jsonify({'success': False, 'message': str(oe)})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})


class UserCRUD(Resource):
    # 修改操作
    def put(self):
        choose = request.json['choose']
        user = User.query.filter(User.user_id == request.json['id']).first()  # 通过ID值查找user
        if choose == '1':  # 用户修改个人信息
            user.user_name = request.json['name']
        elif choose == '2':  # 用户更新密码
            user.user_password = request.json['password']
        try:
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 通过用户id获取信息
    def get(self):
        u = User.query.filter(User.user_id == request.args['id']).first()
        if u:
            data = {'name': u.user_name, 'tel': u.user_tel, 'email': u.user_email, "iconUrl": u.user_iconUrl}
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': False, 'message': 'not find'})

    # 用户注册
    def post(self):
        user = User(user_id=creat_md5_id()[:15], user_name=request.json['username'], user_tel=request.json['tel'],
                    user_email=request.json['email'], user_password=request.json['password'],
                    user_authToken=creat_md5_id()[:5])
        try:
            db.session.add(user)  # 加入数据库
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            if list(User.query.filter(User.user_tel == user.user_tel)):
                return jsonify({'success': False, 'message': 'tel has existed'})
            elif list(User.query.filter(User.user_email == user.user_email)):
                return jsonify({'success': False, 'message': 'email has existed'})


class Login(Resource):
    # 用户登录
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
            return jsonify({'success': False, 'data': None, 'message': 'invalid tel or email'})
        else:
            user = users[0]
            if password == user.user_password:
                user_id = user.user_id
                data = {'id': user_id,
                        'loginToken': encode(user_id, 60 * 60 * (24 * 5 if remember else 2))}  # 免登录5天，否则2小时
                user.user_IP = request.remote_addr  # 获取本地ip地址
                try:
                    db.session.add(user)  # 加入数据库
                    db.session.commit()
                    return jsonify({'success': True, 'data': data})

                except Exception as e:  # 数据库插入操作异常处理
                    db.session.rollback()  # 回滚
                    db.session.flush()  # 刷新，清空缓存
                    return jsonify({'success': False, 'message': str(e)})
            else:
                return jsonify({'success': False, 'data': None, 'message': 'password is wrong'})

    # 用户通过Token登录
    def put(self):
        if decode(request.json['token'])[0]:
            try:
                user = User.query.filter(User.user_id == decode(request.json['token'])[1])[0]
                user.user_IP = request.remote_addr  # 获取本地ip地址
                db.session.commit()
                return jsonify({'success': True})
            except Exception as e:  # 数据库插入操作异常处理
                db.session.rollback()  # 回滚
                db.session.flush()  # 刷新，清空缓存
                return jsonify({'success': False, 'message': str(e)})
        else:
            return jsonify({'success': False, 'loginExpired': True})

    # 修改用户ip地址，用户登出
    def get(self):
        try:
            user = User.query.filter(User.user_id == request.args['uid']).first()
            user.user_IP = None
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})


# 定义全局 用户列表字典集合【key:value=uid：value
#                    value:用户状态（0:同一局域网,1:好友在线,2:好友未添加(请求添加者),3：待确认添加好友(好友接收者)
#                       负数：表示不在线    eg：-1:好友不在线, -2:未添加的好友不在线, -3：待确认好友不在线）】
userIdDict = {}


# 获取同一局域网下的所有用户id【参数：user_id:用户id,ip:用户ip地址】
def getSameNetUsers(user_id, ip):
    global userIdDict
    for user in User.query.filter(User.user_IP == ip):
        if user.user_id != user_id and user.user_id not in userIdDict:
            userIdDict[user.user_id] = 0


# 获取好友的用户id【参数：user_id:用户id,ip:用户ip地址】
def getFriends(user_id, ip):
    global userIdDict
    # 通过uid找authtoken对应的用户
    for friend in FriendShip.query.filter(FriendShip.userid == user_id):
        user = User.query.filter(User.user_authToken == friend.friend_token).first()
        if friend.friend_state == 1:  # 已添加好友
            userIdDict[user.user_id] = 1 if user.user_IP == ip else -1
        elif friend.friend_state == 0:  # 待确认添加的好友
            userIdDict[user.user_id] = 2 if user.user_IP == ip else -2

    # 通过authtoken找uid对应的用户
    auth_token_user = User.query.filter(User.user_id == user_id).first()
    for friend in FriendShip.query.filter(FriendShip.friend_token == auth_token_user.user_authToken):
        user = User.query.filter(User.user_id == friend.userid).first()
        if friend.friend_state == 1:  # 已添加好友
            userIdDict[user.user_id] = 1 if user.user_IP == ip else -1
        elif friend.friend_state == 0:  # 用户自己需要确认的好友
            userIdDict[user.user_id] = 3 if user.user_IP == ip else -3


# 获取用户列表
class GetUserList(Resource):
    def get(self):
        global userIdDict
        user_id = request.args['id']  # 获取当前用户id
        ip = request.remote_addr
        # 1、获取当前局域网下的所有用户id
        getSameNetUsers(user_id, ip)
        # 2、获取好友的用户id
        getFriends(user_id, ip)
        # 3、根据userIdDict进行数据封装
        data = [{'id': user.user_id, 'name': user.user_name, 'icon': user.user_iconUrl, 'ip': user.user_IP,
                 'state': userIdDict[user.user_id]} for user in User.query.filter(User.user_id.in_(userIdDict.keys()))]
        userIdDict.clear()
        return jsonify({'data': data, 'success': True})
