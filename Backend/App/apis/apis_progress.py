# @Author: LiXiang
# @Time: 2023/12/22 15:21
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *
import re


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
        tP = TestProject.query.filter(TestProject.tP_id == request.args['tPid'])[0]
        if tP.tP_status == 1:
            process = readTemp('APP/data/Logs/' + tP.tP_id + '/process.temp')
            if process >= 0:
                tP.tP_progress = process
                if process == 100:
                    tP.tP_status = 2
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
            return tP.tP_progress
