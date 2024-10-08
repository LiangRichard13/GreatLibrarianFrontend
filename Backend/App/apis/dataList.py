import os
import shutil
from flask_restful import Resource
from flask import jsonify, request

import json
import hashlib
import time


DATASET_CONF = {
    "DATA_SAVE_DIR": r"D:\GreatLibrarianFrontend\Backend\App\data\data_save"
}

DATA_SAVE_DIR = DATASET_CONF["DATA_SAVE_DIR"]

SHARED_LINKS = {}  # 用于存储生成的临时链接


class DataListSearch(Resource):

    #媒体文件设置临时链接
    def generate_shared_link(self, file_path):
        file_hash = hashlib.md5(file_path.encode()).hexdigest()
        SHARED_LINKS[file_hash] = {
            "file_path": file_path,
            "created_at": time.time(),
            "expires_in": 3600
        }
        return file_hash

    #验证临时链接
    def validate_shared_link(self, token):
        for folder_name in os.listdir(DATA_SAVE_DIR):
            folder_path = os.path.join(DATA_SAVE_DIR, folder_name)
            if os.path.isdir(folder_path):
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)
                    generated_token = hashlib.md5(file_name.encode()).hexdigest()
                    if generated_token == token:
                        if os.path.exists(file_path):
                            return file_path
                        else:
                            return None
        return None

    #加载数据
    def load_data(self):
        data_list = []
        for folder_name in os.listdir(DATA_SAVE_DIR):
            folder_path = os.path.join(DATA_SAVE_DIR, folder_name)
            if os.path.isdir(folder_path):
                json_file_path = os.path.join(folder_path, f"{folder_name}.json")
                if os.path.isfile(json_file_path):
                    with open(json_file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        data['uniqid'] = folder_name
                        data_list.append(data)
        return data_list

    #搜索字段标准化
    def normalize_resource(self, resource_input):
        if resource_input is not None:
            resource_input = resource_input.lower()
            if 'ceval' in resource_input.replace('-', '').replace('_', ''):
                return 'C-Eval'
        return resource_input


    def post(self):
        
        # print(request.json['resource'])
        paras = request.json
        # parse param
        resource = paras.get('resource', None)
        data_type_input = paras.get('data_type_input', None)
        data_type_output = paras.get('data_type_output', None)
        test_dimension = paras.get('test_dimension', None)

        print(resource)

        # find data
        try:
            datasets = self.load_data()
            normalized_resource = self.normalize_resource(resource)  # TODO: Fix bug
            filtered_datasets = []

            for dataset in datasets:
                match = True

                if normalized_resource and normalized_resource.lower() not in dataset.get('metadata', {}).get('resource', '').lower():
                    match = False
                if data_type_input and data_type_input not in dataset.get('metadata', {}).get('data_type', ''):
                    match = False
                if data_type_output and data_type_output not in dataset.get('metadata', {}).get('data_type', ''):
                    match = False
                if test_dimension and test_dimension.lower() not in dataset.get('metadata', {}).get('test_dimension', '').lower():
                    match = False

                if match:
                    question_content = dataset.get('data_content', {}).get('question', {})
                    if isinstance(question_content, dict):
                        file_url = question_content.get('file_url', '')
                    else:
                        file_url = ''
                    if file_url.startswith('./'):
                        uniqid = dataset['uniqid']
                        file_url = f"http://localhost:5000/data/data_save/{uniqid}{file_url[1:]}"  # TODO: localhost:5000
                    elif file_url.startswith("http"):
                        pass

                    # parse data to formatted json
                    filtered_datasets.append({
                        "question": dataset["data_content"]["question"],
                        "answer": dataset["data_content"]["answer"],
                        "file_url": file_url,
                        "uploader": dataset.get('metadata', {}).get('uploader', ''),
                        "version_update": {
                            "version": dataset.get('metadata', {}).get('version_update', '').split(';')[0][1:].strip(),
                            "update_time": dataset.get('metadata', {}).get('version_update', '').split(';')[1][:-1].strip() if ';' in dataset.get('metadata', {}).get('version_update', '') else ''
                        },
                        "answer_mode": dataset.get('metadata', {}).get('answer_mode', ''),
                        "data_note": dataset.get('metadata', {}).get('data_note', '')
                    })

            return jsonify({"data": filtered_datasets, "success": True})

        except Exception as e:
            return jsonify({"message": str(e), "success": False}), 500






