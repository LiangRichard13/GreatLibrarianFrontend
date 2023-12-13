# @Author: LiXiang
# @Time: 2023/12/12 16:07
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *


class TestProject(Resource):
    def post(self):
        project = Project(
            # project_id=creat_md5_id()[:6],
            project_name=request.json['name'],
            project_info=request.json['info'],
            project_LLM='-'.join(request.json['LLM']),  # 获取到的是APIKey_id值  列表转化为字符串
            project_DataSet=request.json['dataSet'],
            userId=request.json['uid'])

