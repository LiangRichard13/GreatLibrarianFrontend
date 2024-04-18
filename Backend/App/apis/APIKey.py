# @Author: LiXiang
# @Time: 2023/11/15 20:22
# @version: 1.0
import os

from flask import jsonify, request
from flask_restful import Resource

from App.models import db, APIKey
from App.utils.MD5_ID import *
from App.utils.backend_path import BackendPath


class APIKeyCRUD(Resource):
    # 添加
    def post(self):
        apiKey = APIKey(AK_id=creat_md5_id()[:8], AK_name=request.json['name'], AK_value=request.json['value'],
                        AK_intro=request.json['intro'], userid=request.json['uid'])
        try:
            db.session.add(apiKey)  # 加入数据库
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 删除
    def delete(self):
        try:
            AK = APIKey.query.filter(APIKey.AK_id == request.json['id']).first()
            try:  # 删除call函数的py文件
                os.remove(os.path.join(BackendPath(), 'App', 'data', 'call', AK.AK_id + '.py'))
            except FileNotFoundError:
                pass
            db.session.delete(AK)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 查询【参数:uid,返回:【uid下的所有apikey列表】
    def get(self):
        return jsonify({'data': [
            {'id': x.AK_id, 'name': x.AK_name, 'value': x.AK_value, 'intro': x.AK_intro}
            for x in APIKey.query.filter(APIKey.userid == request.args['uid'])], 'success': True})

    # call函数【添加、修改、查看】
    def put(self):
        if request.json['choose'] == '1':  # 添加、修改
            AKid, code = request.json['id'], request.json['code']
            file_dir = os.path.join(BackendPath(), 'App', 'data', 'call')
            os.makedirs(file_dir, exist_ok=True)  # 创建多层文件夹
            file = os.path.join(file_dir, AKid + '.py')
            with open(file, 'w') as f:
                f.write(code)  # 写入代码到文件
            try:
                compiled_code = compile(code, file, 'exec')  # 检查语法错误
                exec(compiled_code, {})  # 在一个空的局部和全局命名空间中执行编译后的代码
                return jsonify({'success': True})
            except Exception:
                os.remove(os.path.join(BackendPath(), 'App', 'data', 'call', AKid + '.py'))
                return jsonify({'success': False, 'message': '存在语法错误'})
        elif request.json['choose'] == '2':  # 查询
            try:
                with open(os.path.join(BackendPath(), 'App', 'data', 'call', request.json['id'] + '.py'), 'r') as file:
                    return jsonify({'success': True, 'code': file.read()})
            except FileNotFoundError:
                return jsonify({'success': False, 'message': '读取call函数失败'})
