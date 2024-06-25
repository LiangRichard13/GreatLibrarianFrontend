# @Author: LiXiang
# @Time: 2023/12/22 15:21
# @version: 1.0
import os
import re

from flask import jsonify, request
from flask_restful import Resource

from App.models import db, TestProject
from App.utils.backend_path import BackendPath


# 采用正则化，进行temp文件进行读取
def readTemp(url):
    with open(url, 'r', encoding="utf-8") as file:  # 读取文件内容
        content = file.read()
    match = re.search(r'目前的进度为：(\d+)/(\d+)', content)  # 使用正则表达式匹配数字
    if match:
        current = int(match.group(1))  # 获取"/"前面的数字
        total = int(match.group(2))  # 获取"/"后面的数字
        return round(current / total * 100, 2)
    else:
        return -1  # 未找到进度信息


# print(readTemp('process.temp'))

# progress 实验中进度条的查看、修改
class Progress(Resource):
    # 查看进度条
    def get(self):
        #   状态判断:state=0 待实验【直接返回0】
        #           state=1 正在实验【去查实验的进度】
        #           state=2 待审核【直接返回100】
        #           state=3 已完成【直接返回100】
        tP = TestProject.query.filter(TestProject.tP_id == request.args['tPid']).first()
        if tP.tP_status == 1:
            try:
                process = readTemp(
                    os.path.join(BackendPath(), "App", "data", "Logs", tP.tP_id, "testcase_process.temp"))
            except Exception:
                return jsonify(
                    {'success': False, 'message': tP.tP_id + '-' + tP.tP_name + '读取进度失败', 'progressFail': True})
            if process >= 0:
                tP.tP_progress = process
                # if process == 100:  # 已经完成实验，进行实验状态修改
                #     tP.tP_status = 2
                try:
                    db.session.commit()  # 提交数据库
                    return jsonify({'success': True, 'process': process})
                except Exception as e:  # 数据库操作异常处理
                    db.session.rollback()  # 回滚
                    db.session.flush()  # 刷新，清空缓存
                    return jsonify({'success': False, 'message': str(e)})
            else:
                return jsonify({'success': False, 'message': 'not find'})
        else:
            return jsonify({'success': True, 'process': tP.tP_progress})

    # 进度条连续获取5次失败后请求的接口
    def post(self):
        tP = TestProject.query.filter(TestProject.tP_id == request.args['tPid']).first()
        try:
            tP.tP_status = 0  # 修改实验state状态【0:待实验、1:正在实验、2:待审核、3:已完成】
            db.session.commit()  # 提交数据库
            return jsonify({'success': True})
        except Exception as e:  # 数据库操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 判断是否存在工具箱测试异常
    def delete(self):
        tP = TestProject.query.filter(TestProject.tP_id == request.args['tPid']).first()
        path = os.path.join(BackendPath(), "App", "data", "Logs", tP.tP_id, "traceback.temp")
        return jsonify({'success': True, 'exists': os.path.exists(path)})
