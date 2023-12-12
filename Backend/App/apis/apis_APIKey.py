# @Author: LiXiang
# @Time: 2023/11/15 20:22
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *
from App.utils.MD5_ID import *


class APIKeyAdd(Resource):
    def post(self):
        apiKey = APIKey(
            apiKey_id=creat_md5_id()[:8],
            apiKey_name=request.json['name'],
            apiKey_value=request.json['value'],
            apiKey_auth=request.json['auth'],
            userid=request.json['uid'])
        try:
            db.session.add(apiKey)  # 加入数据库
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            print(e)
            return jsonify({'success': False})


class APIKeyDelete(Resource):
    def delete(self):
        try:
            db.session.delete(APIKey.query.filter(APIKey.apiKey_id == request.json['id'])[0])
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False})


class APIKeySearch(Resource):
    def post(self):
        return jsonify({'data': [
            {'id': x.apiKey_id, 'name': x.apiKey_name, 'value': x.apiKey_value, 'auth': x.apiKey_auth}
            for x in APIKey.query.filter(APIKey.userid == request.json['uid'])], 'success': True})


class APIKeyUpdate(Resource):
    def post(self):
        pass
