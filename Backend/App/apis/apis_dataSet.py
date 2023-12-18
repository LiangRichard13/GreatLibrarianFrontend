# @Author: LiXiang
# @Time: 2023/12/8 16:02
# @version: 1.0
# -*- coding: utf-8 -*-
import os
import shutil

from flask import jsonify, request
from flask_restful import Resource

from App.models import *


class DataSetOperation(Resource):
    # 查询数据集
    def get(self):
        DS = DataSet.query.filter(DataSet.DS_id == request.args['id'])[0]
        return jsonify({'name': DS.DS_name, 'info': DS.DS_info, 'url': DS.DS_url})

    # 添加数据集
    def post(self):
        DS = DataSet(DS_name=request.form['name'], DS_info=request.form['info'], userid=request.form['uid'])
        zipFile = request.files.get('dataSetFile')  # 获取到前端的zip文件

        file_dir = os.path.join("App", "data", "DataSet", zipFile.filename.split('.')[0])
        DS.DS_url = file_dir  # 存储数据集保存的url

        file_dir_save = os.path.join(file_dir, "all")
        os.makedirs(file_dir_save, exist_ok=True)  # 创建多层文件夹

        file_url = os.path.join(file_dir_save, zipFile.filename)
        zipFile.save(file_url)  # 将zip文件进行保存
        shutil.unpack_archive(file_url, file_dir_save, 'zip')  # 解压zip文件
        os.remove(file_url)  # 删除以及解压的zip文件

        try:
            db.session.add(DS)
            db.session.commit()
            return jsonify({'success': True})
        except OSError as oe:  # 文件处理异常
            return jsonify({'success': False, 'message': oe})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': e})

    # 删除数据集
    def delete(self):
        try:
            db.session.delete(DataSet.query.filter(DataSet.DS_id == request.args['id'])[0])
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': e})

    # 移动数据集【选中所需要数据集】
    def put(self):
        pass
