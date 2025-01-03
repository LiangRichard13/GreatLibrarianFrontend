# @Author:LiXiang
# @Time:2025/1/3 13:28
import shutil
import os
from datetime import datetime
from backend_path import BackendPath


def backup_data_and_db(data_folder, db_file, output_folder):
    backup_filename = f"GLF_DataBackup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    backup_filepath = os.path.join(output_folder, backup_filename)

    # 创建一个临时文件夹，用于存放需要备份的文件
    temp_folder = 'temp_backup_folder'
    os.makedirs(temp_folder, exist_ok=True)

    # 将 data 文件夹 拷贝到临时文件夹中
    if os.path.isdir(data_folder):
        shutil.copytree(data_folder, os.path.join(temp_folder, 'data'))
    else:
        print(f"Data folder {data_folder} does not exist!")

    # 将数据库文件拷贝到临时文件夹中
    if os.path.isfile(db_file):
        shutil.copy(db_file, temp_folder)
    else:
        print(f"Database file {db_file} does not exist!")

    shutil.make_archive(backup_filepath.replace('.zip', ''), 'zip', temp_folder)  # 将临时文件夹压缩成 ZIP 文件
    shutil.rmtree(temp_folder)  # 删除临时文件夹
    print(f"Backup successful! The compressed file is stored at {os.path.abspath(backup_filepath)}")


data = os.path.join(BackendPath(), 'APP', 'data')  # 数据文件夹路径
db = os.path.join(BackendPath(), 'instance', 'sqlite3.db')  # 数据库文件路径
output = os.path.join(BackendPath(), '..', 'backups')  # 输出文件夹路径

backup_data_and_db(data, db, output)
