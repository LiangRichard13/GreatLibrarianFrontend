# @Author: LiXiang
# @Time: 2023/11/15 16:36
# @version: 1.0
import hashlib
import random
import time


def creat_md5_id():
    # 生成当前时间戳+一个随机数
    timestamp = int(time.time())  # 获取当前时间戳
    random_number = random.randint(100, 1000)  # 生成1-1000的随机数
    unique_id = f"{timestamp}-{random_number}"
    # print("当前时间戳+随机数:" + unique_id)
    # 使用MD5生成唯一ID
    md5 = hashlib.md5()
    md5.update(unique_id.encode('UTF-8'))
    md5_id = md5.hexdigest()
    # print("生成的ID:" + md5_id)
    return md5_id

# creat_md5_id()
