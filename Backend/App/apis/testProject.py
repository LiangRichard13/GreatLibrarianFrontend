# @Author: LiXiang
# @Time: 2023/12/12 16:07
# @version: 1.0
import os
from flask import jsonify, request
from flask_restful import Resource
from App.models import db, APIKey, DataSet, TestProject
from datetime import datetime
from App.utils.MD5_ID import *


def getAK(AKid):
    x = APIKey.query.filter(APIKey.AK_id == AKid).first()
    return {'id': x.AK_id, 'name': x.AK_name, 'value': x.AK_value, 'auth': x.AK_auth}


def getDS(DSid):
    x = DataSet.query.filter(DataSet.DS_id == DSid).first()
    return {'id': x.DS_id, 'name': x.DS_name, 'info': x.DS_info, 'url': x.DS_url}


# 项目下的实验配置
class TestProjectCRUD(Resource):
    # 添加实验
    def post(self):
        tP = TestProject(tP_id=creat_md5_id()[:9], tP_name=request.form['name'], tP_time=datetime.now(),
                         Pid=request.form['pid'], AK1=request.form['AK1'], AK2=request.form['AK2'],
                         DS=request.form['DS'])
        # 上传配置文件
        f = request.files.get('configFile')  # 获取到前端的config文件
        file_dir = os.path.join("App", "data", "config")
        os.makedirs(file_dir, exist_ok=True)  # 创建多层文件夹
        fileName = 'config_' + tP.tP_id + '.' + f.filename.split('.')[-1]  # 文件名为config_+实验Id
        file_url = os.path.join(file_dir, fileName)
        tP.tP_configURL = file_url
        try:
            f.save(file_url)  # 将文件进行保存
            db.session.add(tP)
            db.session.commit()
            return jsonify({'success': True})
        except OSError as oe:  # 文件处理异常
            return jsonify({'success': False, 'message': str(oe)})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 删除实验
    def delete(self):
        try:
            db.session.delete(TestProject.query.filter(TestProject.tP_id == request.json['tPid']).first())
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 查看实验
    def get(self):
        test = []
        for x in TestProject.query.filter(TestProject.Pid == request.args['pid']):
            test.append({'id': x.tP_id, 'name': x.tP_name, 'time': x.tP_time,
                         'status': x.tP_status, 'progress': x.tP_progress,
                         'AK1': getAK(x.AK1), 'AK2': getAK(x.AK2), 'dataSet': getDS(x.DS)})
        return jsonify({'data': test, 'success': True})

    # 实验修改
    def put(self):
        tP = TestProject.query.filter(TestProject.tP_id == request.json['tPid']).first()
        tP.tP_name = request.json['name']
        tP.AK1, tP.AK2, tP.DS = request.json['AK1'], request.json['AK2'], request.json['DS']
        try:
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})
