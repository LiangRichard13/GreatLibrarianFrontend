# @Author: LiXiang
# @Time: 2023/12/22 12:22
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import db, APIKey, ProjectAPIKey


def getAK(AKid):
    x = APIKey.query.filter(APIKey.apiKey_id == AKid).first()
    return {'id': x.apiKey_id, 'name': x.apiKey_name, 'value': x.apiKey_value, 'auth': x.apiKey_auth}


# 项目下配置APIKey
class ProjectAK(Resource):
    # 项目下添加APIKey
    def post(self):
        try:
            db.session.add(ProjectAPIKey(Pid=request.json['pid'], AKid=request.json['AKid']))  # 加入数据库
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 项目下删除APIKey
    def delete(self):
        try:
            db.session.delete(ProjectAPIKey.query.filter(ProjectAPIKey.Project_APIKey_id == request.json['PAKid'])[0])
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 项目下修改APIKey
    def put(self):
        PAK = ProjectAPIKey.query.filter(ProjectAPIKey.Project_APIKey_id == request.json['PAKid']).first()
        PAK.AKid = request.json['AKid']
        try:
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 查询项目下的AK【参数:Pid,返回:该项目下的所有ak列表】
    def get(self):
        AK = [getAK(x.AKid) for x in ProjectAPIKey.query.filter(ProjectAPIKey.Pid == request.json['Pid'])]
        return jsonify({'data': AK, 'success': True})
