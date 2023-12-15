# @Author: LiXiang
# @Time: 2023/12/8 16:02
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *


class ProjectOperation(Resource):
    # 增加
    def post(self):
        project = Project(
            # project_id=creat_md5_id()[:6],
            project_name=request.json['name'],
            project_info=request.json['info'],
            project_LLM='-'.join(request.json['LLM']),  # 获取到的是APIKey_id值  列表转化为字符串
            project_DataSet=request.json['DSid'],
            userId=request.json['uid'])
        try:
            db.session.add(project)  # 加入数据库
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            print(e)
            return jsonify({'success': False})

    # 删除
    def delete(self):
        project = Project.query.filter(Project.project_id == request.json['id'])[0]
        try:
            db.session.delete(project)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False})

    # 查询
    def get(self):
        data = []
        for x in Project.query.filter(Project.userId == request.args['uid']):
            LLM = []
            for y in x.project_LLM.split('-'):
                aK = APIKey.query.filter(APIKey.apiKey_id == y)[0]
                LLM.append({'id': y, 'name': aK.apiKey_name, 'value': aK.apiKey_value, 'auth': aK.apiKey_auth})
            data.append({'id': x.project_id, 'name': x.project_name, 'info': x.project_info, 'LLM': LLM})
        return jsonify({'data': data, 'success': True})
