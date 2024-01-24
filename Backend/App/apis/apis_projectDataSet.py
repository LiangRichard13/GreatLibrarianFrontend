# @Author: LiXiang
# @Time: 2023/12/22 12:25
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *


def getDS(DSid):
    x = DataSet.query.filter(DataSet.DS_id == DSid)[0]
    return {'id': x.DS_id, 'name': x.DS_name, 'info': x.DS_info, 'url': x.DS_url}


# 项目下配置DataSet
class ProjectDS(Resource):
    # 项目下添加DataSet
    def post(self):
        try:
            db.session.add(ProjectDataSet(Pid=request.json['pid'], DSid=request.json['DSid']))  # 加入数据库
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False,'message': str(e)})

    # 项目下删除DataSet
    def delete(self):
        PDS = ProjectDataSet.query.filter(ProjectDataSet.Project_DataSet_id == request.json['PDSid'])[0]
        try:
            db.session.delete(PDS)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 项目下修改DataSet
    def put(self):
        PDS = ProjectDataSet.query.filter(ProjectDataSet.Project_DataSet_id == request.json['PDSid'])[0]
        PDS.DSid = request.json['DSid']
        try:
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 查询项目下的DataSet【参数:DSid,返回:该项目下的所有DS列表】
    def get(self):
        DS = [getDS(x.DSid) for x in ProjectDataSet.query.filter(ProjectDataSet.Pid == request.json['DSid'])]
        return jsonify({'data': DS, 'success': True})
