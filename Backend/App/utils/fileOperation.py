# @Author: LiXiang
# @Time: 2023/11/7 14:45
# @version: 1.0


def upload(file):
    """接受前端传送过来的文件"""
    if file is None:
        # 表示没有发送文件
        return "未上传文件"

    suffix = file.filename.split('.')[-1]  # 取得文件的后缀名
    # 也可以根据文件的后缀名对文件类型进行过滤，如：
    if suffix.lower() not in ['jpg', 'jpeg', 'png', 'rar', 'zip', 'doc', 'docx']:
        return 'Invalid'

    # 将文件保存到某个目录中
    # file.save('D:/test001.' + suffix)
    file.save('./resource/test001.' + suffix)


'''    # 【保存方法一--直接保存】将文件保存到本地
    # 1. 创建一个文件
    f = open("./resource/demo.png", "wb")
    # 2. 向文件写内容
    data = file_obj.read()
    print(data)
    f.write(data)
    # 3. 关闭文件
    f.close()

    # 【保存方式二--使用上下文管理器方式保存】
    with open("./demo.png", "wb") as f:
        data = file_obj.read()
        f.write(data)'''

# f = open('../testExcel.xlsx', 'rb')
print(upload('../testExcel.xlsx'))
