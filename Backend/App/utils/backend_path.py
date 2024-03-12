# @Author: LiXiang
# @Time: 2024/3/12 13:06
# @version: 1.0
import os


def BackendPath():
    # 获取当前文件的绝对路径,并截取到App
    file_path = os.path.abspath(__file__)
    index_of_app = file_path.find('App')
    return file_path[:index_of_app] if index_of_app != -1 else print("Backend not found")
