# @Author: LiXiang
# @Time: 2023/12/12 16:07
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *
from datetime import datetime
from App.utils.MD5_ID import *


def getAK(AKid):
    x = APIKey.query.filter(APIKey.apiKey_id == AKid)[0]
    return {'id': x.apiKey_id, 'name': x.apiKey_name, 'value': x.apiKey_value, 'auth': x.apiKey_auth}


def getDS(DSid):
    x = DataSet.query.filter(DataSet.DS_id == DSid)[0]
    return {'id': x.DS_id, 'name': x.DS_name, 'info': x.DS_info, 'url': x.DS_url}


class TestProjectCRUD(Resource):
    # 添加实验
    def post(self):
        tP = TestProject(tP_id=creat_md5_id()[:9], tP_name=request.json['name'], tP_time=datetime.now(),
                         AK1=request.json['AK1'], AK2=request.json['AK2'], DS=request.json['DS'])
        try:
            db.session.add(tP)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': e})

    # 删除实验
    def delete(self):
        try:
            db.session.delete(TestProject.query.filter(TestProject.tP_id == request.json['tPid'])[0])
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': e})

    # 查看实验
    def get(self):
        test = []
        for x in TestProject.query.filter(TestProject.tP_id == request.args['pid']):
            test.append({'id': x.tP_id, 'name': x.tP_name, 'time': x.tP_time,
                         'status': x.tP_status, 'progress': x.tP_progress,
                         'AK1': getAK(x.AK1), 'AK2': getAK(x.AK2), 'dataSet': getDS(x.DS)})

    # 实验修改
    def put(self):
        tP = TestProject.query.filter(TestProject.tP_id == request.json['tPid'])[0]
        tP.tP_name = request.json['name']
        tP.AK1, tP.AK2, tP.DS = request.json['AK1'], request.json['AK2'], request.json['DS']
        try:
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'massage': e})
