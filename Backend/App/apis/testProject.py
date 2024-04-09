# @Author: LiXiang
# @Time: 2023/12/12 16:07
# @version: 1.0
import os
import shutil
from datetime import datetime

from flask import jsonify, request
from flask_restful import Resource

from App.models import db, APIKey, DataSet, TestProject
from App.utils.MD5_ID import *
from App.utils.backend_path import BackendPath
from App.utils.config_operation import add_call_function, update_code_to_class, update_instance


def getAK(AKid):
    x = APIKey.query.filter(APIKey.AK_id == AKid).first()
    return {'id': x.AK_id, 'name': x.AK_name, 'value': x.AK_value, 'intro': x.AK_intro}


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
        # f = request.files.get('configFile')  # 获取到前端的config文件
        # file_dir = os.path.join("App", "data", "config")
        # os.makedirs(file_dir, exist_ok=True)  # 创建多层文件夹
        # fileName = 'config_' + tP.tP_id + '.' + f.filename.split('.')[-1]  # 文件名为config_+实验Id
        # file_url = os.path.join(file_dir, fileName)
        # tP.tP_configURL = file_url
        try:
            # f.save(file_url)  # 将文件进行保存
            db.session.add(tP)
            db.session.commit()
            return jsonify({'success': True})
        # except OSError as oe:  # 文件处理异常
        #     return jsonify({'success': False, 'message': str(oe)})
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
                         'status': x.tP_status, 'progress': x.tP_progress, 'configURL': x.tP_configURL,
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


# 配置文件的相关操作
class ConfigCRUD(Resource):
    """
        生成配置文件整体流程：
            1、获取到配置脚本中call函数代码,添加至temp配置文件,并检验该代码是否符合python语法要求【post接口】,无误则继续
            2、【生成配置脚本:传实验id】代码均正确无误添加完成后，移动temp配置文件,并添加文件中的类实例化信息【get接口】,信息来源数据库
    """

    # 添加配置文件(加入到数据库)
    def get(self):
        tp = TestProject.query.filter(TestProject.tP_id == request.args['tPid']).first()
        # 配置文件临时区路径
        temp_path = os.path.join(BackendPath(), 'APP', 'data', 'config', 'Temp', 'config_' + tp.tP_id + '.py')
        # 配置文件路径
        config_path = os.path.join('APP', 'data', 'config', 'config_' + tp.tP_id + '.py')
        tp.tP_configURL = config_path  # 修改数据库数据
        config_path = os.path.join(BackendPath(), config_path)
        try:
            shutil.move(temp_path, config_path)  # 移动配置文件
            update_instance(request.args['tPid'])  # 补充配置文件的实例化
            db.session.commit()
            return jsonify({'success': True})
        except shutil.Error as e:
            return jsonify({'success': False, 'message': "移动文件时出错:" + str(e)})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 修改配置文件
    def put(self):
        choose = request.args['choose']  # 修改内容选项【1:call函数,2:实例化参数】
        if choose == '1':  # 修改call函数
            tPid, code, className = request.json['tPid'], request.json['code'], request.json['className']
            temp_path = os.path.join(BackendPath(), 'App', 'data', 'config', 'config_' + tPid + '.py')  # 配置文件临时区路径
            return jsonify({'success': update_code_to_class(temp_path, code, className)})
        elif choose == '2':  # 修改实例化参数
            return jsonify({'success': update_instance(request.json['tPid'])})  # 补充配置文件的实例化

    # 删除配置文件
    def delete(self):
        tp = TestProject.query.filter(TestProject.tP_id == request.json['tPid']).first()
        config_path = os.path.join(BackendPath(), 'APP', 'data', 'config', 'config_' + tp.tP_id + '.py')  # 配置文件路径
        tp.tP_configURL = None
        try:
            os.remove(config_path)
            db.session.commit()
            return jsonify({'success': True})
        except OSError as e:
            return jsonify({'success': False, 'message': "删除文件时出错:" + str(e)})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 添加相应代码至配置文件并进行代码语法检查【参数：tPid实验id,code函数代码,className类名】
    def post(self):
        tPid, code, className = request.json['tPid'], request.json['code'], request.json['className']
        # 配置文件临时区路径
        temp_path = os.path.join(BackendPath(), 'App', 'data', 'config', 'Temp', 'config_' + tPid + '.py')
        flag = 1 if os.path.exists(temp_path) else -1
        return jsonify({'success': add_call_function(temp_path, flag, code, className)})
