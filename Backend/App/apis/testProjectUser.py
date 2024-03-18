# @Author: LiXiang
# @Time: 2024/1/24 15:05
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import db, TestProjectUser, User, TestProject


# 实验--协作者配置管理
class TestProjectUserCRUD(Resource):
    # 添加协作者【参数：TPid实验ID,uid协作者用户ID】
    def post(self):
        try:
            db.session.add(TestProjectUser(TPid=request.json['TPid'], uid=request.json['uid']))
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 查询【参数：choose查询选择（1:通过实验id找协作者;2:通过协作者id找实验）】
    def get(self):
        # 通过实验id找协作者【参数:TPid实验ID】
        if request.args['choose'] == '1':
            tPUList = TestProjectUser.query.filter(TestProjectUser.TPid == request.args['TPid'])
            collaborators = []
            for tPU in tPUList:
                collaborators.append({'id': tPU.uid, 'name': User.query.filter(User.user_id == tPU.uid)[0].user_name})
            return jsonify({'success': True, 'data': collaborators})  # 返回协作者用户ID列表
        # 通过协作者id找实验【参数:uid协作者用户ID】
        if request.args['choose'] == '2':
            tPUList = TestProjectUser.query.filter(TestProjectUser.uid == request.args['uid'])
            testProjects = []
            for tPU in tPUList:
                testProject = TestProject.query.filter(TestProject.tP_id == tPU.TPid).first()
                testProjects.append({'id': tPU.TPid, 'name': testProject.tP_name})
            return jsonify({'success': True, 'data': testProjects})  # 返回实验ID列表

    # 删除协作者【参数：TPid实验ID,uid协作者用户ID】
    def delete(self):
        tPU = TestProjectUser.query.filter(TestProjectUser.TPid == request.json['TPid'],TestProjectUser.uid == request.json['uid']).first()
        try:
            db.session.delete(tPU)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})
