# @Author: LiXiang
# @Time: 2023/12/22 15:32
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import *
import subprocess  # 在终端执行命令库


# 实验操作
class testProjectOperation(Resource):
    # 开始实验
    def post(self):
        tP = TestProject.query.filter(TestProject.tP_id == request.args['tPid'])[0]

        command = 'echo "Hello, World!"'  # 终端中执行的命令
        # result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # print(result.stdout)
