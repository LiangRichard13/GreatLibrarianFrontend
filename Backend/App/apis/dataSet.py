# @Author: LiXiang
# @Time: 2023/12/8 16:02
# @version: 1.0
# -*- coding: utf-8 -*-
import os
import shutil

from flask import jsonify, request
from flask_restful import Resource

from App.models import db, DataSet
from App.utils.backend_path import BackendPath


class DataSetCRUD(Resource):
    # 查询数据集【参数:uid,返回:该uid下的所有DS列表】
    def get(self):
        return jsonify({'data': [
            {'id': x.DS_id, 'name': x.DS_name, 'info': x.DS_info, 'url': x.DS_url}
            for x in DataSet.query.filter(DataSet.userid == request.args['uid'])], 'success': True})

    # 添加数据集
    def post(self):
        DS = DataSet(DS_name=request.form['name'], DS_info=request.form['info'], userid=request.form['uid'])
        try:
            f = request.files.get('dataSetFile')  # 获取到前端的zip文件
            file_dir = os.path.join("App", "data", "DataSet", f.filename.replace(('.' + f.filename.split('.')[-1]), ''))
            # 如果目标文件夹已存在，则添加一个随机后缀以避免冲突
            if os.path.exists(os.path.join(BackendPath(), file_dir)):
                count = 1
                while os.path.exists(os.path.join(BackendPath(), file_dir + '(' + str(count) + ')')):
                    count += 1
                file_dir = file_dir + '(' + str(count) + ')'
            DS.DS_url = file_dir  # 存储数据集保存的url

            file_dir = os.path.join(BackendPath(), file_dir)

            os.makedirs(file_dir, exist_ok=True)  # 创建多层文件夹
            file_url = os.path.join(file_dir, f.filename)
            f.save(file_url)  # 将zip文件进行保存
            shutil.unpack_archive(file_url, file_dir, 'zip')  # 解压zip文件
            os.remove(file_url)  # 删除以及解压的zip文件

            db.session.add(DS)
            db.session.commit()
            return jsonify({'success': True})
        except OSError as oe:  # 文件处理异常
            return jsonify({'success': False, 'message': str(oe)})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 删除数据集
    def delete(self):
        try:
            DS = DataSet.query.filter(DataSet.DS_id == request.json['id']).first()
            shutil.rmtree(os.path.join(BackendPath(), DS.DS_url), ignore_errors=True)  # 删除数据集文件
            db.session.delete(DS)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})
