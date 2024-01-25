# @Author:LiXiang
# @Time:2024/1/25 11:02
import subprocess  # 在终端执行命令库

# 激活 conda 环境
# activate_command = "conda activate GL"
# result = subprocess.run(activate_command, shell=True)
# print(f"命令输出:{result.stdout}___错误信息:{result.stderr}___返回码:{result.returncode}")


# 运行 gltest --help 命令
# gltest_command = "gltest --help"
gltest_command = "conda run -n GL gltest --help"
result = subprocess.run(gltest_command, shell=True, capture_output=True, text=True, encoding='utf-8')
# result = subprocess.run(gltest_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
#                         encoding='utf-8')
# 打印结果
print(f"命令输出:{result.stdout}___错误信息:{result.stderr}___返回码:{result.returncode}")
