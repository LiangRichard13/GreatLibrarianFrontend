# @Author: LiXiang
# @Time: 2023/12/22 15:32
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import TestProject, DataSet, Project, db
import subprocess  # 在终端执行命令库


# 实验操作
class TPOperation(Resource):
    # 用于开发做测试【忽略】
    def get(self):
        try:
            command = "conda run -n GL gltest --help"
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True, encoding='utf-8')
            print(f"命令输出:{result.stdout.strip()}___错误信息:{result.stderr}___返回码:{result.returncode}")
            return jsonify({'success': True})
        except subprocess.CalledProcessError as e:
            return jsonify({'success': False, 'message': str(e)})

    # 开始执行测试实验任务
    def post(self):
        tP = TestProject.query.filter(TestProject.tP_id == request.args['tPid']).first()
        # 命令中的参数
        testcase_path = DataSet.query.filter(DataSet.DS_id == tP.DS).first().DS_url  # 本次实验所用的数据集的文件夹路径
        config_path = 'APP/data/config/config_' + tP.tP_id + '.py'  # 配置文件的文件路径
        project_name = Project.query.filter(Project.project_id == tP.Pid).first().project_name  # 项目名称
        test_name = tP.tP_name  # 实验名称
        test_id = tP.tP_id  # 实验ID
        # 执行实验命令
        command = 'conda run -n GL gltest --testcase_path=' + testcase_path + ' --config_path=' + config_path + \
                  ' --project_name=' + project_name + ' --test_name=' + test_name + ' --test_id=' + test_id
        print(command)
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True, encoding='utf-8')
            print(f"命令输出:{result.stdout}___错误信息:{result.stderr}___返回码:{result.returncode}")
            # 修改实验state状态【0:待实验、1:正在实验、2:待审核、3:已完成】
            tP.tP_status = 1
            db.session.commit()
            return jsonify({'success': True})
        except subprocess.CalledProcessError as e:
            return jsonify({'success': False, 'message': str(e)})
        except Exception as e:  # 数据库操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 更新报告
    def put(self):
        tP = TestProject.query.filter(TestProject.tP_id == request.args['tPid']).first()
        config_path = 'APP/data/config/config_' + tP.tP_id + '.py'  # 配置文件的文件路径
        test_id = tP.tP_id  # 实验ID
        # 更新报告命令
        command = 'conda run -n GL glupdate --config_path=' + config_path + ' --test_id' + test_id
        print(command)
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True, encoding='utf-8')
            print(f"命令输出:{result.stdout}___错误信息:{result.stderr}___返回码:{result.returncode}")
            return jsonify({'success': True})
        except subprocess.CalledProcessError as e:
            return jsonify({'success': False, 'message': str(e)})
