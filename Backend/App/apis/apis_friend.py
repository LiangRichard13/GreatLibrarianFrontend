# @Author: LiXiang
# @Time: 2023/12/11 15:40
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *
from datetime import datetime


class Friend(Resource):
    # 好友申请【接收参数：请求者uid，接收者fid】
    def post(self):
        friendship = FriendShip(
            userid=request.json['uid'],  # 获取当前用户id
            friend_token=User.query.filter(User.user_id == request.json['fid'])[0].user_authToken,  # 获取好友的id
            createTime=datetime.now())
        try:
            db.session.add(friendship)  # 加入数据库
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': e})

    # 好友申请审核【接收参数:接收者uid、同意/拒绝响应result(bool类型值)】
    def put(self):
        uid = request.json['uid']
        result = request.json['result']  # 获取好友接收者的返回结果
        friend_token = User.query.filter(User.user_id == uid)[0].user_authToken  # 获取接收者的token
        friendship = FriendShip.query.filter(FriendShip.friend_token == friend_token)[0]  # 根据authToken查询请求记录
        try:
            if result:  # 同意添加好友
                friendship.friend_state = 1
                friend_next = FriendShip(
                    userid=uid,  # 接收者id
                    friend_token=User.query.filter(User.user_id == friendship.userid)[0].user_authToken,  # 获取好友的id
                    friend_state=1,
                    createTime=datetime.now()
                )
                db.session.add(friend_next)
            else:  # 拒绝添加好友
                db.session.delete(friendship)
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'massage': e})

    def get(self):
        user = User.query.filter(User.user_id == request.args['uid'])[0]
        friendList = FriendShip.query.filter(FriendShip.friend_token == user.user_authToken and FriendShip.friend_state==0)
        return jsonify({'fid': [x.userid for x in friendList],'success':True})
