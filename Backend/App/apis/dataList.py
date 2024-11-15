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


def soft_jsonify(obj):
    try:
        return jsonify(obj)
    except:
        return obj

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

            return soft_jsonify({"data": filtered_datasets, "success": True})

        except Exception as e:
            return soft_jsonify({"message": str(e), "success": False}), 500


import random

class TestsetBuild(Resource):
    def __init__(self):
        # 加载数据
        self.data_list_search = DataListSearch()
        self.datasets = self.data_list_search.load_data()
        
    def format_selected_data(self, selected_data, test_dimension_name):
        """格式化选中的数据"""
        formatted_data = {
            "field": test_dimension_name,
            "data": []
        }
        for data in selected_data:
            question_content = data.get('data_content', {}).get('question', {})
            if isinstance(question_content, dict):
                file_url = question_content.get('file_url', '')
            else:
                file_url = ''

            if file_url.startswith('./'):
                uniqid = data['uniqid']
                file_url = f"http://localhost:5000/data/data_save/{uniqid}{file_url[1:]}"
            elif file_url.startswith("http"):
                pass

            formatted_data["data"].append({
                "question": data['data_content']['question'],
                "answer": str(data['data_content']['answer'].get("keywords", [[]])[0]) if test_dimension_name in ["幻觉", "鲁棒性", "公平性", "安全性"] else str(data['data_content']['answer']),
                "file_url": file_url
            })
        print('formatted_data',formatted_data)
        return formatted_data

    # 构建测试数据集的方法
    def build_testset(self, composition):
        result_data = []
        print("Building testset with composition:", composition)  # 打印传入的 composition 数据
        
        for item in composition:
            resource_name = item.get('resource_name')
            test_dimension_name = item.get('test_dimension_name')
            case_number = item.get('case_number')

            print("Processing item:", item)  # 打印每一个 item

            # 验证必要字段
            if not resource_name and not test_dimension_name:
                print("Missing required fields: resource_name or test_dimension_name")
                return {"message": "Either 'resource_name' or 'test_dimension_name' must be provided", "success": False}, 400
            if not isinstance(case_number, int) or case_number <= 0:
                print("Invalid case_number:", case_number)
                return {"message": "Invalid 'case_number'", "success": False}, 400

            # 处理仅有resource_name的情况
            if resource_name and not test_dimension_name:
                matching_data = []
                for dataset in self.datasets:
                    if dataset['metadata']['resource'] == resource_name:
                        matching_data.append(dataset)

                print(f"Found {len(matching_data)} matching datasets for resource_name:", resource_name)
                
                random.shuffle(matching_data)
                selected_data = matching_data[:min(case_number, len(matching_data))]
                print("Selected data:", selected_data)

                # 按 test_dimension_name 分类数据
                test_dimension_dict = {}
                for data in selected_data:
                    test_dimension = data['metadata']['test_dimension']
                    if test_dimension not in test_dimension_dict:
                        test_dimension_dict[test_dimension] = []
                    test_dimension_dict[test_dimension].append(data)

                # 格式化并添加到结果数据
                for test_dimension_name, grouped_data in test_dimension_dict.items():
                    formatted_data = self.format_selected_data(grouped_data, test_dimension_name)
                    result_data.append(formatted_data)
                    print('添加到result_data:',result_data)

            # 处理仅有test_dimension_name的情况
            elif test_dimension_name and not resource_name:
                matching_data = []
                for dataset in self.datasets:
                    if dataset['metadata']['test_dimension'] == test_dimension_name:
                        matching_data.append(dataset)

                print(f"Found {len(matching_data)} matching datasets for test_dimension_name:", test_dimension_name)

                random.shuffle(matching_data)
                selected_data = matching_data[:min(case_number, len(matching_data))]

                if selected_data:
                    formatted_data = self.format_selected_data(selected_data, test_dimension_name)
                    result_data.append(formatted_data)

            # 处理同时有resource_name和test_dimension_name的情况
            elif resource_name and test_dimension_name:
                matching_data = []
                for dataset in self.datasets:
                    if (dataset['metadata']['resource'] == resource_name and 
                            dataset['metadata']['test_dimension'] == test_dimension_name):
                        matching_data.append(dataset)

                print(f"Found {len(matching_data)} matching datasets for resource_name and test_dimension_name:", resource_name, test_dimension_name)

                random.shuffle(matching_data)
                selected_data = matching_data[:min(case_number, len(matching_data))]

                if selected_data:
                    formatted_data = self.format_selected_data(selected_data, test_dimension_name)
                    result_data.append(formatted_data)
        
        print("Final result_data:", result_data)
        return {"data": result_data, "success": True}, 200

    def post(self):
        try:
            paras = request.json
            print("Received parameters:", paras)  # 打印传入的参数
            composition = paras.get('composition', [])
            
            # 调用 post 方法构建测试集
            result_data, status_code = self.build_testset(composition)
            print(result_data, type(result_data))
            return result_data, status_code

        except Exception as e:
            return soft_jsonify({"message": str(e), "success": False}), 500


