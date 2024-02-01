# @Author: LiXiang
# @Time: 2023/12/8 16:02
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import db, APIKey, DataSet, Project, ProjectAPIKey, ProjectDataSet


# 项目的CRUD配置
class ProjectCRUD(Resource):
    # 增加
    def post(self):
        project = Project(project_name=request.json['name'], project_info=request.json['info'],
                          userId=request.json['uid'])
        try:
            db.session.add(project)  # 加入数据库
            db.session.commit()
            return jsonify({'success': True, 'id': project.project_id})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False})

    # 删除
    def delete(self):
        project = Project.query.filter(Project.project_id == request.json['id']).first()
        try:
            db.session.delete(project)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 查询
    def get(self):
        data = []
        for project in Project.query.filter(Project.userId == request.args['uid']):
            # 查找该项目下的apikey
            project_apikey = []
            for item in ProjectAPIKey.query.filter(ProjectAPIKey.Pid == project.project_id):
                aK = APIKey.query.filter(APIKey.AK_id == item.AKid).first()
                project_apikey.append({'id': aK.AK_id, 'name': aK.AK_name})

            # 查找该项目下的dataset
            project_dataset = []
            for item in ProjectDataSet.query.filter(ProjectDataSet.Pid == project.project_id):
                dS = DataSet.query.filter(DataSet.DS_id == item.DSid).first()
                project_dataset.append({'id': dS.DS_id, 'name': dS.DS_name})

            data.append({'id': project.project_id, 'name': project.project_name, 'info': project.project_info,
                         'apiKey': project_apikey, 'dataSet': project_dataset})
        return jsonify({'data': data, 'success': True})
